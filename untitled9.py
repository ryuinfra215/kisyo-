import streamlit as st
from streamlit_folium import st_folium
import folium

# --- アプリの基本設定 ---
st.set_page_config(page_title="座標取得ツール Ver. 2.0")
st.title("🗺️ 地図クリック座標取得ツール Ver. 2.0")
st.write("地図上の任意の地点をクリックすると、その場所にピンが立ちます。")
st.info("ピンをクリックすると表示される座標を、Googleフォームに貼り付けてください。")

# --- Streamlitのセッションステートを使って、クリックした位置を記憶する ---
if "last_clicked_point" not in st.session_state:
    st.session_state.last_clicked_point = None

# --- 地図の表示 ---
# 地図の中心を日本のあたりに設定
map_center = [35, 135]
m = folium.Map(location=map_center, zoom_start=5)

# (改良点！) 記憶しているピンがあれば、地図が描画される前にピンを追加する
if st.session_state.last_clicked_point:
    lat, lon = st.session_state.last_clicked_point
    popup_text = f"緯度: {lat:.4f}<br>経度: {lon:.4f}"
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_text, max_width=200)
    ).add_to(m)

# 地図を表示し、クリックされた情報を `map_data` に格納
map_data = st_folium(m, width='100%')

# (改良点！) クリックされたら、その位置を記憶してアプリを再実行させる
if map_data and map_data["last_clicked"]:
    clicked_point = (map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"])
    # 記憶している点と違う場所がクリックされたら更新
    if clicked_point != st.session_state.last_clicked_point:
        st.session_state.last_clicked_point = clicked_point
        st.rerun() # アプリをリフレッシュしてピンを即座に表示
        
# --- 座標の表示 ---
st.header("取得した座標")
if st.session_state.last_clicked_point:
    lat, lon = st.session_state.last_clicked_point
    st.text("緯度（北緯）:")
    st.code(f"{lat:.6f}")
    st.text("経度（東経）:")
    st.code(f"{lon:.6f}")
else:
    st.write("地図上をクリックして地点を指定してください。")
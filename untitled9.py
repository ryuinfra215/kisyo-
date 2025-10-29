# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 09:55:59 2025

@author: yff59
"""

import streamlit as st
from streamlit_folium import st_folium
import folium

# --- アプリの基本設定 ---
st.set_page_config(page_title="台風予想コンテスト 座標取得ツール")
st.title("🗺️ 台風予想コンテスト 座標取得ツール")
st.info("下の「予想時間」を選んでから、地図をクリックして座標を取得してください。")

# --- Streamlitのセッションステートを初期化 ---
# 4つの時間帯の座標をそれぞれ記憶する場所を作る
if "point_24h" not in st.session_state:
    st.session_state.point_24h = None
if "point_48h" not in st.session_state:
    st.session_state.point_48h = None
if "point_72h" not in st.session_state:
    st.session_state.point_72h = None
if "point_96h" not in st.session_state:
    st.session_state.point_96h = None

# --- 1. 予想時間を選択するラジオボタン ---
st.subheader("1. 予想時間を選択")
forecast_time = st.radio(
    label="まず、地図でクリックしたい予想時間を選んでください。",
    options=["24時間後", "48時間後", "72時間後", "96時間後"],
    horizontal=True,
    label_visibility="collapsed"
)

# --- 2. 地図の表示 ---
st.subheader(f"2. 「{forecast_time}」の予想地点をクリック")
map_center = [35, 135]
m = folium.Map(location=map_center, zoom_start=5)

# --- すでにピンが押されている場所を地図に表示 ---
# 24h
if st.session_state.point_24h:
    lat, lon = st.session_state.point_24h
    folium.Marker([lat, lon], popup="24時間後の予想", icon=folium.Icon(color="blue")).add_to(m)
# 48h
if st.session_state.point_48h:
    lat, lon = st.session_state.point_48h
    folium.Marker([lat, lon], popup="48時間後の予想", icon=folium.Icon(color="green")).add_to(m)
# 72h
if st.session_state.point_72h:
    lat, lon = st.session_state.point_72h
    folium.Marker([lat, lon], popup="72時間後の予想", icon=folium.Icon(color="orange")).add_to(m)
# 96h
if st.session_state.point_96h:
    lat, lon = st.session_state.point_96h
    folium.Marker([lat, lon], popup="96時間後の予想", icon=folium.Icon(color="red")).add_to(m)

# 地図を表示し、クリックされた情報を `map_data` に格納
map_data = st_folium(m, width='100%', height=400)

# --- 3. クリック処理 ---
# クリックされたら、選択中の予想時間の座標を更新する
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    
    if forecast_time == "24時間後":
        st.session_state.point_24h = (lat, lon)
    elif forecast_time == "48時間後":
        st.session_state.point_48h = (lat, lon)
    elif forecast_time == "72時間後":
        st.session_state.point_72h = (lat, lon)
    elif forecast_time == "96時間後":
        st.session_state.point_96h = (lat, lon)
    
    # クリックしたら即座に再実行して、下の「取得した座標」表示を更新する
    st.rerun()

# --- 4. 取得した座標の表示 ---
st.divider()
st.subheader("3. 取得した座標の確認")

def show_coordinate(label, point_data):
    """座標を表示する関数"""
    if point_data:
        st.text(f"✅ {label}:")
        st.code(f"緯度: {point_data[0]:.6f}, 経度: {point_data[1]:.6f}", language=None)
    else:
        st.text(f"❌ {label}: 未入力（地図をクリックしてください）")

show_coordinate("24時間後", st.session_state.point_24h)
show_coordinate("48時間後", st.session_state.point_48h)
show_coordinate("72時間後", st.session_state.point_72h)
show_coordinate("96時間後", st.session_state.point_96h)

# --- 5. 応募ボタン ---
st.divider()
st.subheader("4. 応募フォームを開く")

# 4つすべて入力されたかチェック
all_filled = (
    st.session_state.point_24h and
    st.session_state.point_48h and
    st.session_state.point_72h and
    st.session_state.point_96h
)

if all_filled:
    st.success("すべての座標が入力されました！下のボタンから応募してください。")
    
    # --- ★★★ ここをあなたの情報（8個のID）に書き換えてください ★★★ ---
    
    YOUR_FORM_ID = "1FAIpQLSe341DAqBnQbaWtJqodSFLsnXwvm9Y7nTtOZU0a8wsNmAi5eA" # あなたのフォームID
    
    ENTRY_ID_LAT_24 = "entry.1947537758" # 24h・緯度
    ENTRY_ID_LON_24 = "entry.266065608" # 24h・経度
    ENTRY_ID_LAT_48 = "entry.1717988796" # 48h・緯度
    ENTRY_ID_LON_48 = "entry.1267246012" # 48h・経度
    ENTRY_ID_LAT_72 = "entry.2112374973" # 72h・緯度
    ENTRY_ID_LON_72 = "entry.178056443" # 72h・経度
    ENTRY_ID_LAT_96 = "entry.1345580482" # 96h・緯度
    ENTRY_ID_LON_96 = "entry.1665500649" # 96h・経度
    
    # --- ★★★ 書き換えここまで ★★★ ---

    # 座標データを取得
    lat24, lon24 = st.session_state.point_24h
    lat48, lon48 = st.session_state.point_48h
    lat72, lon72 = st.session_state.point_72h
    lat96, lon96 = st.session_state.point_96h

    # 8個のデータを埋め込んだ超・長いURLを作成
    gform_url = (
        f"https://docs.google.com/forms/d/e/{YOUR_FORM_ID}/viewform?usp=pp_url"
        f"&{ENTRY_ID_LAT_24}={lat24:.6f}"
        f"&{ENTRY_ID_LON_24}={lon24:.6f}"
        f"&{ENTRY_ID_LAT_48}={lat48:.6f}"
        f"&{ENTRY_ID_LON_48}={lon48:.6f}"
        f"&{ENTRY_ID_LAT_72}={lat72:.6f}"
        f"&{ENTRY_ID_LON_72}={lon72:.6f}"
        f"&{ENTRY_ID_LAT_96}={lat96:.6f}"
        f"&{ENTRY_ID_LON_96}={lon96:.6f}"
    )
    
    st.link_button(
        label="✅ 全ての座標を自動入力して応募フォームを開く", 
        url=gform_url, 
        type="primary",
        use_container_width=True
    )

else:
    st.warning("4つの予想時間すべてに座標を入力すると、ここに応募ボタンが表示されます。")
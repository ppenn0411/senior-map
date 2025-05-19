import streamlit as st
import folium
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide") # 가로 레이아웃 넓게 설정 유지

# Streamlit 앱 제목
# st.markdown("## Senior Map") # 메인 제목 첫 줄 (기존)
# st.write("") # 빈 줄 추가 (기존)
# st.write("서울시 고령층 만성질환자 의료 접근성 해소를 위한 지역별 진료격차 분석 서비스") # 메인 제목 둘째 줄 (설명) (기존)
st.markdown("## 🗺️ Senior Map") # 메인 제목 첫 줄 (h2) - 이모티콘 추가
st.markdown("### 서울시 고령층 만성질환자 의료 접근성 해소를 위한 지역별 진료격차 분석 서비스") # 메인 제목 둘째 줄 (h3)

st.markdown("---") # 타이틀 아래 구분선 추가

# 데이터 로드
geojson_filepath = 'seoul_municipalities_geo_simple.json'
seoul_geo_data = gpd.read_file(geojson_filepath)
district_names = seoul_geo_data['name'].unique().tolist()

# 세션 상태 초기화
if "selected_district" not in st.session_state:
    st.session_state.selected_district = district_names[0]

def get_district_by_point(lat, lon):
    """위도, 경도 기준으로 어느 지역구인지 반환"""
    point = Point(lon, lat)  # shapely는 (x,y) = (lon, lat)
    for _, row in seoul_geo_data.iterrows():
        if row.geometry.contains(point):
            return row['name']
    return None

with st.sidebar:
    # st.markdown("# 관심있는 지역을 선택하세요") # 사이드바 상단 제목 추가 (이미지로 교체)
    st.markdown("---") # 구분선 추가

    # 이미지와 설명 텍스트를 위한 컬럼 생성
    col_img, col_text = st.columns([1, 2]) # 이미지 컬럼:텍스트 컬럼 비율 (예시로 1:2)

    with col_img:
        # st.markdown("# 관심있는 지역을 선택하세요") # 사이드바 상단 제목 추가 (이미지로 교체)
        st.image("seniormap.png", width=150) # 이미지 크기 조정: width 설정

    with col_text:
        st.markdown("##### 서비스 설명") # 텍스트 상자 제목
        st.write(
            "서울시 고령층 만성질환자의 의료 접근성을 개선하기 위한 지역별 진료 격차 분석 서비스입니다. "
            "지도를 통해 지역별 현황을 확인하고 상세 데이터를 볼 수 있습니다."
        ) # 웹사이트 설명 텍스트 추가

    st.markdown("---") # 구분선 추가: 이미지/텍스트와 selectbox 사이

    # 사이드바 지도
    seoul_center = [37.5665, 126.9780]
    m_sidebar = folium.Map(location=seoul_center, zoom_start=11, min_zoom=10)

    folium.GeoJson(
        seoul_geo_data,
        name='서울시 지역구 경계',
        style_function=lambda x: {'fillColor': '#808080', 'color': 'black', 'weight': 1, 'fillOpacity': 0.1},
        highlight_function=lambda x: {'fillColor': 'orange', 'color': 'orange', 'weight': 5, 'fillOpacity': 0.5},
        tooltip=folium.features.GeoJsonTooltip(fields=['name'], aliases=['지역구:'])
    ).add_to(m_sidebar)

    # 지도 렌더링 및 클릭 데이터 받기
    map_data_sidebar = st_folium(m_sidebar, height=400, use_container_width=True)

    if map_data_sidebar and map_data_sidebar.get("last_clicked"):
        lat, lon = map_data_sidebar["last_clicked"]["lat"], map_data_sidebar["last_clicked"]["lng"]
        clicked_district = get_district_by_point(lat, lon)
        if clicked_district and clicked_district != st.session_state.selected_district:
            st.session_state.selected_district = clicked_district

    selected = st.selectbox(
        "지역구 구분:",
        district_names,
        index=district_names.index(st.session_state.selected_district),
        key="selectbox_district"
    )
    if selected != st.session_state.selected_district:
        st.session_state.selected_district = selected

# 메인 영역: 상세 지도 및 클릭 이벤트
st.write(f"##### 선택된 지역구: {st.session_state.selected_district}")

# 선택된 지역구 지도 표시
selected_geo = seoul_geo_data[seoul_geo_data['name'] == st.session_state.selected_district]
if not selected_geo.empty:
    centroid = selected_geo.geometry.centroid.iloc[0]
    m_main = folium.Map(location=[centroid.y, centroid.x], zoom_start=13, min_zoom=13, tiles='CartoDB.Positron')

    folium.GeoJson(
        selected_geo,
        style_function=lambda feature: {
            'fillColor': 'transparent',
            'color': 'blue',
            'weight': 3,
            'fillOpacity': 0.0
        },
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['선택된 지역구:'])
    ).add_to(m_main)

    # 메인 지도 클릭 이벤트 처리
    map_data_main = st_folium(m_main, height=500, use_container_width=True)

    if map_data_main and map_data_main.get("last_clicked"):
        lat, lon = map_data_main["last_clicked"]["lat"], map_data_main["last_clicked"]["lng"]
        clicked_district_main = get_district_by_point(lat, lon)
        if clicked_district_main and clicked_district_main != st.session_state.selected_district:
            st.session_state.selected_district = clicked_district_main

    # --- 그래프 영역 (두 개의 열) ---
    st.markdown("#### 지역별 상세 통계 (예시)") # 그래프 영역 제목
    col1_graph, col2_graph = st.columns(2) # 그래프를 위한 두 개의 열 생성

    with col1_graph:
        st.markdown("##### 예시 그래프 1")
        # 예시 데이터 생성
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        # Matplotlib 그래프 생성
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.plot(x, y1)
        ax1.set_title(f'{st.session_state.selected_district} - 추세 1')
        ax1.set_xlabel('X 값')
        ax1.set_ylabel('Y 값')
        # Streamlit에 그래프 표시
        st.pyplot(fig1, use_container_width=True)

    with col2_graph:
        st.markdown("##### 예시 그래프 2")
        # 예시 데이터 생성
        y2 = np.cos(x)
        # Matplotlib 그래프 생성
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.plot(x, y2, color='red')
        ax2.set_title(f'{st.session_state.selected_district} - 추세 2')
        ax2.set_xlabel('X 값')
        ax2.set_ylabel('Y 값')
        # Streamlit에 그래프 표시
        st.pyplot(fig2, use_container_width=True)

else:
    st.warning("선택된 지역구 정보를 찾을 수 없습니다.")

# --- 푸터 (출처) ---
st.markdown("---") # 푸터 구분선
st.markdown("###### 데이터 출처: [공공 데이터 포털](https://www.data.go.kr/) 등") # 예시 출처 정보

import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

# Streamlit 앱 제목
st.markdown("## 시니어케어맵: 서울시 지역별 고령층 고수요 질환 진료역량 분석 기반 의료기관 추가지역 제안 서비스")

# 사이드바
st.sidebar.header('지역구 선택')

# GeoJSON 파일 경로
geojson_filepath = 'seoul_municipalities_geo_simple.json'

# 서울시 경계 데이터 로드
try:
    seoul_geo_data = gpd.read_file(geojson_filepath)
except Exception as e:
    st.sidebar.error(f'서울시 경계 데이터를 로드하는 데 오류가 발생했습니다: {e}')
    st.sidebar.warning('geopandas 및 관련 라이브러리(fiona, pyproj 등) 설치 상태를 확인해 주세요.')
    st.stop()

district_names = seoul_geo_data['name'].unique().tolist()

# 세션 상태 초기화
if 'selected_district' not in st.session_state:
    st.session_state.selected_district = district_names[0]

# selectbox 변경 시 세션 상태 업데이트
def update_district_from_sidebar():
    st.session_state.selected_district = st.session_state.sidebar_selectbox

# 사이드바: 지역구 선택
st.sidebar.selectbox(
    '지역구를 선택하세요:',
    district_names,
    index=district_names.index(st.session_state.selected_district),
    key='sidebar_selectbox',
    on_change=update_district_from_sidebar
)

# 지도 생성 및 사이드바에 표시
with st.sidebar:
    st.markdown("### 🗺️ 서울시 전체 지도")
    seoul_center = [37.5665, 126.9780]
    m = folium.Map(location=seoul_center, zoom_start=11, min_zoom=10)

    # 스타일 함수
    def style_function(feature):
        return {'fillColor': '#808080', 'color': 'black', 'weight': 1, 'fillOpacity': 0.1}

    def highlight_function(feature):
        return {'fillColor': 'orange', 'color': 'orange', 'weight': 5, 'fillOpacity': 0.5, 'bringToFront': True}

    folium.GeoJson(
        seoul_geo_data,
        name='서울시 지역구 경계',
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(fields=['name'], aliases=['지역구:'])
    ).add_to(m)

    # 지역구 이름 마커 추가
    for _, row in seoul_geo_data.iterrows():
        centroid = row.geometry.centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            icon=folium.features.DivIcon(
                icon_size=(150, 20),
                icon_anchor=(75, 0),
                html=f'<div style="font-size: 10pt; text-align: center;">{row["name"]}</div>',
                class_name="map-label"
            )
        ).add_to(m)

    # 지도 표시
    try:
        map_data = st_folium(m, height=600, use_container_width=True)
        if map_data and 'last_object_clicked' in map_data and map_data['last_object_clicked']:
            clicked_props = map_data['last_object_clicked'].get('properties')
            if clicked_props:
                clicked_name = clicked_props.get('name')
                if clicked_name in district_names:
                    st.session_state.selected_district = clicked_name
    except Exception as e:
        st.warning(f"지도 상호작용 처리 중 오류 발생: {e}")

# 메인 화면: 선택된 지역구 정보
st.subheader('선택된 지역구 상세 형태')
st.write(f'현재 선택된 지역구: **{st.session_state.selected_district}**')

# 선택된 지역구 지도 표시
selected_geo = seoul_geo_data[seoul_geo_data['name'] == st.session_state.selected_district]
if not selected_geo.empty:
    centroid = selected_geo.geometry.centroid.iloc[0]
    m_detail = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB.Positron', min_zoom=11)

    def detail_style_function(feature):
        if feature['properties']['name'] == st.session_state.selected_district:
            return {
                'fillColor': 'transparent',
                'color': 'blue',
                'weight': 3,
                'fillOpacity': 0.0
            }
        return {'fillOpacity': 0.0}

    folium.GeoJson(
        selected_geo,
        name='선택된 지역구',
        style_function=detail_style_function,
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['선택된 지역구:'])
    ).add_to(m_detail)

    st_folium(m_detail, height=400, use_container_width=True)
else:
    st.warning("선택된 지역구 정보를 찾을 수 없습니다.")

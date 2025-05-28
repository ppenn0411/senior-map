import streamlit as st
import base64

# 이미지 파일을 Base64 문자열로 인코딩하는 함수
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Base64 문자열을 사용하여 배경 이미지를 설정하는 함수
def set_png_as_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover; /* 배경 이미지를 컨테이너에 맞게 조절 */
        background-position: center; /* 배경 이미지 가운데 정렬 */
        background-repeat: no-repeat; /* 배경 이미지 반복 방지 */
        background-attachment: fixed; /* 배경 이미지를 뷰포트에 고정 */
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
#이미지 파일 패치치   
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{b64_encoded}"

# Base64 인코딩된 이미지 경로
image_base64 = get_base64_image("map5.png")



st.set_page_config(page_title="한눈맵65+", layout="wide")

# 사용자 지정 CSS 스타일 (버튼 가로 스크롤, 세로 크기 조절, 컨테이너 배경색, 제목 및 버튼 텍스트 줄바꿈 방지를 위한 수정)
st.markdown(
    """
    <style>
        /* Streamlit 제목 글자 크기 및 위치 조절 */
        .stApp h1 {
            font-size: 3em !important; /* 제목 글자 크기 설정 (원하는 크기로 조절 가능) */
            margin-top: -30px !important; /* 제목을 위로 약간 올립니다 (값 조절 가능) */
            /* white-space: nowrap; */ /* 줄바꿈 방지 */
            /* overflow: hidden; */ /* 넘치는 텍스트 숨김 */
            /* text-overflow: ellipsis; */ /* 넘치는 텍스트를 말줄임표로 표시 */
            text-align: center; /* 제목 가운데 정렬 */
        }

        /* Streamlit 버튼 스타일, 텍스트 줄바꿈 방지 */
        div.stButton > button {
             width: 100%; /* 버튼의 너비를 부모 컬럼에 맞춰 100%로 설정 */
             height: 100%; /* 버튼의 세로 높이를 부모 컨테이너에 맞춰 100%로 설정 */
             padding-top: 15px; /* 위쪽 패딩 추가 */
             padding-bottom: 15px; /* 아래쪽 패딩 추가 */
             white-space: nowrap; /* 줄바꿈 방지 */
             overflow: hidden; /* 넘치는 텍스트 숨김 */
             text-overflow: ellipsis; /* 넘치는 텍스트를 말줄임표로 표시 */
             font-size: 3em !important;  /* 버튼 글자 크기만 키우기 */
        }

        /* 버튼들을 담는 내부 st.columns 컨테이너에 Flexbox 및 스크롤 설정 */
        /* 이 컨테이너는 이제 제목 옆의 컬럼 안에 배치됩니다. */
        /* 제목과 버튼을 감싸는 외부 st.columns 컨테이너 스타일 */
        /*
        [data-testid="stColumns"]:nth-of-type(1) {
            background-color: #483D8B !important; /* 군청색 배경 설정 (강화) */
            padding-top: 10px !important; /* 위쪽 패딩 10px (강화) */
            padding-bottom: 10px !important; /* 아래쪽 패딩 10px (강화) */
            padding-left: 0 !important; /* 좌우 패딩 0 */
            padding-right: 0 !important; /* 좌우 패딩 0 */
            margin-bottom: 20px; /* 이 섹션 아래 내용과의 간격 */
            width: 100vw; /* 뷰포트 너비에 맞춤 */
            position: relative; /* 내부 요소의 위치 기준 설정 */
            left: 50%; /* 가운데 정렬을 위해 왼쪽으로 50% 이동 */
            right: 50%;
            margin-left: -50vw; /* 가운데 정렬을 위해 왼쪽 마진 음수값 설정 */
            margin-right: -50vw; /* 가운데 정렬을 위해 오른쪽 마진 음수값 설정 */
            z-index: 10; /* 배경 이미지 위에 쌓임 순서 설정 (값 증가) */
        }
        */

        [data-testid="stColumns"]:nth-of-type(2) {
            display: flex; /* Flexbox 레이아웃 활성화 */
            flex-wrap: nowrap; /* 컬럼(버튼)들이 줄바꿈되지 않도록 강제 */
            overflow-x: auto; /* 내용이 넘칠 때 가로 스크롤바 표시 */
            overflow-y: hidden; /* 세로 스크롤바 숨김 */
            /* 스크롤바가 콘텐츠를 가리지 않도록 하단 패딩 추가 (필요 시) */
             padding-bottom: 15px; /* 스크롤바를 위한 하단 패딩은 유지 */
             /* 버튼이 세로 공간을 채울 수 있도록 부모 컨테이너의 최소 높이 설정 */
             min-height: 100px; /* 원하는 최소 높이 값으로 설정 */
             align-items: center; /* 자식 요소(컬럼)들을 수직 중앙 정렬 시도 */
             /* background-color: #000; */ /* 기존 버튼 컨테이너 검정색 배경 제거 */
        }

        /* 버튼들을 담는 내부 st.columns의 각 컬럼(버튼 컨테이너) 스타일 */
        [data-testid="stColumns"]:nth-of-type(2) > div {
             flex-shrink: 0; /* 컬럼이 줄어들지 않도록 설정 */
             /* min-width: 100px; /* 필요 시 최소 너비 설정 */ */
             /* flex-basis나 width로 각 컬럼의 기본 크기 조절 가능 */
             /* 컬럼 사이 간격은 st.columns의 gap 속성이나 여기 margin-right로 조절 가능 */
             margin-right: 10px; /* 컬럼 사이 간격 추가 */
             /* 버튼이 세로 공간을 채울 수 있도록 이 컨테이너의 높이 설정 (필요 시) */
             /* height: auto; */ /* 또는 고정 높이 */
        }

        /* 마지막 컬럼의 오른쪽 마진 제거 (선택 사항) */
        [data-testid="stColumns"]:nth-of-type(2) > div:last-child {
            margin-right: 0;
        }

        /* 구분선 (hr 태그) 스타일 - 제거 */
        /*
        .stApp hr {
            border: none !important;
            border-top: 4px solid #bbb !important;
            margin-top: 20px !important;
            margin-bottom: 20px !important;
            width: 100% !important;
        }
        */

        /* 이전 텍스트 줄바꿈 방지 CSS 제거 */
        /*
        .stApp h2, .stApp p, .stApp div {
            white-space: nowrap;
        }
        */


    </style>
    """,
    unsafe_allow_html=True,
)

# background.png 파일을 읽어서 배경 이미지로 설정
set_png_as_bg("background.png")

# 페이지 목록 정의 (이름: 값 형태 유지)
pages = {
    "홈": "main",
    "의료 수요 맵": "page1",
    "의료 공급 맵": "page2",
    "의료 취약도 맵": "page3",
    "의원 분포 맵": "page4",
    
}

# 페이지 이름 목록
page_names = list(pages.keys())

# session_state를 사용하여 현재 페이지 상태 유지
if 'current_page_name' not in st.session_state:
    st.session_state.current_page_name = page_names[0] # 초기 페이지 설정

# 제목과 버튼 컨테이너를 나란히 배치할 컬럼 생성
title_col, buttons_col = st.columns([3, 7]) # 비율 조정 가능 [제목 컬럼 비율, 버튼 컬럼 비율]

with title_col:
    st.markdown("""
        <h1 style='text-align: left;'>
            한눈맵 65<span style='color: red;'><sup>+</sup></span>
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)


with buttons_col:
    # 페이지 이동 버튼 생성 (가로 배열)
    # 이전의 st.columns 코드가 이제 이 buttons_col 안에 들어갑니다.
    cols = st.columns(len(page_names))
    for i, page_name in enumerate(page_names):
        with cols[i]:
            # 각 버튼에 고유한 key를 할당합니다.
            # 버튼 클릭 시 해당 페이지로 이동하고 스크립트를 다시 실행합니다.
            # 버튼 텍스트에 줄바꿈 문자 추가
            button_text = f"{page_name}\n\n\n" # 버튼 세로 크기를 위해 줄바꿈 문자는 유지
            if st.button(button_text, key=f"btn_{pages[page_name]}"):
                st.session_state.current_page_name = page_name
                st.rerun() # 페이지 상태 변경 후 스크립트 다시 실행


# 선택된 페이지 이름에 해당하는 페이지 '값'을 찾아서 내용 표시
current_page_value = pages[st.session_state.current_page_name]


 # 서비스 개요를 위한 검정색 박스
st.markdown("""
    <div style="
        background-color: black; /* 검정색 */
        width: 100%; /* 컨테이너 너비에 맞춤 */
        height: 200px; /* 박스 높이 (원하는 높이로 조절 가능) */
        margin-top: 20px; /* 위에 약간의 간격 추가 */
        margin-bottom: 20px; /* 아래에 약간의 간격 추가 - 페이지 1~4 헤더 간격에 맞춰 조정 */
     "></div>
 """, unsafe_allow_html=True)
if current_page_value == "main":

    
    # 메인 페이지 헤더에 군청색 배경 박스 추가
    st.markdown(f"""
    <div style="
        background-color: black;
        padding: 10px;
        margin-bottom: 15px;
        text-align: center;
    ">
        <img src="{image_base64}" style="width: 1300px; height: 800px; object-fit: contain;"/>
    </div>
    """, unsafe_allow_html=True)

elif current_page_value == "page1":
    # 페이지 1 헤더에 검정색 배경 박스 추가
    st.markdown("""
        <div style="
            background-color: black; /* 검정색 */
            padding: 10px; /* 내부 여백 */
            margin-bottom: 15px; /* 아래쪽 간격 */
            text-align: center; /* 텍스트 중앙 정렬 */
        ">
            <h2 style="color: white; text-align: center;">서울시 고령층 만성질환 의료 수요 맵</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 이곳은 첫 번째 페이지입니다. 대신 iframe 삽입
    st.markdown(
        '''
        <div style="display: flex; justify-content: center;">
        <iframe title="page1" width="100%" height="750" src="https://app.powerbi.com/view?r=eyJrIjoiZTBjZjNhYTctYmQ2Mi00ZDk3LWI3MjAtYThkOTM4ZTI1MjE2IiwidCI6IjAyZjU1YjU3LWZmMzEtNGMzZC1hYzA0LTBhMjQwOGIxNDgyMCJ9" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        ''', unsafe_allow_html=True
    )

elif current_page_value == "page2":
    # 페이지 2 헤더에 검정색 배경 박스 추가
    st.markdown("""
        <div style="
            background-color: black; /* 검정색 */
            padding: 10px; /* 내부 여백 */
            margin-bottom: 15px; /* 아래쪽 간격 */
            text-align: center; /* 텍스트 중앙 정렬 */
        ">
            <h2 style="color: white; text-align: center;">서울시 고령층 만성질환 의료 공급 맵</h2>
        </div>
    """, unsafe_allow_html=True)
    # 이곳은 두 번째 페이지입니다. 대신 iframe 삽입
    st.markdown(
        '''
        <div style="display: flex; justify-content: center;">
        <iframe title="page2" width="100%" height="750" src="https://app.powerbi.com/view?r=eyJrIjoiOGMyZGZiNjgtY2Y1My00Njc2LWJkNzMtNmYxNmU5NWMxYzFiIiwidCI6IjAyZjU1YjU3LWZmMzEtNGMzZC1hYzA0LTBhMjQwOGIxNDgyMCJ9" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        ''', unsafe_allow_html=True
    )

elif current_page_value == "page3":
    # 페이지 3 헤더에 검정색 배경 박스 추가
    st.markdown("""
        <div style="
            background-color: black; /* 검정색 */
            padding: 10px; /* 내부 여백 */
            margin-bottom: 15px; /* 아래쪽 간격 */
            text-align: center; /* 텍스트 중앙 정렬 */
        ">
            <h2 style="color: white; text-align: center;">서울시 고령층 만성질환 의료 취약도 맵</h2>
        </div>
    """, unsafe_allow_html=True)
    # 이곳은 세 번째 페이지입니다. 대신 iframe 삽입
    st.markdown(
        '''
        <div style="display: flex; justify-content: center;">
        <iframe title="page3" width="100%" height="750" src="https://app.powerbi.com/view?r=eyJrIjoiOWJiN2QyNGUtNjIxOC00NTI2LTk1ZWYtMmI2MzY3ZWY5ODg4IiwidCI6IjAyZjU1YjU3LWZmMzEtNGMzZC1hYzA0LTBhMjQwOGIxNDgyMCJ9" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        ''', unsafe_allow_html=True
    )

elif current_page_value == "page4":
    # 페이지 4 헤더에 검정색 배경 박스 추가
    st.markdown("""
        <div style="
            background-color: black; /* 검정색 */
            padding: 10px; /* 내부 여백 */
            margin-bottom: 15px; /* 아래쪽 간격 */
            text-align: center; /* 텍스트 중앙 정렬 */
        ">
            <h2 style="color: white; text-align: center;">서울시 고령층 만성질환 의료 분포 맵</h2>
        </div>
    """, unsafe_allow_html=True)
    # 이곳은 네 번째 페이지입니다. 대신 iframe 삽입
    st.markdown(
        '''
        <div style="display: flex; justify-content: center;">
        <iframe title="page4" width="100%" height="750" src="https://app.powerbi.com/view?r=eyJrIjoiODdmOTQ1NzEtYWIwMy00ZjYyLTg5ZWYtM2Q3ZGIyODliYjgzIiwidCI6IjAyZjU1YjU3LWZmMzEtNGMzZC1hYzA0LTBhMjQwOGIxNDgyMCJ9" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        ''', unsafe_allow_html=True
    )
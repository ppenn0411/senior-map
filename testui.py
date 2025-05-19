#push test
import streamlit as st

st.set_page_config(layout="wide")

st.title('Senior Care Map!')

with st.expander('About "Senior Care Map"'):
  st.write('서울시 내 의료기관 진료역량을 정량화하고, 고령층 인구와 비교해 지역별 수요–공급 격차를 분석')
  st.image('SeniorMap Logo.png', width=250)

st.sidebar.header('고혈압, 당뇨를 앓고 계신가요?')
user_name = st.sidebar.text_input('당신의 이름을 알려주세요.')
user_address = st.sidebar.selectbox('당신이 살고 있는 곳은 어딘가요?', ['금천구', '광진구', '서대문구', '서초구', '강서구', '중량구', '성동구','송파구','용산구','강동구','종로구','도봉구', '동작구', '마포구', '은평구', '중구', '강북구', '동대문구', '성북구', '노원구', '강남구', '양천구', '영등포구', '구로구', '관악구'])

st.header('출력')

col1, col2, col3 = st.columns(3)

with col1:
  if user_name != '':
    st.write(f'👋 안녕하세요 {user_name}님!')
  else:
    st.write('👈  **이름**을 입력해 주세요!')

with col2:
  if user_address != '':
    st.write(f'{user_address}는 당신이 사는 곳입니다!')
  else:
    st.write('👈 **사는 곳**을 선택해 주세요!')


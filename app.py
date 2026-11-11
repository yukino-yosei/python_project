import streamlit as st
from datetime import date
import db
from api import get_video, get_rest_api_data
import json
import pandas as pd

db.init_db()

# try :
st.title('유튜브 영상 조회 앱')
user_id = st.text_input('로그 저장용 문구를 입력해주세요.')
youtube_url = st.text_input('영상 url을 입력해주세요')

log_data = None

if st.button('조회') :
    data = get_video(youtube_url)
    if data == '올바른 주소 아님' :
        st.write('올바른 주소가 아닙니다.')
    else :
        log_data = db.log_view(user_id)
        log_data[youtube_url] = data['items'][0]['snippet']['title']
        db.log_change(user_id, log_data)

        st.write(f"### {data['items'][0]['snippet']['title']}")
        st.image(data['items'][0]['snippet']['thumbnails']['default']['url'], width = data['items'][0]['snippet']['thumbnails']['default']['width'])
        st.video(youtube_url)

if log_data is None :
    st.write('로그가 없습니다.')
else :
    st.write('검색 로그')
    for i in log_data :
        st.write(f"{i} - {log_data[i]}")
# except :
    # print("오류 발생")
st.write('- - -')
rst = get_rest_api_data()
df = pd.DataFrame({
    'ID' : i['id'],
    'EMAIL' : i['email'],
    'ZIPCODE' : i['address']['zipcode'],
    'LAT' : i['address']['geo']['lat'],
    'LNG' : i['address']['geo']['lng']
} for i in rst)
st.dataframe(df)
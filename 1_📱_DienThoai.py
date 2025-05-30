
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 00:12:35 2023

@author: Admin
"""

# -*- coding: utf-8 -*-
import PIL.Image
import streamlit as st
import pandas as pd
from datetime import date,timedelta
import plotly.express as px
import plotly.graph_objects as go
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import sqlite3
from db_config import init_db, get_staff_list, add_tip, get_statistics_by_range, get_statistics_by_period
import io


icon = PIL.Image.open("favicon.ico")
st.set_page_config(page_title="Glow Nails Spa",page_icon=icon, layout="centered",initial_sidebar_state="collapsed")
#tialogo = PIL.Image.open("tia-logo06.png")


icon = PIL.Image.open("favicon.ico")
st.set_page_config(page_title="Matdohanhkhach",page_icon=icon, layout="centered",initial_sidebar_state="collapsed")
#tialogo = PIL.Image.open("tia-logo06.png")

get_today=date.today()+ timedelta(days=0)
today_day=get_today.strftime("%Y-%m-%d")


#-------------- Web Design - User Authentication --------------#


# names = ["matdo","ktg","tia"]
# usernames = ["matdo","ktg","tia"]
# file_path = Path(__file__).parent / "hashed_pw1.pkl"

# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)

# credentials = {"usernames":{}}

# for un, name, pw in zip(usernames, names, hashed_passwords):
#     user_dict = {"name":name,"password":pw}
#     credentials["usernames"].update({un:user_dict})


# authenticator = stauth.Authenticate(credentials,"MDHK","tsn123",cookie_expiry_days=30)
# name, authentication_status, username = authenticator.login("Login", "main")




# if authentication_status == False:
#     st.error("❌ Ten dang nhap hoac mat khau khong dung")
# if authentication_status == None:
#     st.warning("💁 Vui long nhap ten dang nhap va mat khau")
# if authentication_status:


       



    #number = st.sidebar.number_input('Hệ số ghế',key='seat_cont')
  
   #---------- lessen the distace of space at the header -----------#
    
st.markdown("""
        <style>
                .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
    #---------- Hiden hamburger button -----------#
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
    

# Initialize and check database
conn = init_db()
staff_list = get_staff_list(conn)

# Title
st.title("Nails Management")

# --- Add Tip Entry ---
st.subheader("Thêm Tiền Tip")
staff_name = st.selectbox("Tên Nhân Viên:", staff_list)
tip_amount = st.number_input("Số Tiền Tip:", min_value=0.0, step=1.0)
tip_date = st.date_input("Ngày Nhận Tip:", value=date.today())

if st.button("Thêm Tiền Tip"):
    add_tip(conn, staff_name, tip_amount, tip_date)
    st.success("✅ Đã thêm tiền tip thành công!")

# --- View Statistics ---
st.subheader("Thống Kê Tiền Tip")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Ngày Bắt Đầu:", value=date.today() - timedelta(days=7))
with col2:
    end_date = st.date_input("Ngày Kết Thúc:", value=date.today())

if st.button("Xem Thống Kê"):
    df = get_statistics_by_range(conn, start_date, end_date)
    total_tip = df['Tổng Tiền Tip'].sum()
    st.write(f"**Thống Kê từ {start_date} đến {end_date}**")
    st.write(f"**Tổng Tiền Tip:** ${total_tip:.2f}")
    st.dataframe(df)

    # Always show download button if df is available
    if not df.empty:
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        st.download_button(
            label="📥 Tải Excel",
            data=output,
            file_name=f"{today_day}_tip_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# --- Line Chart ---
st.subheader("Biểu Đồ Tổng Tiền Tip")
period = st.radio("Chọn thời gian thống kê:", ["Ngày", "Tuần", "Tháng"], horizontal=True)

df_chart = get_statistics_by_period(conn, period.lower())
if not df_chart.empty:
    fig = px.line(df_chart, x='time', y='total', color='staff_name', title=f"Tổng tiền tip theo {period.lower()}")
    st.plotly_chart(fig)
else:
    st.info("Không có dữ liệu để hiển thị biểu đồ.")


#------------ Hiden Streamlit and change to TIA slogan -----------#
hide_streamlit_style = """
        <style>
        footer {visibility: hidden;}
        footer:after {content:'All rights reserved, Khánh Nails 2025'; visibility: visible;display: block;position: relative;padding: 5px;top: 2px;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
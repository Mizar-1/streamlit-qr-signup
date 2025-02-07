import streamlit as st
import sqlite3
import pandas as pd
import qrcode
from io import BytesIO

# 数据库初始化
def init_db():
    conn = sqlite3.connect("signups.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 存储用户数据
def save_to_db(name):
    conn = sqlite3.connect("signups.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# 读取数据库数据
def get_users():
    conn = sqlite3.connect("signups.db")
    df = pd.read_sql("SELECT * FROM users", conn)
    conn.close()
    return df

# 生成二维码
def generate_qr(link):
    qr = qrcode.make(link)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# 初始化数据库
init_db()

# Streamlit 界面
st.title("活动签到系统")

# 生成二维码
form_url = "https://your-streamlit-app.com"  # 修改为实际 Streamlit 部署地址
st.subheader("扫码签到")
qr_image = generate_qr(form_url)
st.image(qr_image, caption="扫描二维码进行签到", use_container_width=False)

# 用户输入签到
txt_name = st.text_input("请输入您的姓名:")
if st.button("签到"):
    if txt_name:
        save_to_db(txt_name)
        st.success(f"{txt_name}，签到成功！")
    else:
        st.error("请输入姓名！")

# 显示所有签到用户
st.subheader("已签到用户")
user_data = get_users()
st.dataframe(user_data)

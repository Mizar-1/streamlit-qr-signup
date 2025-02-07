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


# 用户输入签到
txt_name = st.text_input("请输入您的姓名:")
if st.button("签到"):
    if txt_name:
        save_to_db(txt_name)
        st.success(f"{txt_name}，签到成功！")
    else:
        st.error("请输入姓名！")


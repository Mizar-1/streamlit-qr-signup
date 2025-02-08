import streamlit as st
import sqlite3
import os

# 连接 SQLite 数据库
conn = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = conn.cursor()

#检查user_data.db路径是否一致
print(os.path.abspath("user_data.db"))

# 创建用户数据表（如果不存在）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')
conn.commit()

# Streamlit 界面
st.title("🎉 活动签到")

# 用户输入姓名
name = st.text_input("请输入您的姓名")

# 提交按钮
if st.button("✅ 签到"):
    if name:
        # 检查是否已签到
        cursor.execute("SELECT * FROM users WHERE name=?", (name,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            st.warning("您已签到，无需重复签到！")
        else:
            # 插入数据
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            st.success(f"欢迎 {name}！签到成功 🎉")
    else:
        st.error("请输入姓名后再签到")

# 关闭数据库连接
conn.close()


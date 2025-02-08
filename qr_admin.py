import streamlit as st
import pandas as pd
import sqlite3

# 连接 SQLite 数据库
conn = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = conn.cursor()

# 创建用户数据表（如果不存在）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')
conn.commit()

# Streamlit 界面
st.title("后台管理系统")

# 统计已签到人数
cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]
st.subheader(f"✅ 已签到人数: {total_users}")

# 显示已签到用户列表
st.subheader("📋 签到用户列表")
df_users = pd.read_sql("SELECT * FROM users", conn)
st.dataframe(df_users,use_container_width = True)

# 搜索功能
search_query = st.text_input("🔍 搜索用户（输入姓名）")
if search_query:
    df_users = df_users[df_users["name"].str.contains(search_query, case=False, na=False)]

st.dataframe(df_users, use_container_width=True)

if st.button("🔄 刷新数据"):
    st.experimental_rerun()

# 数据导出
if st.button("📥 导出 Excel"):
    df_users.to_excel("签到用户.xlsx", index=False)
    st.success("数据已导出为 Excel 文件")

# 删除用户数据
delete_user = st.text_input("❌ 删除用户（输入姓名）")
if st.button("删除用户") and delete_user:
    cursor.execute("DELETE FROM users WHERE name=?", (delete_user,))
    conn.commit()
    st.success(f"用户 {delete_user} 已删除")
    st.experimental_rerun()

# 关闭数据库连接
conn.close()
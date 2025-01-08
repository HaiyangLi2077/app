
import streamlit as st
import pandas as pd
import numpy as np

# 标题
st.title("我的第一个 Streamlit 应用")

# 文本
st.write("这是一个从 Colab 迁移的 Streamlit 应用！")

# 创建一个简单的数据表
st.write("### 随机数据表")
data = pd.DataFrame({
    'A': np.random.rand(10),
    'B': np.random.rand(10),
    'C': np.random.rand(10)
})
st.write(data)

# 绘制图表
st.write("### 随机数据折线图")
st.line_chart(data)

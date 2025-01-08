import streamlit as st
import pandas as pd
import numpy as np
import pygwalker as pyg
import plotly.express as px

# 设置页面标题和图标
st.set_page_config(
    page_title="UK Biobank 在线分析",
    page_icon="📊",
    layout="wide"
)

# 自定义 CSS 样式
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stSelectbox, .stSlider {
        margin-bottom: 20px;
    }
    .stHeader {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.title("📊 UK Biobank 在线分析")
st.markdown("通过上传 UKB 数据进行自定义分析")

# 侧边栏
with st.sidebar:
    st.header("设置")
    st.markdown("在这里配置数据和分析选项。")

# 检查是否已安装 pygwalker，如果没有则安装
try:
    import pygwalker as pyg
except ImportError:
    st.warning("正在安装 pygwalker...")
    st.spinner("安装中...")
    !pip install pygwalker -q
    import pygwalker as pyg

# 检查是否已安装 pandas，如果没有则安装
try:
    import pandas as pd
except ImportError:
    st.warning("正在安装 pandas...")
    st.spinner("安装中...")
    !pip install pandas -q
    import pandas as pd

# 加载 FieldID 数据
st.header("📋 FieldID 数据表")


mapping_df = pd.read_csv("/mount/src/app/FieldID.csv")
st.write(mapping_df)

# 上传 UKB 原始数据
st.header("📤 上传 UKB 原始数据")
uploaded_file = st.file_uploader("上传你的 UKB 数据文件 (CSV 或 Excel)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # 读取数据为 Pandas 数据框
    if uploaded_file.name.endswith('.csv'):
        data_df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        data_df = pd.read_excel(uploaded_file)

    # 检查并处理重复的 FieldID
    if mapping_df['FieldID'].duplicated().any():
        st.warning("发现重复的 FieldID，保留第一个出现的值。")
        mapping_df = mapping_df.drop_duplicates(subset='FieldID', keep='first')

    # 创建映射字典
    mapping_dict = dict(zip(mapping_df['FieldID'], mapping_df['Description']))

    # 重命名列
    missing_cols = [col for col in data_df.columns if col not in mapping_dict]
    if missing_cols:
        st.warning(f"以下列未找到映射: {missing_cols}。这些列将保留原始名称。")

    data_df.rename(columns=mapping_dict, inplace=True)
    st.success("数据上传完成！")

    # 显示数据表
    st.header("📄 上传的数据表")
    st.write(data_df)

    # 绘制图表
    st.header("📈 数据可视化")
    chart_type = st.selectbox("选择图表类型", ["折线图", "柱状图", "散点图"])
    if chart_type == "折线图":
        fig = px.line(data_df, title="随机数据折线图")
    elif chart_type == "柱状图":
        fig = px.bar(data_df, title="随机数据柱状图")
    else:
        fig = px.scatter(data_df, x=data_df.columns[0], y=data_df.columns[1], title="随机数据散点图")

    st.plotly_chart(fig, use_container_width=True)

    # 使用 Pygwalker 进行高级分析
    st.header("🔍 高级数据分析")
    st.markdown("使用 Pygwalker 进行交互式数据分析。")
    pyg.walk(data_df)

# 页脚
st.markdown("---")
st.markdown("© 2023 UK Biobank 在线分析. 保留所有权利。")

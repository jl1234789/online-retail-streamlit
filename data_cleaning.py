# ----------------------
# Streamlit 应用主入口
# ----------------------
st.set_page_config(page_title="电商客户分析", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_excel("data/Online Retail.xlsx")
    df = df[df['CustomerID'].notnull()]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    return df


df = load_data()

# ----------------------
# 侧边栏筛选器
# ----------------------
st.sidebar.title("📂 页面导航")
country_list = sorted(df['Country'].unique())
selected_country = st.sidebar.selectbox("选择国家", country_list)
page = st.sidebar.radio("选择页面", ["📊 数据概览", "👥 客户分析", "📘 项目介绍"])

# 时间范围提示和选择器
min_date = df['InvoiceDate'].min().date()
max_date = df['InvoiceDate'].max().date()

st.sidebar.markdown(f"**数据时间范围**：{min_date} 至 {max_date}")

selected_date = st.sidebar.date_input(
    "选择时间范围",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(selected_date, tuple):
    start_date, end_date = selected_date
else:
    start_date = end_date = selected_date

mask = (
    (df['Country'] == selected_country) &
    (df['InvoiceDate'].dt.date >= start_date) &
    (df['InvoiceDate'].dt.date <= end_date)
)
df_filtered = df[mask]

# ----------------------
# 页面 1：数据概览
# ----------------------
if page == "📊 数据概览":
    st.title(f"📊 {selected_country} 国家销售概览")
    st.markdown(
        f"数据包含 **{df_filtered.shape[0]:,}** 条交易记录，覆盖 **{df_filtered['CustomerID'].nunique()}** 位客户。")

    col1, col2, col3 = st.columns(3)
    col1.metric("总销售额 💰", f"£{df_filtered['TotalPrice'].sum():,.0f}")
    col2.metric("订单数 📦", f"{df_filtered['InvoiceNo'].nunique():,}")
    col3.metric("商品种类数 🏷️", f"{df_filtered['StockCode'].nunique():,}")

    # 销售趋势图
    st.subheader("📈 月度销售趋势")
    monthly_sales = (
        df_filtered.set_index("InvoiceDate")
        .resample("M")["TotalPrice"]
        .sum()
        .reset_index()
    )
    monthly_sales["Month"] = monthly_sales["InvoiceDate"].dt.strftime("%Y-%m")
    st.line_chart(data=monthly_sales, x="Month", y="TotalPrice")

    # Top 10 产品销售额
    st.subheader("🔥 销售额 Top10 商品")
    top_products = (
        df_filtered[df_filtered['Quantity'] > 0]
        .groupby('Description')['TotalPrice']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_products)

    # 退货率分析
    st.subheader("↩️ 每月退货率趋势")
    df_filtered['IsReturn'] = df_filtered['Quantity'] < 0
    df_filtered['Month'] = df_filtered['InvoiceDate'].dt.to_period('M')

    return_summary = (
        df_filtered.groupby(['Month', 'IsReturn'])['TotalPrice']
        .sum().unstack(fill_value=0).reset_index()
    )
    return_summary.columns.name = None
    return_summary['ReturnRate'] = abs(
        return_summary[True]) / (return_summary[False] + abs(return_summary[True]))
    return_summary['Month'] = return_summary['Month'].astype(str)

    st.line_chart(data=return_summary, x='Month', y='ReturnRate')

# ----------------------
# 页面 2：客户分析
# ----------------------
elif page == "👥 客户分析":
    st.title(f"👥 {selected_country} 客户 RFM 分析")

    df_no_return = df_filtered[df_filtered['Quantity'] > 0]
    rfm_df = calculate_rfm(df_no_return)
    rfm_df = label_rfm(rfm_df)

    st.subheader("客户分群（Top / Loyal / At Risk / Lost）")
    st.dataframe(
        rfm_df[['CustomerID', 'Recency', 'Frequency',
                'Monetary', 'RFM_Score', 'Customer_Segment']]
        .sort_values("RFM_Score", ascending=False)
        .reset_index(drop=True)
    )

    st.subheader("📊 客户标签分布")
    segment_counts = rfm_df['Customer_Segment'].value_counts().sort_index()
    st.bar_chart(segment_counts)

    st.download_button(
        label="📥 下载客户RFM数据",
        data=rfm_df.to_csv(index=False).encode('utf-8-sig'),
        file_name=f"rfm_{selected_country}.csv",
        mime="text/csv"
    )

# ----------------------
# 页面 3：项目介绍
# ----------------------
elif page == "📘 项目介绍":
    st.title("📘 项目介绍")

    st.markdown("""
    **项目名称：** 在线零售客户分析（Online Retail Customer Analysis）  
    **数据来源：** UCI Machine Learning Repository - Online Retail Dataset  

    **项目目标：**  
    - 通过 RFM 模型识别不同客户群体  
    - 分析各国销售表现与退货率  
    - 探索高价值商品与客户行为模式  
    - 构建可交互分析平台辅助业务决策

    **核心功能：**
    - 数据筛选：按国家 & 时间范围筛选交易数据  
    - 销售概览：查看订单数、销售额、商品种类、月度趋势与退货率  
    - 客户分析：RFM 模型分群，导出客户分群结果  
    - 商品分析：识别热销商品 Top10

    **技术栈：**  
    Python, Pandas, Streamlit, Excel 数据处理, 可视化分析

    """)

# rfm_analysis.py
import streamlit as st
import pandas as pd
from datetime import timedelta

# ----------------------
# RFM 分析函数
# ----------------------


def calculate_rfm(df):
    snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    rfm['R'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm['F'] = pd.qcut(rfm['Frequency'].rank(method="first"),
                       5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['M'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['RFM_Score'] = rfm[['R', 'F', 'M']].sum(axis=1)
    return rfm.reset_index()


def label_rfm(rfm_df):
    rfm_df['Customer_Segment'] = pd.cut(
        rfm_df['RFM_Score'],
        bins=[0, 6, 9, 11, 15],
        labels=['Lost', 'At Risk', 'Loyal', 'Top']
    )
    return rfm_df


# import pandas as pd


# def calculate_rfm(df: pd.DataFrame, snapshot_date: str = "2011-12-10") -> pd.DataFrame:
#     # 将分析日期设为最后交易日前后几天（可以参数化）
#     snapshot_date = pd.to_datetime(snapshot_date)

#     # 按客户聚合 RFM
#     rfm = df.groupby('CustomerID').agg({
#         'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
#         'InvoiceNo': 'nunique',
#         'TotalPrice': 'sum'
#     }).reset_index()

#     rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

#     # 删除 Monetary 为 0 的客户（无价值）
#     rfm = rfm[rfm['Monetary'] > 0]

#     # 计算分位数评分（4-高分，1-低分）
#     rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
#     rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(
#         method='first'), 4, labels=[1, 2, 3, 4])
#     rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])

#     # 拼接 RFM Segment
#     rfm['RFM_Segment'] = rfm['R_Score'].astype(
#         str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

#     # 计算 RFM 得分总和
#     rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].astype(
#         int).sum(axis=1)

#     return rfm

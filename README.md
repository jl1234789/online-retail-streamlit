# 在线零售客户分析 (Online Retail Customer Analysis)

## 项目简介

本项目基于著名的 UCI Online Retail 数据集，使用 Python 和 Streamlit 构建了一个交互式数据分析平台。  
通过数据清洗、销售趋势分析及客户 RFM 模型分群，帮助理解业务状况及客户价值，具备实际商业应用价值。

---

## 功能介绍

- 按国家和时间范围筛选销售数据  
- 查看销售总额、订单数、商品种类数等关键指标  
- 展示月度销售趋势和退货率变化  
- 挖掘销售额 Top10 商品  
- 利用 RFM 模型对客户进行分群（Top / Loyal / At Risk / Lost）  
- 支持导出客户 RFM 数据 CSV 文件  

---

## 技术栈

- Python  
- Pandas（数据处理）  
- Streamlit（快速构建交互式 Web 应用）  

---

## 在线体验

项目已部署 Streamlit Cloud
👉 [https://online-retail-app.streamlit.app/](https://online-retail-app.streamlit.app/)

---
## 使用说明
   pip install -r requirements.txt
   streamlit run app.py

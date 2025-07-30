from data_cleaning import load_and_clean_data

df = load_and_clean_data("data/Online Retail.xlsx")

print(df.head())
print(df.info())
print("👥 客户数量：", df['CustomerID'].nunique())
print("📦 总订单数：", df['InvoiceNo'].nunique())
print("💰 总销售额：", df['TotalPrice'].sum())

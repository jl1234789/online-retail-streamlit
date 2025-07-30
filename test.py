import pandas as pd

try:
    df = pd.read_excel('data/Online Retail.xlsx')
    print(df.shape)
except Exception as e:
    print("读取失败:", e)

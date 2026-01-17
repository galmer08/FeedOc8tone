import pandas as pd

try:
    df = pd.read_excel(r'd:\Antigravity\FeedOc8tone\Tiendastic\Productos.xlsx', nrows=5)
    print("Columns found:")
    for col in df.columns:
        print(f"- {col}")
    print("\nFirst row sample:")
    print(df.iloc[0].to_dict())
except Exception as e:
    print(f"Error reading excel: {e}")

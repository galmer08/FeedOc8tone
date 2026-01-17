import pandas as pd

try:
    df = pd.read_excel(r'd:\Antigravity\FeedOc8tone\Tiendastic\Productos.xlsx', nrows=1)
    print("Clean Column List:")
    for col in df.columns:
        print(f"'{col}'")
except Exception as e:
    print(f"Error: {e}")

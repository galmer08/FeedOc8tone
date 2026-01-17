import pandas as pd

try:
    target_id = 4170086 # From XML
    df = pd.read_excel(r'd:\Antigravity\FeedOc8tone\Tiendastic\Productos.xlsx')
    match = df[(df['Id'] == target_id) | (df['Id Variante'] == target_id)]
    if not match.empty:
        print("Match found:")
        print(match[['Id', 'Id Variante', 'SKU', 'Nombre']].to_string())
    else:
        print(f"No match found for {target_id} in Id or Id Variante")
except Exception as e:
    print(f"Error: {e}")

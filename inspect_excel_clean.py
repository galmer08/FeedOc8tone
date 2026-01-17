import pandas as pd

try:
    df = pd.read_excel(r'd:\Antigravity\FeedOc8tone\Tiendastic\Productos.xlsx')
    
    # Filter for products likely to have usage info (creams, shampoos)
    keywords = ['piel', 'cabello', 'cutis', 'ideal para', 'indicado para']
    pattern = '|'.join(keywords)
    
    # Matches where description contains one of the keywords
    matches = df[df['Descripcion'].str.contains(pattern, case=False, na=False)]
    
    if not matches.empty:
        print(f"Found {len(matches)} items matching keywords.")
        # Print ID and full description of first 5 matches
        for index, row in matches.head(5).iterrows():
            print(f"\n--- ID: {row['Id']} ({row['Nombre']}) ---")
            desc = str(row['Descripcion'])
            # Limit print length but enough to see context
            print(desc[:500] + "..." if len(desc) > 500 else desc)
    else:
        print("No matches found.")

except Exception as e:
    print(f"Error: {e}")

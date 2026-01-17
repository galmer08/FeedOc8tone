import xml.etree.ElementTree as ET
import requests
import io
import pandas as pd
import os

def load_excel_data(excel_path):
    """Loads product data from Excel and returns a dictionary indexed by Id."""
    print(f"Loading Excel data from {excel_path}...")
    try:
        df = pd.read_excel(excel_path)
        # Ensure Id is treated as string for consistent matching
        df['Id'] = df['Id'].astype(str)
        # Create a dictionary for fast lookup: Id -> Row Data (dict)
        # We drop na values to avoid keys with 'nan'
        data_dict = df.set_index('Id').to_dict('index')
        print(f"Loaded {len(data_dict)} products from Excel.")
        return data_dict
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return {}

def clean_text(text):
    """Cleans text for XML output."""
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    return text.strip().replace('\n', ' ').replace('\r', '')

def enrich_feed(input_url, output_file, excel_path):
    print(f"Downloading feed from {input_url}...")
    response = requests.get(input_url)
    response.raise_for_status()
    
    # Load Excel Data
    product_data = load_excel_data(excel_path)
    
    # Register the namespace to ensure output uses 'g:' prefix
    ET.register_namespace('g', "http://base.google.com/ns/1.0")
    
    # Parse XML from the downloaded content
    tree = ET.parse(io.BytesIO(response.content))
    root = tree.getroot()
    ns = {'g': 'http://base.google.com/ns/1.0'}
    
    count = 0
    enriched_count = 0
    
    for item in root.findall('.//item'):
        g_id = item.find('g:id', ns).text
        
        # Look up in Excel data
        excel_item = product_data.get(str(g_id))
        
        if excel_item:
            enriched_count += 1
            # --- Generate Rich Title for AI Bot ---
            # Format: [Nombre Excel] | [Marca Excel] | [Categoría Excel]
            nombre_excel = clean_text(excel_item.get('Nombre', ''))
            marca_excel = clean_text(excel_item.get('Marca', ''))
            categoria_excel = clean_text(excel_item.get('Categoria', '')) # Full path
            
            title_parts = [nombre_excel]
            
            # Add Brand if not present (case insensitive check)
            if marca_excel and marca_excel.lower() not in nombre_excel.lower():
                title_parts.append(marca_excel)
                
            # Add Full Category for context
            if categoria_excel:
                title_parts.append(categoria_excel)
                
            new_title = " | ".join(title_parts)
            
            # Update Title in XML
            title_elem = item.find('g:title', ns)
            if title_elem is not None:
                title_elem.text = new_title

            # --- Generate Technical Description for AI Bot ---
            # Structure: Key-Value pairs + Full Description
            
            sku_excel = clean_text(excel_item.get('SKU', ''))
            barcode_excel = clean_text(excel_item.get('Barcode', ''))
            desc_excel = clean_text(excel_item.get('Descripcion', '')) # Rich description
            
            desc_lines = []
            desc_lines.append(f"Producto: {nombre_excel}")
            if marca_excel:
                desc_lines.append(f"Marca: {marca_excel}")
            if categoria_excel:
                desc_lines.append(f"Categoría: {categoria_excel}")
            if sku_excel:
                desc_lines.append(f"SKU: {sku_excel}")
            if barcode_excel:
                desc_lines.append(f"Barcode: {barcode_excel}")
            
            desc_lines.append("---")
            desc_lines.append("Descripción Detallada:")
            desc_lines.append(desc_excel if desc_excel != "nan" else "No disponible")
            
            new_desc = "\n".join(desc_lines)
            
            # Update Description in XML
            desc_elem = item.find('g:description', ns)
            if desc_elem is None:
                desc_elem = ET.SubElement(item, '{http://base.google.com/ns/1.0}description')
            desc_elem.text = new_desc

        count += 1

    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Processed {count} items. Enriched {enriched_count} items using Excel data. Saved to {output_file}")

if __name__ == "__main__":
    FEED_URL = "https://files.batitienda.com/xml/catalog/epUw7zmO7x1_C4-A7f2WTw2"
    # Use absolute path to ensure CRON/GitHub Actions find it
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXCEL_PATH = os.path.join(BASE_DIR, 'Tiendastic', 'Productos.xlsx')
    
    enrich_feed(FEED_URL, 'output_feed.xml', EXCEL_PATH)

import xml.etree.ElementTree as ET
import requests
import io

def enrich_feed(input_url, output_file):
    print(f"Downloading feed from {input_url}...")
    response = requests.get(input_url)
    response.raise_for_status()
    
    # Register the namespace to ensure output uses 'g:' prefix
    ET.register_namespace('g', "http://base.google.com/ns/1.0")
    
    # Parse XML from the downloaded content
    tree = ET.parse(io.BytesIO(response.content))
    root = tree.getroot()
    ns = {'g': 'http://base.google.com/ns/1.0'}
    
    count = 0
    
    for item in root.findall('.//item'):
        title = item.find('g:title', ns)
        title_text = title.text if title is not None else ""
        
        brand = item.find('g:brand', ns)
        brand_text = brand.text if brand is not None else ""
        
        product_type = item.find('g:product_type', ns)
        product_type_text = product_type.text if product_type is not None else ""
        
        gtin = item.find('g:gtin', ns)
        gtin_text = gtin.text if gtin is not None else ""
        
        # Enrich Title
        # Format: [Title] | [Brand] | [Category]
        title_parts = [title_text]
        
        if brand_text:
            title_parts.append(brand_text)
            
        if product_type_text:
            # We use the full product type string
            title_parts.append(product_type_text)
            
        new_title = " | ".join(title_parts)
        if title is not None:
            title.text = new_title
            
        # Original description
        description_elem = item.find('g:description', ns)
        
        # New Description Format:
        # Producto: [Título]. Marca: [Marca]. Categoría: [Categoría]. Ideal para búsquedas de [Categoría]. Código: [GTIN].
        
        parts = []
        if title_text:
            parts.append(f"Producto: {title_text}.")
        
        if brand_text:
            parts.append(f"Marca: {brand_text}.")
            
        if product_type_text:
            parts.append(f"Categoría: {product_type_text}. Ideal para búsquedas de {product_type_text}.")
            
        if gtin_text:
            parts.append(f"Código: {gtin_text}.")
        else:
             parts.append("Código: No disponible.")

        new_desc = " ".join(parts)
        
        if description_elem is None:
            description_elem = ET.SubElement(item, '{http://base.google.com/ns/1.0}description')
        
        description_elem.text = new_desc
        count += 1

    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Processed {count} items. Saved to {output_file}")

if __name__ == "__main__":
    FEED_URL = "https://files.batitienda.com/xml/catalog/epUw7zmO7x1_C4-A7f2WTw2"
    enrich_feed(FEED_URL, 'output_feed.xml')

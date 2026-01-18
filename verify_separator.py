import xml.etree.ElementTree as ET

def verify_separator(xml_file, target_id):
    print(f"Verifying Separator for ID {target_id} in {xml_file}...")
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {'g': 'http://base.google.com/ns/1.0'}
        
        for item in root.findall('.//item'):
            g_id = item.find('g:id', ns).text
            if g_id == target_id:
                title = item.find('g:title', ns).text
                print(f"\n--- Item {g_id} ---")
                print(f"Title: {title}")
                
                # Check for " |" vs " | "
                if " | " in title:
                     print("FAIL: Found ' | ' (space after pipe).")
                elif " |" in title and " ||" not in title: # Ensure it's the pattern we want
                     print("PASS: Found ' |' and no Space after pipe.")
                else:
                     print("WARNING: Separator pattern unclear.")
                     
                return

        print(f"Item {target_id} not found in XML.")

    except Exception as e:
        print(f"Error parsing XML: {e}")

if __name__ == "__main__":
    verify_separator('output_feed.xml', '2392180')

import xml.etree.ElementTree as ET

def verify_debug(xml_file, target_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'g': 'http://base.google.com/ns/1.0'}
    
    for item in root.findall('.//item'):
        g_id = item.find('g:id', ns).text
        if g_id == target_id:
            title = item.find('g:title', ns).text
            print(f"Title: {title!r}")
            # Find all occurrences of pipe
            for i, char in enumerate(title):
                if char == '|':
                    c_before = title[i-1] if i>0 else 'START'
                    c_after = title[i+1] if i<len(title)-1 else 'END'
                    print(f"Pipe at {i}: '{c_before}' | '{c_after}'")

if __name__ == "__main__":
    verify_debug('output_feed.xml', '2392180')

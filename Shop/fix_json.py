import json

# Read the file with correct encoding
try:
    with open('data.json', 'r', encoding='utf-16') as f:
        data = json.load(f)
    
    # Write it back as proper UTF-8
    with open('data_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print('File fixed successfully as data_fixed.json')
except Exception as e:
    print(f'Error: {e}')
    
    # Try with utf-8-sig to remove BOM
    try:
        with open('data.json', 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        with open('data_fixed.json', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print('BOM removed, saved as data_fixed.json')
    except Exception as e2:
        print(f'Second attempt failed: {e2}')
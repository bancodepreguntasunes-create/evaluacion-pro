p = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript_full.jsonl'
with open(p, 'rb') as fp:
    data = fp.read()

f_idx = data.rfind(b'Fecha,C')
if f_idx != -1:
    print("Found in transcript_full at byte:", f_idx)
    text = data[f_idx:].decode('utf-8', errors='ignore')
    # End is at the closing quote of the content field in JSON: '", "' or '"}' or '\"'
    import json
    # Let's extract properly
    # Look for the end of the JSON string
    end_idx = text.find('",')
    if end_idx == -1: end_idx = text.find('"}\n')
    if end_idx == -1: end_idx = text.find('"\n')
    csv_raw = text[:end_idx if end_idx != -1 else len(text)]
    # Decode json string escapes
    csv_lines = []
    for line in csv_raw.split('\\n'):
        line = line.replace('\\r', '').replace('\\t', '\t').strip()
        if line:
            csv_lines.append(line)
    
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_recibidos_nov11.csv', 'w', encoding='utf-8') as out:
        out.write('\n'.join(csv_lines))
    print(f"Extracted {len(csv_lines)} lines to datos_recibidos_nov11.csv!")
    print("First line:", csv_lines[0])
    print("Last line:", csv_lines[-1])
else:
    print("Could not find Fecha,C in transcript_full")

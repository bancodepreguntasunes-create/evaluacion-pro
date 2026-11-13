import os

p = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript_full.jsonl'
with open(p, 'rb') as fp:
    content = fp.read()

start_marker = b'V-31644393,ROXANNA'
end_marker = b'V-32555563,YISNEYDY,STEFANY,MEDINA,MARTINEZ,MONAGAS SP T1,Servicio Policial,56742879,95,true,1'

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

print("Start pos:", start_pos)
print("End pos:", end_pos)

if start_pos != -1 and end_pos != -1:
    # Find header before start_pos
    header_pos = content.rfind(b'Fecha,', 0, start_pos)
    full_slice = content[header_pos : end_pos + len(end_marker)]
    text = full_slice.decode('utf-8', errors='ignore')
    text = text.replace('\\r\\n', '\n').replace('\\n', '\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_recibidos_nov11.csv', 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines))
    print(f"Extracted EXACT CSV with {len(lines)} rows!")
    print("Row 0:", lines[0])
    print("Row 1:", lines[1])
    print("Row -1:", lines[-1])
else:
    print("Could not find markers in transcript_full.jsonl, searching chunks...")

p = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\chunks\transcript_full\00000010.jsonl'
with open(p, 'rb') as fp:
    data = fp.read()

idx = data.find(b'Fecha,C')
print('Fecha,C index:', idx)
if idx != -1:
    end_idx = data.find(b'The following is a <SYSTEM_MESSAGE>', idx)
    if end_idx == -1:
        end_idx = data.find(b'</USER_REQUEST>', idx)
    chunk = data[idx:end_idx if end_idx != -1 else len(data)]
    text = chunk.decode('utf-8', errors='ignore')
    text = text.replace('\\r\\n', '\n').replace('\\n', '\n').strip()
    if text.endswith('"'):
        text = text[:-1].strip()
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_recibidos_nov11.csv', 'w', encoding='utf-8') as out:
        out.write(text.strip())
    rows = text.strip().splitlines()
    print('Saved to datos_recibidos_nov11.csv! Rows:', len(rows))
    print('First row:', rows[0])
    print('Last row:', rows[-1])

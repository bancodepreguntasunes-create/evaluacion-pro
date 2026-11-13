import json

p = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript_full.jsonl'
with open(p, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        obj = json.loads(line)
        if obj.get('type') == 'USER_INPUT':
            cnt = obj.get('content', '')
            if 'actualiza los datos con esto' in cnt:
                print("Found target USER_INPUT step!", obj.get('step_index'), "Length:", len(cnt))
                f_idx = cnt.find('Fecha,C')
                if f_idx != -1:
                    csv_text = cnt[f_idx:].strip()
                    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_recibidos_nov11.csv', 'w', encoding='utf-8') as out:
                        out.write(csv_text)
                    print("Saved to datos_recibidos_nov11.csv! Total lines:", len(csv_text.splitlines()))
                    print("First line:", csv_text.splitlines()[0])
                    print("Last line:", csv_text.splitlines()[-1])

import glob
import os

files = glob.glob(r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\**\*.*', recursive=True)
found = False

for f in files:
    if f.endswith('.jsonl') or 'steps' in f:
        try:
            with open(f, 'rb') as fp:
                data = fp.read()
                if b'actualiza los datos con esto' in data:
                    print("Found user prompt in:", f)
                    text = data.decode('utf-8', errors='ignore')
                    f_idx = text.find('Fecha,C')
                    if f_idx != -1:
                        # find where the string ends or closing tag
                        end_candidates = [text.find('</USER_REQUEST>', f_idx), text.find('",', f_idx), text.find('"\n', f_idx)]
                        end_candidates = [x for x in end_candidates if x != -1]
                        end_idx = min(end_candidates) if end_candidates else len(text)
                        csv_text = text[f_idx:end_idx]
                        csv_text = csv_text.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\t', '\t')
                        with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_recibidos_nov11.csv', 'w', encoding='utf-8') as out:
                            out.write(csv_text.strip())
                        print("Saved CSV successfully! Lines:", len(csv_text.strip().splitlines()))
                        found = True
                        break
        except Exception as e:
            pass

if not found:
    print("Could not find in files, checking transcript_full.jsonl directly...")
    p = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript_full.jsonl'
    with open(p, 'rb') as fp:
        data = fp.read()
        f_idx = data.rfind(b'Fecha,C')
        if f_idx != -1:
            print("Found in transcript_full at byte:", f_idx)
            text = data[f_idx:].decode('utf-8', errors='ignore')
            end_idx = text.find('",')
            csv_text = text[:end_idx if end_idx != -1 else len(text)]
            csv_text = csv_text.replace('\\r\\n', '\n').replace('\\n', '\n')
            with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\datos_recibidos_nov11.csv', 'w', encoding='utf-8') as out:
                out.write(csv_text.strip())
            print("Saved from transcript_full! Lines:", len(csv_text.strip().splitlines()))

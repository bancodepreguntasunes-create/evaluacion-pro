import json
import sys

p = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript.jsonl'
with open(p, 'rb') as fp:
    for line_idx, line in enumerate(fp):
        if b'actualiza los datos' in line:
            print(f"Found in line {line_idx+1}")
            try:
                obj = json.loads(line.decode('utf-8'))
                print("Step:", obj.get("step_index"), "truncated:", obj.get("truncated_fields"))
            except Exception as e:
                print("Error parsing json:", e)

p = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript.jsonl'
with open(p, 'rb') as fp:
    lines = fp.readlines()

target_line = lines[1117]
print("Target line length:", len(target_line))
import json
obj = json.loads(target_line.decode('utf-8'))
for k, v in obj.items():
    if k != 'content':
        print(k, ':', v)
    else:
        print('content length:', len(v))
        print('content preview:', repr(v[:100]), '...', repr(v[-100:]))

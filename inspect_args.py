
import json

transcript_path = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript_full.jsonl'

lines = [88, 90, 94, 97, 185]
with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx in lines:
            obj = json.loads(line)
            for tc in obj.get('tool_calls', []):
                args = tc.get('args', {})
                print(f"Line {idx} {tc.get('name')}:")
                for k, v in args.items():
                    print(f"  {k}: {str(v)[:300]}")


import json

transcript_path = r'C:\Users\PC\.gemini\antigravity\brain\5b0b08a9-b938-4fc8-b006-63249b295d73\.system_generated\logs\transcript_full.jsonl'

target_lines = [185, 203, 209, 224, 231]
with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx in target_lines:
            data = json.loads(line)
            print(f'=== LINE {idx} ===')
            content = data.get('content') or ''
            print('Content length:', len(content))
            print(content[:500])
            calls = data.get('tool_calls', [])
            for c in calls:
                print('Tool call:', c.get('name') or c.get('function', {}).get('name'))
                args = c.get('arguments') or c.get('function', {}).get('arguments')
                print('Args:', str(args)[:300])

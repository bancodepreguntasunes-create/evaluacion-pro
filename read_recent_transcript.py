import json

p = 'C:/Users/PC/.gemini/antigravity/brain/5b0b08a9-b938-4fc8-b006-63249b295d73/.system_generated/logs/transcript_full.jsonl'
with open(p, 'r', encoding='utf-8') as f:
    lines = [json.loads(x) for x in f if x.strip()]

for i in range(-5, 0):
    step = lines[i]
    t = step.get('type')
    idx = step.get('step_index')
    cnt = step.get('content', '')
    print(f"Step {idx}, type {t}, len {len(cnt)}")
    if 'Fecha' in cnt:
        print(f"  --> FOUND 'Fecha' in step {idx}!")
        with open('C:/Users/PC/.gemini/antigravity/scratch/unes-sistema/datos_recibidos_nov11.csv', 'w', encoding='utf-8') as out:
            f_idx = cnt.find('Fecha')
            out.write(cnt[f_idx:].strip())
        print("  --> Wrote to datos_recibidos_nov11.csv")

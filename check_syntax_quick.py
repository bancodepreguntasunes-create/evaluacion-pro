# -*- coding: utf-8 -*-
import sys

with open(r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\unes_sistema_final.js", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Let's check for template literals or multi-line strings or unescaped quotes
# Check line by line
in_template = False
in_string = False
string_char = None

for i, line in enumerate(lines):
    # check for obvious syntax anomalies like missing commas or broken statements
    # especially around recent edits
    if i < 20 or i > len(lines) - 50:
        pass
print("Done line check.")

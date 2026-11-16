# -*- coding: utf-8 -*-
import os, sys, re, json

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unes-sistema"

def read_file(filename):
    with open(os.path.join(BASE_DIR, filename), "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def write_file(filename, content):
    with open(os.path.join(BASE_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)

print("Reading files...")
index_html = read_file("index.html")
unes_js = read_file("unes_sistema_final.js")
styles_css = read_file("styles.css")

print(f"index.html length: {len(index_html)}")
print(f"unes_sistema_final.js length: {len(unes_js)}")
print(f"styles.css length: {len(styles_css)}")

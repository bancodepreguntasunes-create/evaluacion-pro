
with open(r'C:\Users\PC\.gemini\antigravity\scratch\unes-sistema\index.html','rb') as f: d=f.read()

db_start = d.find(b'id="view-dashboard"')
map_start = d.find(b'<!-- Mapa Interactivo', db_start)
map_end   = d.find(b'</section>', map_start) + len(b'</section>')

print('db_start:', db_start)
print('map_start:', map_start)
print('map_end:', map_end)

# Show what comes just before map
print(repr(d[map_start-20:map_start+100]))
print('---')
print(repr(d[map_end-60:map_end+100]))

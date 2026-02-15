# -*- coding: utf-8 -*-
import urllib.request
import json

url = "http://localhost:5000/api/tools"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode('utf-8'))

for cat in data['tools']:
    for t in data['tools'][cat]:
        if 'v9' in t['filename'] and 'standalone' in t['filename']:
            print('Found v9 tool:')
            print('  filename:', t['filename'])
            print('  description:', t['description'][:80], '...')

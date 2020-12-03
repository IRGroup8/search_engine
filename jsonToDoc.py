import json

f = open('output.json')

data = json.load(f)

for i in range(0, 1):
    print(data[i])

f.close()
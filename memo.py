import requests
import pprint

def gaStr(action): # get action str // verified
    if action == 0:
        return "lu"
    elif action == 1:
        return "u"
    elif action == 2:
        return "ru"
    elif action == 3:
        return "l"
    elif action == 4:
        return "s"
    elif action == 5:
        return "r"
    elif action == 6:
        return "ld"
    elif action == 7:
        return "d"
    elif action == 8:
        return "rd"

response = requests.get('http://localhost:8000/start') #gets data
print(response.text)
f = response.text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
iv_list = [int(i) for i in f.split()] #listing initial value
num_terns = iv_list[0] #number of terns
Row = iv_list[1] #row of field
Column = iv_list[2]

fa = requests.post('http://localhost:8000/show').text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
la = [int(i) for i in fa.split()]
lf = []
for i in range(Row):
    l = []
    for j in range(Column):
        l.append(la[Row * Column + Column * i + j ])
    lf.append(l)

pprint.pprint(lf)

data = [
  ('usr', 1),
  ('d', gaStr(0)),
]
f = requests.post('http://localhost:8000/judgedirection', data = data).text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
iv_list = [i for i in f.split()]
i = [int(iv_list[0]),int(iv_list[1])]

a = []
if iv_list[2] == "Error":
    a.append([False, 0, "oof", i])
elif iv_list[2] == "is_panel":
    a.append([True, 0, "remove", i])
else:
    a.append([True, 0, "move", i])

print(a)
print(lf[i[0]][i[1]])

import json


with open('data.json', 'r', encoding='utf-8') as f:

    # json.dump(counter, f, ensure_ascii=False, indent=4)

    datas = json.load(f)


myKeys = list(datas.keys())
myKeys.sort()
sorted_dict = {i: datas[i] for i in myKeys}
 
with open('dataKeySorted.json', 'w', encoding='utf-8') as f:

    json.dump(sorted_dict, f, ensure_ascii=False, indent=4)

sorted_value_dict = dict(sorted(datas.items(), key=lambda item: item[1], reverse=True))
with open('dataValueSorted.json', 'w', encoding='utf-8') as f:

    json.dump(sorted_value_dict, f, ensure_ascii=False, indent=4)
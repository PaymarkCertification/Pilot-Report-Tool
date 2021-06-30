import re
import json

def load_json(json_file: str) -> dict:
    with open(json_file) as data:
        return json.load(data)        

r = load_json('Routing.json')

def translate(s: str) -> str:
    def translate_routing(BIN: str, bank: str) -> str:
        s.split(" ")[0]
        return s.split(" ")[1]+ " " + bank

    pos = re.search('\d{6}\s\w', s)
    if pos:
        match_pos = pos.group(0)
        k=r.get(match_pos.split(' ')[0])
        if k is not None:
            return translate_routing(match_pos, k)
        else: 
            return s
    else:
        return s




import pandas as pd
df= pd.DataFrame({'Routing':["308326 I","308443 I", "111111 N", "639491 A"],
                'STAN':[1, 2, 0, 4]
})
df['Routing'] = df['Routing'].apply(translate)
print(df)


# i="308326 i"
# e=re.search('\d{6}\s\w', i)
# print(e)
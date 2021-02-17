import os
path="C:/Users/34588/Desktop/station_name.js"
pathw="C:/Users/34588/Desktop/name.txt"
stationcontent=[]
purestationname=[]
with open(path,encoding='utf-8') as file_obj:
    contents=file_obj.read().strip("")
    stationcontent=contents.split("'")[1]
stationcontentsingle=stationcontent.split('@')[1:]
for item in stationcontentsingle:
    purestationname.append(item.split("|")[1])
print(len(purestationname))
print(purestationname)
with open(pathw,encoding="utf-8",mode="w") as file_w:
    for item in purestationname:
        file_w.write(item)
        file_w.write("\n")
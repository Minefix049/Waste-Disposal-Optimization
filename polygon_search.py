import httpx
import json
import numpy as np


with open('./gaode_api_params.json', 'r') as file:
    input = json.load(file)

for collection in input['collection_centers']:
    polygon = collection['polygon']
    keywords = "小区|家园|家属院|居民区|居民楼"
    url = "https://restapi.amap.com/v3/place/polygon?parameters"
    params = {
        "polygon": polygon,
        "keywords": "小区|家园|家属院|居民区|居民楼",
        "offset": "25",
        "page": "0",
        "key": "5c514a9506919d900868876a446b3518",
    }
    response = httpx.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        collection['keywords'] = keywords
        collection['count'] = data['count']
        print('success!')
    else:
        collection['keywords'] = keywords
        collection['count'] = None
        print('Failed!')

disntance_collection_plant = np.zeros((len(input['collection_centers']),len(input['process_plant_candidate'])))

for i, collection in enumerate(input['collection_centers']):
    for j, process_plant in enumerate(input['process_plant_candidate']):
        origin = collection['center']
        destination = process_plant['center']
        url = "https://restapi.amap.com/v3/direction/driving?parameters"
        params = {
            "origin": origin,
            "destination": destination,
            "strategy" : 13,
            "key": "5c514a9506919d900868876a446b3518",
        }
        response = httpx.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print('haha')
            distance = min([path['distance'] for path in data['route']['paths']])
            disntance_collection_plant[i,j] = distance
            input['disntance_collection_plant'] = disntance_collection_plant.tolist()
            print('success!')
        else:

            print('Failed!')

disntance_plant_landfill = np.zeros((len(input['process_plant_candidate']),len(input['landfill_site_candidate'])))

for i, process_plant in enumerate(input['process_plant_candidate']):
    for j, landfill in enumerate(input['landfill_site_candidate']):
        origin = process_plant['center']
        destination = landfill['center']
        url = "https://restapi.amap.com/v3/direction/driving?parameters"
        params = {
            "origin": origin,
            "destination": destination,
            "strategy" : 13,
            "key": "5c514a9506919d900868876a446b3518",
        }
        response = httpx.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print('haha')
            distance = min([path['distance'] for path in data['route']['paths']])
            disntance_plant_landfill[i,j] = distance
            input['disntance_plant_landfill'] = disntance_collection_plant.tolist()
            print('success!')
        else:

            print('Failed!')


with open('./GIS_data.json','w') as file:
    input = json.dump(input, file,indent=4)


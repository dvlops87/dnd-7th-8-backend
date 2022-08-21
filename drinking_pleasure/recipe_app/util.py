import base64


def preprocessing_recipe_es_data(data_list):
    res = []
    for data in data_list:
        img = data["img"]
        if img:
            img = base64.decodebytes(img).decode('latin_1')

        my_data = {
            "recipe_id": data["recipe_id"],
            "nickname": data["nickname"],
            "recipe_name": data["recipe_name"],
            "img": img,
            "price": data["price"],
            "tag": "",
            "like_cnt": data["like_cnt"],
        }
        res.append(my_data)

    return res


def preprocessing_recipe_data(data):
    data['img'] = base64.decodebytes(data['img']).decode('latin_1')

    for i in range(len(data['main_meterial_list'])):
        img = data['main_meterial_list'][i]['img']
        if img:
            data['main_meterial_list'][i]['img'] = base64.decodebytes(img).decode('latin_1')

    for i in range(len(data['sub_meterial_list'])):
        img = data['sub_meterial_list'][i]['img']
        if img:
            data['sub_meterial_list'][i]['img'] = base64.decodebytes(img).decode('latin_1')

    return data


def preprocessing_list_data(data):
    for i in range(len(data)):
        img = data[i]['img']
        if img:
            data[i]['img'] = base64.decodebytes(img).decode('latin_1')

    return data

import base64


def preprocessing_recipe_es_data(data_list):
    res = []
    for data in data_list:
        img = data["img"]
        if img:
            img = base64.decodebytes(img).decode('latin_1')

        tag_list = []
        try:
            for tag in data["tag_list"]:
                tag_list.append(tag["tag"])
        except:
            pass

        my_data = {
            "recipe_id": data["recipe_id"],
            "nickname": data["nickname"],
            "recipe_name": data["recipe_name"],
            "img": img,
            "price": data["price"],
            "tag": tag_list,
            "like_cnt": data["like_cnt"],
        }
        res.append(my_data)

    return res


def preprocessing_recipe_data(data):
    data['img'] = base64.decodebytes(data['img']).decode('latin_1')
    data['tag'] = data['tag'].split(',')
    data['description'] = data['description'].split('<tr>')

    data['diff_score'] = int(data['diff_score'])
    data['price_score'] = int(data['price_score'])
    data['sweet_score'] = int(data['sweet_score'])
    data['alcohol_score'] = int(data['alcohol_score'])

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
    res = []
    for i in range(len(data)):
        res.append(data[i]['meterial_name'])

    data = {
        "meterial_name": res
    }
    return data

    for i in range(len(data)):
        img = data[i]['img']
        if img:
            data[i]['img'] = base64.decodebytes(img).decode('latin_1')

    return data

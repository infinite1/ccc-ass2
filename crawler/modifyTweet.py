import json

def check(line):
    dict = {}
    user = {}
    check = True

    tweet = json.loads(line)
    # print(tweet)
    if tweet["place"]["country_code"] == "AU" and tweet["lang"] == "en":

        if tweet["coordinates"]:
            dict["coordinates"] = tweet["coordinates"]["coordinates"]
        else:
            longitude = 0
            latitude = 0
            for i in range(4):
                longitude = longitude + tweet["place"]["bounding_box"]["coordinates"][0][i][0]
                latitude = latitude + tweet["place"]["bounding_box"]["coordinates"][0][i][1]
            longitude = round(longitude/4,8)
            latitude = round(latitude/4,8)
            dict["coordinates"] = [longitude, latitude]

        user["id"] = tweet["user"]["id"]
        user["name"] = tweet["user"]["name"]
        user["id_str"] = tweet["user"]["id_str"]
        user["description"] = tweet["user"]["description"]
        dict["created_at"] = tweet["created_at"]
        dict["place"] = tweet["place"]
        dict["user"] = user
        dict["lang"] = tweet["lang"]
        dict["text"] = tweet["text"]
    else:
        check = False

    if check:
        data = json.dumps(dict)
        return data
    else:
        return []

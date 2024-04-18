import smol_json

if __name__ == '__main__':
    # json_str = """
    # {
    #     "name": "Jordie",
    #     "age": 25,
    #     "DOB": "May 29, 1998",
    #     "likesWork": false,
    #     "innerObj": {
    #         "innerObjItem": [
    #             {"whoa": "yeah"},
    #             5,
    #             ["always", {"id": "98a-0ohg"}, {"just-keeps-going": [1.08, false]}]
    #         ]
    #     },
    #     "children": null,
    #     "randomFloat": 897.9,
    #     "randomList": [1, "thing", false, null, true, 1.5]
    # }
    # """
    dict_ = {
        "name": "Jordie",
        "age": 25,
        "DOB": "May 29, 1998",
        "likesWork": False,
        "innerObj": {
            "innerObjItem": [
                {"whoa": "yeah"},
                5,
                ["always", {"id": "98a-0ohg"}, {"just-keeps-going": [1.08, False]}]
            ]
        },
        "children": None,
        "randomFloat": 897.90,
        "randomList": [1, "thing", False, None, True, 1.5]
    }
    res_dict = smol_json.loads('{"hello": "world", "inner": {"age": 25, "innerInner": {"bye": "mars", "boolean": false}}, "float": 5.67}')#, "hobbies": ["games", "drawing", "working out"]}')
    json_str = smol_json.dumps(res_dict)
    print(json_str)

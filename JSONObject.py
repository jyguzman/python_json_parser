from typing import List, Union


class JSONObject:
    def __init__(self, entries: dict = None, level: int = 0, indent: int = 0):
        self.entries = entries
        if self.entries is None:
            self.entries = {}

        self.level = level
        self.indent = indent

    def add(self, key: str, val: Union['JSONObject', 'JSONArray', float, int, str, None]):
        self.entries[key] = val
        return self

    def __repr__(self):
        return str(self.entries).replace("'", "")


class JSONArray:
    def __init__(self, items: List[Union[JSONObject, 'JSONArray', str, float, int, None]] = None):
        self.items = items
        if self.items is None:
            self.items = []

    def add(self, *items: Union[JSONObject, 'JSONArray', str, float, int, None]):
        # for item in items:
        #     if isinstance(item, JSONObject):
        #         self.items += item.entries
        #     elif isinstance(item, JSONArray):
        #         self.items += item.items
        #     else:
        self.items += items
        return self

    def __repr__(self):
        return str(self.items)
        #return '[' + ', '.join([str(item) for item in self.items]) + ']'


if __name__ == "__main__":
    json = (JSONObject()
            .add("name", "Jordie")
            .add("innerDict", JSONObject().add("innerItemKey", "innerItemVal"))
            .add("age", 25)
            .add("list", JSONArray().add(25, "drawing", "clashing")))
    print(str(json))

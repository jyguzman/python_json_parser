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
        self.items += items
        return self

    def __repr__(self):
        return str(self.items)


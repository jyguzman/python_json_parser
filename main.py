import smol_json
import requests
import json

if __name__ == '__main__':
    data = requests.get('https://datausa.io/api/data?drilldowns=Nation&measures=Population')
    regular_json_str = json.dumps(data.json())
    smol_json_str = str(smol_json.loads(data.text))
    assert smol_json_str == regular_json_str


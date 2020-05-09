import json
import argparse

# parse command line arguments
parser = argparse.ArgumentParser("python3 changeToJson.py")
parser.add_argument('filename', help='change result_geo_aus.json to valid json format')
args = parser.parse_args()
filename = args.filename

data = {"docs": []}

with open(filename, "r") as fp:
    lines = fp.readlines()
    for line in lines:
        if line != '\n':
            data["docs"].append(json.loads(line))

with open(filename, 'w') as fp:
    json.dump(data, fp)

print("finish format adjust")
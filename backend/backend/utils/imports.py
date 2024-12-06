import yaml
import json

def import_yaml(yaml_file):
    with open(yaml_file, "r") as stream:
        try:
            config = yaml.safe_load(stream, Loader=yaml.FullLoader)
        except:
            config = yaml.safe_load(stream)
    return config


def import_json(json_file):
    with open(json_file) as stream:
        data = json.load(stream)
    return data

from jsonschema import Draft4Validator
import os.path
import platform
import json


class ConfigParser:
    node_name = ''
    config = {}

    schema = {
        "title": "Config",
        "description": "Configuration for datadog.py",
        "type": "object",
        "properties": {
            "api_key": {
                "description": "API key",
                "type": "string"
            },
            "app_key": {
                "description": "Application Key",
                "type": "string"
            },
            "screenboard": {
                "type": "object",
                "properties": {
                    "width": {
                        "type": "number"
                    },
                    "height": {
                        "type": "number"
                    },
                    "board_title": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "widgets": {
                        "type": "array"
                    },
                    "template_variables": {
                        "type": "array"
                    },
                    "read_only": {
                        "type": "boolean"
                    }
                },
                "required": [
                    "width",
                    "height",
                    "board_title",
                    "description",
                    "widgets",
                    "template_variables",
                    "read_only"
                ]
            },
            "monitors": {
                "type": "array"
            }
        },
        "required": ["api_key", "app_key", "screenboard", "monitors"]
    }

    def __init__(self, file_name):
        self.node_name = platform.node()
        if os.path.isfile(file_name):
            with open(file_name) as f:
                try:
                    self.config = json.load(f)
                except:
                    print ("file " + file_name + " invalid json")
        else:
            raise Exception("file " + file_name + " not found")

    def get_host_name(self):
        return self.node_name

    @property
    def get_config(self):
        conf = Draft4Validator(self.schema)
        if conf.is_valid(self.config):
            return self.config
        else:
            for error in sorted(conf.iter_errors(self.config), key=str):
                print error.message
            return False

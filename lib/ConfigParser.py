import os.path
import platform
import json

class ConfigParser:
    node_name = ''
    config = {}

    _tags = {
        '[[host]]': 'get_host_name',
    }

    def __init__(self, file_name):
        self.node_name = platform.node()

        if os.path.isfile(file_name):
            with open(file_name) as f:
                self.config = json.load(f)
        else:
            raise Exception("file " + file_name + " not found")

    def get_host_name(self):
        """
        Function get host name

        :return: string host name
        """
        return self.node_name

    def get_config(self):
        """
        Function processing config
        :return:
        """
        for _tag, func in self._tags.items():
            i = 0
            while i < len(self.config['monitors']):
                self.config['monitors'][i]['name'] = self.config['monitors'][i]['name'].replace(_tag,
                                                                                                getattr(self, func)())
                self.config['monitors'][i]['query'] = self.config['monitors'][i]['query'].replace(_tag,
                                                                                                  getattr(self, func)())
                self.config['monitors'][i]['message'] = self.config['monitors'][i]['message'].replace(_tag,
                                                                                                      getattr(self,
                                                                                                              func)())
                i += 1

        return self.config

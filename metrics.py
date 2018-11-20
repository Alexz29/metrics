from datadog import initialize, api
import os.path
import platform
import json
import sys


class ConfigParser:
    node_name = ''
    config = {}

    _tags = {
        '{{host}}': 'get_host_name',
    }

    def __init__(self, file_name):
        self.node_name = platform.node()

        if os.path.isfile(file_name):
            with open(file_name) as f:
                self.config = json.load(f)
        else:
            raise Exception("file " + file_name + " not found")

    def get_host_name(self):
        return self.node_name

    def get(self):
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


class Monitors:
    config = {}

    def __init__(self, config):
        self.config = config
        initialize(**{
            'api_key': self.config['api_key'],
            'app_key': self.config["app_key"]
        })

    @staticmethod
    def create_monitor(type, query, message, name, tags, options):
        return api.Monitor.create(type=type, query=query, message=message, name=name, tags=tags, options=options)

    @staticmethod
    def update_monitor(monitor_id, query, message):
        return api.Monitor.update(monitor_id, query=query, message=message)

    @staticmethod
    def is_monitor_isset(name):
        monitors = api.Monitor.get_all()
        flag = False
        for monitor in monitors:
            if monitor['name'] == name:
                flag = monitor['id']
                break
            else:
                flag = False
        return flag

    def delete_monitor(self):
        monitors = api.Monitor.get_all()
        for remote in monitors:
            flag = True
            for local in self.config['monitors']:
                if remote['name'] == local['name']:
                    flag = False

            if flag:
                api.Monitor.delete(remote['id'])
                print remote['name'] + "has been deleted"

    def run(self):
        # before delete monitors
        self.delete_monitor()

        for monitor in self.config['monitors']:
            monitor_id = self.is_monitor_isset(monitor['name'])
            if monitor_id:
                self.update_monitor(monitor_id, monitor['query'], monitor['message'])
                print monitor['name'] + "has been updated"
            else:
                self.create_monitor(
                    monitor['type'],
                    monitor['query'],
                    monitor['message'],
                    monitor['name'],
                    monitor['tags'],
                    monitor['options'])
                print monitor['name'] + "has been created"


if sys.argv[1]:
    cfg = ConfigParser(sys.argv[1])
    instance = Monitors(cfg.get())
    instance.run()
else:
    raise Exception('file path is empty ')

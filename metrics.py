from lib import ConfigParser, Main
from datadog import initialize, api
import sys

if sys.argv[1]:

    instance = ConfigParser(sys.argv[1])
    conf = instance.get_config()

    options = {
        'api_key': conf['api_key'],
        'app_key': conf['app_key']
    }
    initialize(**options)

    monitor_delete_ids = Main.get_ids_for_delete(
        api.Monitor.get_all(name=instance.node_name),
        conf['monitors'],
        'name'
    )

    for monitor_delete_id in monitor_delete_ids:
        api.Monitor.delete(monitor_delete_id)

    for monitor in conf['monitors']:
        monitor_id = Main().isset(api.Monitor.get_all(), monitor['name'], 'name')
        if monitor_id:
            api.Monitor.update(
                monitor_id,
                type=monitor['type'],
                query=monitor['query'],
                message=monitor['message'],
                name=monitor['name'],
                tags=monitor['tags'],
                options=monitor['options'])
        else:
            api.Monitor.create(
                type=monitor['type'],
                query=monitor['query'],
                message=monitor['message'],
                name=monitor['name'],
                tags=monitor['tags'],
                options=monitor['options'])

    screenboard = conf['screenboard']
    screenboard_id = Main().isset(
        api.Screenboard.get_all()['screenboards'],
        screenboard['board_title'],
        'title'
    )

    if screenboard_id:
        api.Screenboard.update(
            screenboard_id,
            board_title=screenboard['board_title'],
            description=screenboard['description'],
            widgets=screenboard['widgets'],
            template_variables=screenboard['template_variables'],
            width=screenboard['width'],
            height=screenboard['height'],
            read_only=screenboard['read_only']
        )
    else:
        api.Screenboard.create(
            board_title=screenboard['board_title'],
            description=screenboard['description'],
            widgets=screenboard['widgets'],
            template_variables=screenboard['template_variables'],
            width=screenboard['width'],
            height=screenboard['height'],
            read_only=screenboard['read_only']
        )

else:
    raise Exception('file path is empty ')

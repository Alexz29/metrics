from lib import ConfigParser, Main
from datadog import initialize, api
import sys

CEND = '\33[0m'
CBLACK = '\33[30m'
CRED = '\33[31m'
CGREEN = '\33[32m'
CYELLOW = '\33[33m'
CBLUE = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE = '\33[36m'
CWHITE = '\33[37m'

if sys.argv[1]:

    instance = ConfigParser(sys.argv[1])
    conf = instance.get_config

    if not conf:
        raise Exception("Wrong config")

    options = {
        'api_key': conf['api_key'],
        'app_key': conf['app_key']
    }
    initialize(**options)

    try:
        monitor_delete_ids = Main.get_ids_for_delete(
            api.Monitor.get_all(name=instance.node_name),
            conf['monitors'],
            'name'
        )
    except:
        raise Exception("Auth problem")

    api.Tag.create(instance.node_name, tags=[conf['group']])

    for monitor_delete_id in monitor_delete_ids:
        api.Monitor.delete(monitor_delete_id)
        print (CGREEN + ">>>Monitor id: " + monitor_delete_id + " has been delet" + CEND)

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
            print (CGREEN + ">>>Monitor " + monitor['name'] + " has been update" + CEND)
        else:
            api.Monitor.create(
                type=monitor['type'],
                query=monitor['query'],
                message=monitor['message'],
                name=monitor['name'],
                tags=monitor['tags'],
                options=monitor['options'])
            print (CGREEN + ">>>Monitor " + monitor['name'] + " has been create" + CEND)

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
        print (CGREEN + ">>>Screenboard " + screenboard['board_title'] + " has been update" + CEND)
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
        print (CGREEN + ">>>Screenboard " + screenboard['board_title'] + " has been create" + CEND)

    print (CBLUE + "DONE ... " + CEND)
else:
    raise Exception('param file path is empty')

This software is necessary for the automatic creation of monitors in DataDog.

Link to documentation in date:
https://docs.datadoghq.com/api/?lang=python#create-a-monitor

To work correctly on the host, you must install the agent:
https://docs.datadoghq.com/agent/?tab=agentv6

And python lib:
https://docs.datadoghq.com/integrations/python/

Widget information:
https://docs.datadoghq.com/graphing/dashboards/widgets/

System requirements:
##Python 2.7


For run
```
python metrics.py datadog.json
```

Param:

```
datadog.json - this is the config file
```


Example of configuration:

```
{
      "type": "metric alert",
      "query": "avg(last_5m):avg:system.cpu.user{host:{{host}}} > 90",
      "message": "We may need to add web hosts if this is consistently high.",
      "name": "metric:system.cpu.user host:{{host}}",  #!IMPORTANT the name need to be unique
      "tags": [
        "app:webserver",
        "cpa"
      ],
      "options": {
        "notify_no_data": true,
        "no_data_timeframe": 20
      }
    },
```


For run all test:
```
python -m unittest discover -s lib -p 'Test*.py'
```

Config:

```
{
  "api_key": "< YOUR API KEY >", // require
  "app_key": "< YOUR APP _KEY >",// require
  
  // screenboard require 
  "screenboard": {   
    "width": 1024, 
    "height": 768,
    "board_title": "MY CUSTOM SCREENBOARD",
    "description": "description",
    "widgets": [< YOUR WIDGETS >],
    "template_variables": [< TEMPLATE VARIABLES >],
    "read_only": false
  },
  
  "monitors": [< YOUR MONITORS >]
}

```
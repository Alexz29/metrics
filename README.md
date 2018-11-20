This software is necessary for the automatic creation of monitors in DataDog.

Link to documentation in date:
https://docs.datadoghq.com/api/?lang=python#create-a-monitor

To work correctly on the host, you must install the agent:
https://docs.datadoghq.com/agent/?tab=agentv6

And python lib:
https://docs.datadoghq.com/integrations/python/

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
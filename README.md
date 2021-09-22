# Nginx Location Manager Utility

## Purpose

This utility is meant to create easy (right now only) proxy locations in any Nginx config that has:

1. One `server` that the config is managing locations for.
2. The beginning of the locations config starts with a line that says: `##### START LOCATIONS CONFIG #####` and ends the locations config with `##### END LOCATIONS CONFIG #####`.

## Import a configuration

We'll be using the default configuration file for Nginx. To instantiate the manager, do:

```python
from NginxLocationManager import NginxLocationManager

mgr = NginxLocationManager()
mgr.parse_locations()
```

## Creating a location
```python
mgr.create_location("/app-1.0.0/")
```

Every Location has four properties:
1. `id` === Location ID in the config.
2. `uri` === URI match for this location.
3. `options` === Options for the Nginx location.
4. `port` === Port used for proxy at this location.

## Deleting a Location

To delete a location with a certain id, use this:
```python
mgr.delete_location(1)
```

## View internal config of manager

To see the Nginx config that would be generated when saving the configuration from the manager, you can use:
```python
mgr.get_internal_config_string()
```

If you just want to see the locations part of the config, you can use:
```python
mgr.get_locations_config_string()
```

## Saving Config to Disk

To save the config the manager has internally to the config file specified when creating the manager, perform:
```python
mgr.save_locations()
```

## Example usage file

Here is a file to start you off:
```python
#!/usr/bin/python3

from NginxLocationManager import NginxLocationManager
from NginxLocationManager.NginxLocationOption import ProxyPassOption, ProxyRedirectOption, SetHeaderOption

mgr = NginxLocationManager()
mgr.parse_locations()

mgr.create_location("/app-v1.1.0/", options=[
    SetHeaderOption('X-Real-IP', '$remote_addr'), 
    SetHeaderOption('X-Forwarded-For', '$http_host'), 
    SetHeaderOption('Host', '$remote_addr'), 
    SetHeaderOption('X-NginX-Proxy', 'true'), 
    ProxyPassOption('http://127.0.0.1:4000/'), 
    ProxyRedirectOption('http://', 'https://')
])

mgr.create_location("/app-v1.2.0/")

print(mgr.get_internal_config_string())
```
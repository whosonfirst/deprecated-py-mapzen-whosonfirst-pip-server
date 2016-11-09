# py-mapzen-whosonfirst-pip-server

Python utilities for working with the go-whosonfirst-pip pip and proxy servers.

## Important

This package has been deprecated. You should use [py-mapzen-whosonfirst-pip](https://github.com/whosonfirst/py-mapzen-whosonfirst-pip) instead.

## Usage

The short version is "too soon". If you're feeling like an adventure:

```
wof_data = "/path/to/whosonfirst-data/data"
pip_server = "/path/to/go-whosonfirst-pip/bin/wof-pip-server"
proxy_config = "/path/to/wof-pip-proxy.json"
placetype = "locality"

pip = mapzen.whosonfirst.pip.server.pip_servers(proxy_config)
print pip.ping_server(placetype)

if pip.is_server_running(placetype):

	pip.stop_server(placetype)

else:

	pip.start_server(placetype, pip_server=pip_server, data=wof_data)
	pip.wait_for_godot([placetype])

print pip.is_server_running(placetype)
print pip.ping_server(placetype)
```

## See also

* https://github.com/whosonfirst/go-whosonfirst-pip/
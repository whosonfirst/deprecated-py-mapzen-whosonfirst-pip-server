# py-mapzen-whosonfirst-pip-proxy

Python utilities for working with the go-whosonfirst-pip proxy servers.

## Usage

The short version is "too soon". If you're feeling 

```
wof_data = "/path/to/whosonfirst-data/data"
pip_server = "/path/to/go-whosonfirst-pip/bin/wof-pip-server"
proxy_config = "/path/to/wof-pip-proxy.json"
placetype = "locality"

p = mapzen.whosonfirst.pip.proxy.server(proxy_config)
print p.ping_server(placetype)

if p.is_server_running(placetype):

	p.stop_server(placetype)

else:

	p.start_server(placetype, pip_server=pip_server, data=wof_data)
	p.wait_for_godot(placetype)

print p.is_server_running(placetype)
print p.ping_server(placetype)
```

## See also

* https://github.com/whosonfirst/go-whosonfirst-pip/
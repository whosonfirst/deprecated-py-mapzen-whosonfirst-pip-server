# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import os
import logging
import json
import subprocess
import tempfile
import signal
import urllib2

class server:

    def __init__(self, cfg, **kwargs):

        fh = open(cfg, 'r')
        data = json.load(fh)
        
        proxy_config = {}

        for cfg in data:
            pt = cfg['Target']
            proxy_config[pt] = cfg

        self.proxy_config = proxy_config

        self.pid_root = kwargs.get("pid_root", tempfile.gettempdir())

    def get_pid_name(self, placetype):

        return "wof-pip-proxy-%s.pid" % placetype

    def get_pid_file(self, placetype):

        fname = self.get_pid_name(placetype)
        return os.path.join(self.pid_root, fname)

    def get_pid(self, placetype):

        pid_file = self.get_pid_file(placetype)

        if not os.path.exists(pid_file):
            return None

        pid_fh = open(pid_file, "r")

        pid = pid_fh.readline()
        pid = int(pid)

        pid_fh.close()

        return pid
        
    def write_pid(self, placetype, pid):

        pid_file = self.get_pid_file(placetype)

        fh = open(pid_file, "w")
        fh.write(str(pid))
        fh.close()

    def is_server_running(self, placetype):

        pid = self.get_pid(placetype)

        if not pid:
            return False

        pid = str(pid)

        # ps h -p ${PID} | wc -l
        
        cmd = [ "ps", "h", "-p", pid ]
        logging.info(" ".join(cmd))

        try:
            out = subprocess.check_output(cmd)
        except Exception, e:
            logging.warning(e)
            return False

        out = out.strip()
        logging.debug(out)

        if not out.startswith(pid):
            return False

        return True

    def start_server(self, placetype, **kwargs):

        pip_server = kwargs.get('pip_server', None)
        data = kwargs.get('data', None)

        if not pip_server:
            raise Exception, "Y U NO pip-server"

        if not data:
            raise Exception, "Y U NO data"

        cfg = self.proxy_config[placetype]

        cmd = [ pip_server, "-cors", "-port", str(cfg['Port']), "-data", data, cfg['Meta'] ]
        logging.debug(cmd)

        proc = subprocess.Popen(cmd)
        pid = proc.pid

        logging.info("start %s pip server with PID %s" % (placetype, pid))

        self.write_pid(placetype, pid)
        return proc

    def stop_server(self, placetype):

        pid_file = self.get_pid_file(placetype)
        pid = self.get_pid(placetype)

        os.kill(pid, signal.SIGKILL)

        if os.path.exists(pid_file):
            os.unlink(pid_file)

        return True

    def ping_server(self, placetype):

        cfg = self.proxy_config[placetype]
        url = "http://localhost:%s" % cfg['Port']

        req = urllib2.Request(url)
        req.get_method = lambda : 'HEAD'

        try:
            urllib2.urlopen(req)
            return True
        except urllib2.HTTPError, e:
            return True
        except Exception, e:
            return False

    # wait for server to respond to a ping, like on startup

    def godot(self, placetype):

        while True:

            pending = False

            if not self.ping_server(placetype):
                logging.info("ping for %s failed, waiting" % placetype)
                pending = True

            if not pending:
                break

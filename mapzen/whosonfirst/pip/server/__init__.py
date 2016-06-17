# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import os
import logging
import json
import subprocess
import tempfile
import signal
import urllib2
import time

class base:

    def __init__(self, cfg, **kwargs):

        fh = open(cfg, 'r')
        data = json.load(fh)
        
        proxy_config = {}

        for cfg in data:
            pt = cfg['Target']
            proxy_config[pt] = cfg

        self.cfg = cfg
        self.proxy_config = proxy_config

class proxy_server(base):

    # PLEASE WRITE ME

    def start_server(self):

        """
        cmd = [ proxy_server, "-host", options.proxy_host, "-port", options.proxy_port, "-config", options.proxy_config ]
        logging.debug(cmd)
        
        proc = subprocess.Popen(cmd)
        """

        return False

class pip_servers(base):

    def __init__(self, cfg, **kwargs):

        base.__init__(self, cfg, **kwargs)

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
        
    def write_pid(self, placetype, pid, **kwargs):

        pid_file = self.get_pid_file(placetype)

        fh = open(pid_file, "w")
        fh.write(str(pid))
        fh.close()

        # PLEASE FIX ME - check kwargs for rules about
        # ownership and permissions on tmp files
        # (20160616/thisisaaronland)

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

        if kwargs.get('sudo', False):

            sudo = [ "sudo", "-u", kwargs["sudo"] ]
            sudo.extend(cmd)

            cmd = sudo

        logging.debug(cmd)

        proc = subprocess.Popen(cmd)
        pid = proc.pid

        logging.info("start %s pip server with PID %s" % (placetype, pid))

        self.write_pid(placetype, pid)
        return proc

    def stop_server(self, placetype, **kwargs):

        pid_file = self.get_pid_file(placetype)
        pid = self.get_pid(placetype)

        if kwargs.get('sudo', False):

            cmd = [ "sudo", "kill", "-9", str(pid) ]
            logging.debug(cmd)

            out = subprocess.check_output(cmd)
            logging.debug(out)

        else:
            os.kill(pid, signal.SIGKILL)

        if os.path.exists(pid_file):
            print "remove %s" % pid_file
            # os.unlink(pid_file)

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

    # wait for one or more servers to respond to a ping, like on startup

    def wait_for_godot(self, placetypes=None):

        if not placetypes:
            placetypes = self.proxy_config.keys()

        while True:

            pending = False

            for pt in placetypes:

                if not self.ping_server(pt):

                    logging.info("ping for %s failed" % pt)
                    pending = True
                    break

            if not pending:
                break

            logging.info("waiting for godot...")
            time.sleep(1)

# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import os
import logging
import json
import subprocess
import tempfile

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
        pid_fh = open(pid_file, "r")

        pid = pid_fh.readline()
        pid = int(pid)

        pid_fh.close()

        return pid
        
    # ps h -p ${PID} | wc -l

    def is_proxy_running(self, placetype):

        pid = str(self.get_pid(placetype))
        
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

    def start_proxy(self, placetype):

        return False

        """
        # because this typically gets invoked as user 'www-data'
        # pid_dirname = "/var/run"

        pid_dirname = tempfile.gettempdir()
        pid_basename = "wof-pip-proxy-%s.pid" % target['Target']

        pid_file = os.path.join(pid_dirname, pid_basename)

        # PID=`cat /var/run/foo.pid`
        # ps h -p ${PID} | wc -l

        cmd = [ pip_server, "-cors", "-port", str(target['Port']), "-data", options.data, target['Meta'] ]
        logging.debug(cmd)

        proc = subprocess.Popen(cmd)
        procs.append(proc)

        pid = proc.pid
        logging.info("start %s pip server with PID %s" % (target['Target'], pid))

        fh = open(pid_file, "w")
        fh.write(str(pid))
        fh.close()
        """

    # stop server

    def stop_proxy(self, placetype):

        return False

    def ping_proxy(self, placetype):

        return False

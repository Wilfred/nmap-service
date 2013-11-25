import os
import json

from flask import Flask, request
import nmap


app = Flask(__name__)


# TODO: UDP too
@app.route("/")
def index():
    return """This is a HTTP endpoint that informs clients if they have a TCP port
open. By default it checks for port 22 (SSH) but you can specify other ports.

For performance reasons, we don't allow querying of multiple ports.
    
"""

def port_is_open(ip, port=22):
    nm = nmap.PortScanner()
    result = nm.scan(hosts=ip, ports=str(port), arguments="-Pn")
    open_tcp_ports = result['scan'].get(ip, {}).get('tcp', {})

    if not open_tcp_ports:
        return False

    port_state = open_tcp_ports.get(port, {}).get('state')
    return port_state == 'open'


@app.route("/ports")
def ports():
    request_ip = request.remote_addr
    return json.dumps({'open_ports': {22: port_is_open(request_ip)}})
    

if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG') == 'y')

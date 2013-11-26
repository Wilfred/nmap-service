import os
import json

from flask import Flask, request, abort, render_template
import nmap


app = Flask(__name__)

if os.path.exists('SECRET'):
    SECRET = open('SECRET', 'r').read()
else:
    SECRET = None

# TODO: UDP too
@app.route("/")
def index():
    if SECRET and request.args.get('secret') != SECRET:
        return "Invalid secret given. You need to pass ?secret=&lt;secret&gt;", 403
        
    return render_template("index.html")


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
    if SECRET and request.args.get('secret') != SECRET:
        return "Invalid secret given. You need to pass ?secret=&lt;secret&gt;", 403
        
    request_ip = request.remote_addr
    port = request.args.get('port', 22)

    try:
        port = int(port)
    except ValueError:
        abort(400)
    
    return json.dumps({'open_ports': {port: port_is_open(request_ip, port)}})
    

if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG') == 'y')

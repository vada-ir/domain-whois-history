# coding: utf-8

from flask import Flask
from flask import request
import sys
import tldextract
import os
import signal
from subprocess32 import Popen, PIPE, TimeoutExpired

######### Bootstrap
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

######### Routes
@app.route('/')
def index():
    return ':)'

@app.route('/plain/<domain>', methods=['GET'])
def plain(domain):
    domain = domain.strip()
    data = whois(domain)

    if not data:
        return ("Couldn't get whois data! :(", 504)

    return (data, 200)

def whois(domain):
    parts = tldextract.extract(domain)

    if(parts.suffix == 'ir'):
        command = "/usr/bin/whois %s | grep -v '^%%'" % domain
    else:
        command = "/usr/bin/whois %s | sed '/>>>/,$d' | sed 's/^[ \t]*//;s/[ \t]*$//'" % domain


    with Popen(command, shell=True, stdout=PIPE, preexec_fn=os.setsid) as process:
        try:
            output = process.communicate(timeout=3)[0]
        except TimeoutExpired:
            os.killpg(process.pid, signal.SIGINT)
            output = process.communicate()[0]

    return output.strip()

########
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8082)

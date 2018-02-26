# coding: utf-8

from flask import Flask
from flask import request
import subprocess as subprocess
import sys
import tldextract

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
        command = "/usr/bin/whois -h 192.168.2.27 %s | grep -v '^%%'" % domain
    else:
        command = "/usr/bin/whois -h 192.168.2.27 %s | sed '/>>>/,$d' | sed 's/^[ \t]*//;s/[ \t]*$//'" % domain

    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to exec command."

    return result.strip()

########
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8082)

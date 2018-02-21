# coding: utf-8
from flask import Flask
from flask import request
import subprocess
import sys
import tldextract

app = Flask(__name__)

@app.route('/')
def index():
    return ':)'

@app.route('/whois/plain/<domain>', methods=['GET'])
def plain(domain):
    domain = domain.strip()
    data = whois(domain)

    return (data, 200)

def whois(domain):
    parts = tldextract.extract(domain)
    if(parts.suffix == 'ir'):
        command = "/usr/bin/whois %s | grep -v '%' | sed '/^$/N;/^\n$/D' | sed '1{/^$/d}' | sed '${/^$/d}'" % domain
    else:
        command = "/usr/bin/whois %s | sed '/>>>/,$d' | sed 's/^[ \t]*//;s/[ \t]*$//'" % domain

    try:
        result = subprocess.check_output([command], shell=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to exec command."

    return result

def get_now():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def my_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

########
if __name__ == '__main__':
    app.run(debug=True)

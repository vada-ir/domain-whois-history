
# Whois?
We needed something to get whois data for our domains, do basic cleanup, process for changes, save the changes and alert in a Telegram channel, and we did it using a simple FLask app, Huginn, ELK and Google Sheets.

# How it works
Domains are listed in a CSV file, list is retrieved periodically (hourly) by a Huginn agent, then processed for any changes in whois output, if any, it will be stored in ELasticsearch through Logstash and also an alert is sent to an specified telegram channel.

# Requirements
- A running instance of [Huginn](https://github.com/huginn/huginn)
- A Telegram bot credential (use [BotFather](https://telegram.me/BotFather) to get one)
- An Online repository of domain data (Google Sheets can be nice, [publish to web](https://support.google.com/docs/answer/37579) as CSV and get the link)
- `whois` installed in server 
- A running ELK (well, mostly Logstash and Elasticsearch)
- Some basic idea about how to find your way in Linux!

# Installation
 1. Clone the repo
 2. Install the Flask app required packages using `pip install -r http-api/requirements.txt`
 3. Import Huginn scenario using provided `json` file
 4. Create necessary credentials in Huginn:
	- `tg_bot_api_key`: your Telegram bot API key
	- `domain_csv_uri`: Google Sheets published URI
	- `tg_domain_alert_channel`: Telegram Channel ID for alerts (with `@`)
	- `http_api_ip_port`: IP:Port of Flask app 
	- `logstash_uri`: Logstash IP, Port and Protocol
 5. Add provided `conf` file to your Logstash instance (it often goes under `/etc/logstash/conf.d/`
 6. Run the Flask app as a system service or some agent like Supervisor
 7. Check Huginn agents execution and emitted events
 8. ???
 9. Profit!


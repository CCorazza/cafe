
all:
	git clone https://github.com/slackhq/python-rtmbot
	cp serge.py python-rtmbot/plugins
	echo "SLACK_TOKEN=" >> python-rtmbot/rtmbot.conf

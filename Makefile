DIR = python-rtmbot

all: $(DIR)/rtmbot.conf $(DIR)/plugins/serge.py $(DIR)/venv

$(DIR):
	git clone https://github.com/slackhq/python-rtmbot $(DIR)

$(DIR)/rtmbot.conf: $(DIR)
	echo "SLACK_TOKEN:" > $(DIR)/rtmbot.conf
	echo "DEBUG: True" >> $(DIR)/rtmbot.conf

$(DIR)/plugins: $(DIR)
	mkdir -p $@

$(DIR)/plugins/serge.py: $(DIR)/plugins
	cp serge.py $(DIR)/plugins

$(DIR)/breaks.json:
	touch $@

$(DIR)/venv:
	virtualenv $(DIR)/venv
	echo "arrow==0.5.4" >> $(DIR)/requirements.txt
	$(DIR)/venv/bin/pip install -r $(DIR)/requirements.txt

clean:
	$(RM) -r $(DIR)

re: clean all

.PHONY: all clean re

PYTHON_SCRIPT_DIR = /usr/share
BASH_SCRIPT_DIR = /usr/local/sbin
VENV_DIR = ./venv
PYTHON_SCRIPT_NAME = mensa.py
BASH_SCRIPT_NAME = mensa
REQUIREMENTS_FILE = requirements.txt
REPO_URL := https://github.com/Jocho-Smith/campo-mensa-script.git
INSTALL_PATH := $(shell pwd)

.PHONY: all install clean

all: install

install: move modify_permissions

clone:
	git clone $(REPO_URL) $(pwd)

move:
	# Create a virtual environment
	python3 -m venv $(VENV_DIR)
	# Activate virtual environment and install dependencies
	. $(VENV_DIR)/bin/activate && pip install -r $(REQUIREMENTS_FILE)
	# Copy python script to sensible location
	cp $(PYTHON_SCRIPT_NAME) $(PYTHON_SCRIPT_DIR)
	# Create bash script
	echo "#!/bin/bash" > $(BASH_SCRIPT_NAME)
	echo "source $(INSTALL_PATH)/venv/bin/activate" >> $(BASH_SCRIPT_NAME)
	echo "python3 $(PYTHON_SCRIPT_DIR)/$(PYTHON_SCRIPT_NAME) X1" >> $(BASH_SCRIPT_NAME)
	chmod +x $(BASH_SCRIPT_NAME)
	# replace the X1
	sed -i 's/X1/$$@/g' $(BASH_SCRIPT_NAME)
	# Move bash script to appropriate location
	mv $(BASH_SCRIPT_NAME) $(BASH_SCRIPT_DIR)

modify_permissions:
	chmod -R 755 $(BASH_SCRIPT_DIR)/$(BASH_SCRIPT_NAME)

clean:
	rm -rf $(VENV_DIR)
	rm $(PYTHON_SCRIPT_DIR)/$(PYTHON_SCRIPT_NAME)
	rm $(BASH_SCRIPT_DIR)/$(BASH_SCRIPT_NAME)

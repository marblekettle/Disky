if [ -d "venv" ]; then
	. venv/bin/activate
else
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

fi
python3 src
package:
	-rm -rf build dist nusenv
	python -m venv nusenv
	. nusenv/Scripts/activate && pip install -r requirements.txt && \
		pip install pyinstaller -U && \
		pyinstaller --onefile nus3express.py --hidden-import cloudmesh-common
	
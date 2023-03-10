# for linux:
(cd lyrical; python -m nuitka --standalone --onefile --include-data-file=literary_resources/*.json=./literary_resources/ --include-data-file=resources/*.gz=./spellchecker/resources/  --enable-plugin=pyqt5 --enable-plugin=anti-bloat lyrical.py)

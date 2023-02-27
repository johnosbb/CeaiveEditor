# Deployment 

## Deployment Options
- To generate requirements => pip install pipreqs then pipreqs /path/to/project
- [Deploying PyQt Applications](https://wiki.python.org/moin/PyQt/Deploying_PyQt_Applications)
- [Build System FBS - requires commercial license](https://build-system.fman.io/pyqt5-tutorial)
- [FBS Deployment Documentation](https://build-system.fman.io/manual/)
- [PPG Appears unmaintained and problematic](https://github.com/runesc/PPG)

## PyInstaller

For QT5 support on Linux we need

```sh
sudo apt install -y qtcreator qtbase5-dev qt5-qmake cmake
```

Up update to the latest

```sh
pip install --upgrade pyinstaller
```

We may need to do

```sh
cp -r ./dist/lyrical/* build/lyrical
```

But I am not sure why this is required

- [Youtube video on Pyinstaller](https://www.youtube.com/watch?v=gI_WXyY-PrA)


### Resolving Issues

If you are getting ModuleNotFoundError: No module named ... errors and you:
- call PyInstaller from a directory other than your main script's directory use relative imports in your script then your executable can have trouble finding the relative imports.

This can be fixed by:

- Calling PyInstaller from the same directory as your main script OR 
- Removing any __init__.py files (empty __init__.py files are not required in Python 3.3+) OR
- Using PyInstaller's paths flag to specify a path to search for imports. E.g. if you are calling PyInstaller from a parent folder to your main script, and your script lives in subfolder, then call PyInstaller as such:

```sh
pyinstaller --paths=subfolder subfolder/script.py.
```

On Windows 11

```sh
python -m PyInstaller lyrical.py
```

On Linux with SpellChecker

```sh
python -m PyInstaller --add-binary="spellchecker/resources/en.json.gz:spellchecker/resources" main.py
```

On Windows 11


```sh
python -m PyInstaller --add-binary="spellchecker/resources/en.json.gz;spellchecker/resources" main.py
```

__Note__: that on windows we use the ; instead of the :

### Issues packaging SpellChecker

- https://stackoverflow.com/questions/46474588/pyinstaller-how-to-include-data-files-from-an-external-package-that-was-install
- https://github.com/barrust/pyspellchecker/issues/64


## Nuitka

- [Home Page](https://www.nuitka.net/)

```sh
conda install libpython-static
```

```sh
pip install nuitka
```


```sh
python3 -m nuitka --follow-imports main.py
python.exe -m nuitka --standalone --onefile --enable-plugin=pyqt5 lyrical.py
```

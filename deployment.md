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


## Nuitka

- [Home Page](https://www.nuitka.net/)

@REM 编译

@echo off
cd src/qt
poetry run nuitka lcufix.py --standalone --windows-disable-console --windows-icon-from-ico=ui/ico.ico --enable-plugin=pyside6 --output-dir=../build --onefile
poetry run nuitka lcufix.py --standalone --windows-disable-console --windows-icon-from-ico=ui/ico.ico --enable-plugin=pyside6 --output-dir=../build 
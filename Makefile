.PHONY: all clean build

all: build

build:
	pyinstaller --onefile --name=linux_looker linux_monitor.py

clean:
	rm -rf build dist linux_looker.spec


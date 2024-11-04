.PHONY: all clean build

all: build

build:
	pyinstaller --onefile --name=my_tool main.py

clean:
	rm -rf build dist my_tool.spec

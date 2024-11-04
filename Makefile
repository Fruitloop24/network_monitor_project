.PHONY: all clean build

all: build run

build:
	# Ensure the virtual environment is activated and dependencies are installed
	python3 -m venv myenv
	. myenv/bin/activate && pip install -r requirements.txt
	# Build the executable with pyinstaller
	. myenv/bin/activate && pyinstaller --onefile --name=linux_looker linux_monitor.py

run:
	# Run the executable after building
	./dist/linux_looker

clean:
	# Clean up build artifacts
	rm -rf build dist linux_looker.spec myenv


.PHONY: build-snap
build-snap:
	cd network_monitor_project && snapcraft

.PHONY: clean
clean:
	cd network_monitor_project && snapcraft clean

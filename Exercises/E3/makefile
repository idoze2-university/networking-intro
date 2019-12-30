
ifndef FILE
FILE=
endif

#PORT=$(strip $(shell lsof -i | grep ':123..'  |sed s/..\*:// | sed -r s/\s?.\(LISTEN\|ESTABLISHED\).*// | head -n 1))
PORT=$(shell cat /tmp/port.txt)
IP=$(strip http://localhost:$(PORT))

run_curl:
	curl '$(IP)/$(FILE)' -H 'Connection: keep-alive'

wget:
	wget $(IP)/$(FILE)
run:
	google-chrome $(IP)/$(FILE)
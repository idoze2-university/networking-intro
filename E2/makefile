LISTEN_ARGS=0
ifndef args
override args=1
endif

REMOTE= hours
SSH_PATH= /usr/bin/ssh
PYTHON_PATH= /usr/bin/python
CLIENT_FILE_NAME= client.py
SERVER_FILE_NAME= server.py
FILE_PATH= /home/idoz/University/Networking/Exercises/E2
CONNECT:= $(SSH_PATH) $(REMOTE)
RUN_CLIENT:= $(PYTHON_PATH) $(FILE_PATH)/$(CLIENT_FILE_NAME)
RUN_SERVER:= $(PYTHON_PATH) $(FILE_PATH)/$(SERVER_FILE_NAME)

copy:
	@/usr/bin/scp $(CLIENT_FILE_NAME) $(REMOTE):$(FILE_PATH)/$(CLIENT_FILE_NAME)

lrun:
	@clear
	@echo 'Running client locally using args...'
	@$(RUN_CLIENT) $(args)

llrun:
	@clear
	@echo 'Running listening client locally...'
	@$(RUN_CLIENT) $(LISTEN_ARGS)

runserver:
	@clear
	@echo 'Running server...'
	@$(RUN_SERVER)


run:
	@clear
	@echo 'Running listening client remotely...'
	@$(CONNECT) $(RUN_CLIENT) $(LISTEN_ARGS)

crun: copy run
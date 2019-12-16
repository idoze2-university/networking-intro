LISTEN_ARGS=0
ifndef args
override args=1
endif
REMOTE= hours
SSH_PATH= /usr/bin/ssh
PYTHON_PATH= /usr/bin/python
FILE_NAME= client.py
FILE_PATH= /home/idoz/University/Networking/Exercises/E2
CONNECT:= $(SSH_PATH) $(REMOTE)
RUN:= $(PYTHON_PATH) $(FILE_PATH)/$(FILE_NAME)

copy:
	@/usr/bin/scp $(FILE_NAME) $(REMOTE):$(FILE_PATH)/$(FILE_NAME)

lrun:
	$(RUN) $(args)

llrun:
	$(RUN) $(LISTEN_ARGS)

run:
	@$(CONNECT) $(RUN) $(LISTEN_ARGS)

crun: copy run
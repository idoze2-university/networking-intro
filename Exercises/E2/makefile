DEF_SERVER_IP= 192.168.1.21
DEF_SERVER_PORT= 12345
DEF_ARGS=1 $(DEF_SERVER_IP) $(DEF_SERVER_PORT)
ifndef args
override args=$(DEF_ARGS)
endif
REMOTE= hours
SSH_PATH= /usr/bin/ssh
PYTHON_PATH= /usr/bin/python
FILE_NAME= client.py
FILE_PATH= /home/idoz/University/Networking/Exercises/E2
CONNECT:= $(SSH_PATH) $(REMOTE)
RUN:= $(PYTHON_PATH) $(FILE_PATH)/$(FILE_NAME) $(args)

copy:
	@/usr/bin/scp $(FILE_NAME) $(REMOTE):

lrun:
	$(RUN)

run:
	@$(CONNECT) $(RUN)

crun: copy run
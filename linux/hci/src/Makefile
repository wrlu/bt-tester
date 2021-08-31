main:main.o socket.o dev_mgmt.o
	gcc -o main main.o socket.o dev_mgmt.o -lbluetooth

.PHONY:clean
clean:
	rm -rf *.o
	rm -rf main

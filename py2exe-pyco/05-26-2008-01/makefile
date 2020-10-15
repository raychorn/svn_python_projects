CFLAGS = -mno-cygwin
CPPFLAGS = -mno-cygwin

all: pycostub.exe pycostub_w.exe

pycostub.exe: pyco.o inflate.o
	$(CC) -mno-cygwin -o $@ $^ -static -lz
	strip $@

pycostub_w.exe: pyco.o inflate.o
	$(CC) -mno-cygwin -mwindows -o $@ $^ -static -lz
	strip $@

clean:
	rm -f pycostub.exe pycostub_w.exe pyco.o inflate.o

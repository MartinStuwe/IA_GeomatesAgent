CC      = gcc  # You can also use clang
FLAGS   = -I /usr/include/box2d/
CFLAGS  = -pedantic -Wall
LDFLAGS = -L /usr/lib/ -lbox2d -shared -fPIC

TARGET  = wrapper.so
SOURCE  = wrapper.c

all:
	$(CC) $(FLAGS) $(CFLAGS) $(LDFLAGS) -o $(TARGET) $(SOURCE)

CC = gcc
CFLAGS = -w -fno-inline-functions -fno-stack-protector

SRC = $(wildcard *.c)
PROG = $(SRC:.c=)

all: $(PROG)
	echo $(SRC) $(PROG)

%:%.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm $(PROG) $(SRC)

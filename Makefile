CC = g++
CFLAGS = -std=c++11
OBJ = mkpage.o
INSTALLDIR = /usr/local/bin

mkpage: $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o bin/mkpage

%.o: %.cpp
	$(CC) $(CFLAGS) -c $<

.PHONY: install
install:
	install bin/mkpage $(INSTALLDIR)

.PHONY: clean
clean:
	rm *.o bin/mkpage

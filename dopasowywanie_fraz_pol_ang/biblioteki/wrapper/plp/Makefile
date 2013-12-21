NAME = plp
CC = gcc
SW = swig
CLP_INCL = /usr/local/clp-1.2/lib/
PYTHON_INCL = /usr/include/python2.5
CLP_LIB = /usr/local/clp-1.2/lib/libclp.so

all: $(NAME).py $(NAME).o $(NAME)_wrap.o _$(NAME).so

$(NAME).py $(NAME)_wrap.c: $(NAME).i  
	$(SW) -python $(NAME).i

$(NAME).o: $(NAME).c
	$(CC) -c -fPIC $(NAME).c -I$(CLP_INCL)

$(NAME)_wrap.o: $(NAME)_wrap.c
	$(CC) -c -fPIC $(NAME)_wrap.c -I$(PYTHON_INCL)

_$(NAME).so: $(NAME).o $(NAME)_wrap.o $(CLP_LIB)
	$(CC) -shared $(NAME).o $(NAME)_wrap.o $(CLP_LIB) -o _$(NAME).so	

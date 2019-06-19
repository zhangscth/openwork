CFLAGS = -fPIC -shared

test: libcomplex.so
	g++ test.cpp -o test -L . -l complex

libcomplex.so:complex.cpp
	g++ complex.cpp $(CFLAGS) -o libcomplex.so

.PHONY: clean

clean:
	rm -rf test libcomplex.so




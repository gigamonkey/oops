all: upload.zip

upload.zip: $(wildcard *.py)
	zip $@ *.py

clean:
	rm -f upload.zip

tidy:
	rm *~

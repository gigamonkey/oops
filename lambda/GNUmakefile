all: upload.zip

upload.zip: $(wildcard *.py)
	rm -f upload.zip
	zip $@ *.py

clean:
	rm -f upload.zip

tidy:
	rm *~

files := oops.py
files += config.json


all: upload.zip



upload.zip: $(files)
	rm -f upload.zip
	zip $@ $(files)

clean:
	rm -f upload.zip

tidy:
	rm *~

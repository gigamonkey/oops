# Where we stash variables we don't want to check into git.
include secrets.make

functions := oops event_dispatcher

files := oops.py
files += config.json

all: upload.zip

create_%: upload.zip
	@echo aws lambda create-function --function-name $* --runtime python3.6 --handler oops.$* --zip-file fileb://$< --role $(aws_role)

update_%: upload.zip
	aws lambda update-function-code --function-name $* --zip-file fileb://$<


upload.zip: $(files)
	rm -f upload.zip
	zip $@ $(files)

clean:
	rm -f upload.zip

tidy:
	rm *~

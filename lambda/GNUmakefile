files := oops.py
files += config.json

functions := oops event_dispatcher

all: upload.zip

create_%: upload.zip
	@echo aws lambda create-function --function-name $* --runtime python3.6 --handler oops.$* --zip-file fileb://$< --role $(AWS_ROLE)

update_%: upload.zip
	aws lambda update-function-code --function-name $* --zip-file fileb://$<


upload.zip: $(files)
	rm -f upload.zip
	zip $@ $(files)

clean:
	rm -f upload.zip

tidy:
	rm *~

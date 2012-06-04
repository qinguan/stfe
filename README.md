STFE
====
### A simple CLI tool for sending a email. 

####usage:
	$ python stfe.py -h
	Usage:     Send the contents of a directory as a MIME message.
		Usage: stfe.py [options]


	Options:
	  -h, --help            show this help message and exit
	  -c CONTEXT, --context=CONTEXT
							Mail the context as the email body.the
							context may be from a given filepath or just a string.
	  -a ATTACHMENT, --attachment=ATTACHMENT
							All the contents of the specified attachments,
							if attachment is a directory, Only the regular files
							in the directory are sent, and we don't recurse to subdirectories.
	  -m SUBJECT, --mainsubject=SUBJECT
							The email subject,default is None.
	  -s SENDER, --sender=SENDER
							The value of the From: header (required)
	  -r RECIPIENT, --recipient=RECIPIENT
							A To: header value.
	  -p PASSWD, --password=PASSWD
							The password for login in sender server.

#### eg: 
	python stfe.py -s ***@126.com -r ***@126.com -p **** -m 'Test' -a directorypathORfilepath -c 'email body'
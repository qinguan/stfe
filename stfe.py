#! /usr/bin/env python
# -*- coding: utf-8 -*-  

'''
a simple CLI tool for sending a email.
'''

import os
import sys
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.message import MIMEMessage
from email.mime.base import MIMEBase
from optparse import OptionParser

def add_attach_file(send_msg,filepath):
    '''
    attach a file to the email.
    '''
    if not os.path.isfile(filepath):
        return send_msg
    ctype,encodeing = mimetypes.guess_type(filepath)
    if ctype is None or encodeing is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/',1)
    
    if maintype == 'text':
        fp = open(filepath,'rb')
        msg = MIMEText(fp.read(),_subtype = subtype)
        fp.close()
    elif maintype == 'image':
        fp = open(filepath,'rb')
        msg = MIMEImage(fp.read(),_subtype = subtype)
    elif maintype == 'audio':
        fp = open(filepath,'rb')
        msg = MIMEAudio(fp.read(),_subtype = subtype)
        fp.close()
    else:
        fp = open(filepath,'rb')
        msg = MIMEBase(fp.read(),_subtype = subtype)
        fp.close()
    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
    send_msg.attach(msg)
    return send_msg

def add_attach_directory(send_msg,directorypath):
    '''
    attach all the files in directorypath to the email.
    '''
    for filename in os.listdir(directorypath):
        path = os.path.join(directorypath,filename)
        send_msg = add_attach_file(send_msg,path)
    return send_msg

def build_email(email_param):
    send_msg = MIMEMultipart()
    send_msg['Subject'] = email_param['Subject']
    send_msg['From'] = email_param['From']
    send_msg['To'] = email_param['To']
    
    context_file = email_param['ContextFile']
    
    if not context_file:
        print 'the email context is blank.'
    elif os.path.isfile(context_file):
        fp = open(context_file,'rb')
        text = MIMEText(fp.read())
        fp.close()
        send_msg.attach(text)
    elif context_file:
        send_msg.attach(MIMEText(context_file))
    else:
        print 'the Context may be not correct.'
        
    if email_param['Attachment']:
        if os.path.isdir(email_param['Attachment']):
            send_msg = add_attach_directory(send_msg,email_param['Attachment'])
        elif os.path.isfile(email_param['Attachment']):
            send_msg = add_attach_file(send_msg,email_param['Attachment'])
            
    return send_msg.as_string()

def get_email_param():
    parser = OptionParser(usage="""\
    Send the contents of a directory as a MIME message.
    Usage: %prog [options]
    """)
    parser.add_option('-c', '--context',
                      type='string', action='store', dest='context',
                      help="""Mail the context as the email body.the 
                      context may be from a given filepath or just a string.""")
    parser.add_option('-a', '--attachment',
                      type='string', action='store',dest='attachment',
                      help="""All the contents of the specified attachments,
                      if attachment is a directory, Only the regular files in 
                      the directory are sent, and we don't recurse to subdirectories.""")
    parser.add_option('-m', '--mainsubject',
                      type='string',action='store',dest='subject',
                      help='The email subject,default is None.')
    parser.add_option('-s', '--sender',
                      type='string', action='store', dest='sender',
                      help='The value of the From: header (required)')
    parser.add_option('-r', '--recipient',
                      type='string', action='append', dest='recipient',
                      help='A To: header value.')
    parser.add_option('-p', '--password',
                      type='string', action='store', dest='passwd',
                      help='The password for login in sender server.')
    opts, args = parser.parse_args()
    if not opts.sender or not opts.recipient or not opts.passwd:
        parser.print_help()
        sys.exit(1)
    
    email_param = {}
    email_param['From']        = opts.sender
    email_param['To']          = ';'.join(opts.recipient)
    email_param['Passwd']      = opts.passwd
    email_param['Subject']     = opts.subject if opts.subject else None #'Test'
    email_param['ContextFile'] = opts.context if opts.context else None #'stfe.py'
    email_param['Attachment']  = opts.attachment if opts.attachment else None  #os.getcwd()
    return email_param

def send_email(email_param):
    send_msg = build_email(email_param)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.'+email_param['From'].split('@')[1]+':25')
        #smtp.connect(':'.join(['smtp.'+send_msg['From'].split('@')[1],'25']))
        smtp.login(email_param['From'],email_param['Passwd'])
        smtp.sendmail(email_param['From'],email_param['To'],send_msg)
        smtp.quit()
        return True
    except:
        print 'failed to send a email.'
        return False
    
def start():
    email_param = get_email_param()
    if send_email(email_param):
        print 'send ok'
    
if __name__ == '__main__':
    start()
    
#test:
import pdb
pdb.set_trace
def test():
    email_param = {}
    email_param['From']        = '****@126.com'
    email_param['To']          = '****@126.com'
    email_param['Passwd']      = '****'
    email_param['Subject']     = 'Test'
    email_param['ContextFile'] = 'stfe.py'
    email_param['Attachment']  = os.getcwd()
    send_email(email_param)
    

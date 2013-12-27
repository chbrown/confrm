#!/usr/bin/env python
# import datetime
import smtplib
import argparse
from email.MIMEText import MIMEText

parser = argparse.ArgumentParser(description='Send email.')
parser.add_argument('--from', help='"From:" header (can be in "First Last <fl@example.com>" format', required=True)
parser.add_argument('--to', help='"To:" header (email address)', required=True)
parser.add_argument('--subject', help='"Subject:" header', required=True)
parser.add_argument('--body', help='Text content of email', required=True)
parser.add_argument('--user', help='Username for SMTPD')
parser.add_argument('--password', help='Password for SMTPD')

args = parser.parse_args()
args = vars(args)

smtp = smtplib.SMTP('localhost', 2525)
# smtp.connect()
smtp.set_debuglevel(1)
# smtp.login(args['user'], args['password'])

mime_message = MIMEText(args['body'], 'plain')
mime_message['Subject'] = args['subject']
mime_message['From'] = args['from']

smtp.sendmail(args['from'], [args['to']], mime_message.as_string())
print 'SMTP sent message'
print '  from %s' % args['from']
print '  to %s' % [args['to']]
print '  body %s' % mime_message.as_string()
smtp.quit()

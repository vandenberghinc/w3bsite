#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils

# the imports.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formatdate

# the email object class.
class Email(object):
	def __init__(self, 
		email=None, # must be first parameter.
		password=None, # must be second parameter.
		smtp_host="smtp.gmail.com", 
		smtp_port=587, 
		use_tls=True,
	):
		self.email = str(email)
		self.password = str(password)
		self.smtp_host = str(smtp_host)
		self.smtp_port = int(smtp_port)
		self.use_tls = bool(use_tls)
		self.smtp = None
	def login(self, timeout=3):

		# try.
		try:
			smtp = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=timeout)
			if self.use_tls:
				smtp.starttls()
			smtp.login(self.email, self.password)
			self.smtp = smtp
		except AttributeError:
			return r3sponse.error("Define the noreply email address & password.")
		except smtplib.SMTPAuthenticationError:
			return r3sponse.error("Failed to log in, provided an incorrect email and password.")
		except OSError as e:
			if "Network is unreachable" in str(e):
				return r3sponse.error("Failed to log in, the network is unreachable. Make sure you provided the correct smtp host & port.")
			else:
				return r3sponse.error(f"Failed to log in, error: {e}.")

		# response.
		return r3sponse.success(f"Successfully logged in to the email [{self.email}].")
	def send(self,
		# the email's subject.
		subject="Subject.",
		# define either html or html_path.
		html=None,
		html_path=None,
		# the email's recipients.
		recipients=[],
		# optional attachments.
		attachments=[],
	):

		# checks.
		if html != None: a=1
		elif html_path == None: 
			return r3sponse.error("Define either parameter [html] or [html_path].")
		else: html = Files.load(html_path)
		if len(recipients) == 0: 
			return r3sponse.error("Define one or multiple recipients")

		# create message.
		try:

			msg = MIMEMultipart('alternative')
			msg['From'] = self.email
			msg["To"] = ", ".join(recipients)
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = subject
			
			# Create the body of the message (a plain-text and an HTML version).
			part1 = MIMEText("", 'plain')
			part2 = MIMEText("""\
				""" + html, 'html')
			msg.attach(part1)
			msg.attach(part2)
			for f in attachments or []:
				with open(f, "rb") as fil:
					part = MIMEApplication(
						fil.read(),
						Name=os.path.basename(f)
					)
				part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
				msg.attach(part)
			self.smtp.sendmail(self.email, recipients, msg.as_string())

			# response.
			return r3sponse.success(f"Succesfully send the email to {recipients}.")
		except:
			return r3sponse.error(f"Failed send the email to {recipients}.")


#
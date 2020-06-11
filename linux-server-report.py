import base64, os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
sender, receiver, password, smtpsrv, port, tls = '','','','','',''

def checkConfig(sender, receiver, password, smtpsrv, port, tls):	
	script_path = os.path.abspath(__file__)
	dir_path = script_path.replace("linux-server-report.py","")
	config = open(dir_path+"config.txt","r")
	for line in config.readlines():
		if "sender(=)" in line:
			sender_conf = line.split("(=)")
			sender = sender_conf[1].replace("\n","")
		elif "password(=)" in line:
			passwd_conf = line.split("(=)")
			b64passwd = passwd_conf[1].replace("\n","")
			b = b64passwd.encode("UTF-8")
			bytes_password = base64.b64decode(b)
			password = bytes_password.decode("UTF-8")
		elif "smtpsrv(=)" in line:
			smtpsrv_conf = line.split("(=)")
			smtpsrv = smtpsrv_conf[1].replace("\n","")
		elif "port(=)" in line:
			port_conf = line.split("(=)")
			port = int(port_conf[1].replace("\n",""))
		elif "receiver(=)" in line:
			receiver_conf = line.split("(=)")
			receiver = receiver_conf[1].replace("\n","")
			receivers = receiver.split(";")
		elif "tls(=)" in line:
			tls_conf = line.split("(=)")
			tls = tls_conf[1].replace("\n","")
		else:
			print("Nothing in config file.")
			exit()
	if all(value != '' for value in [sender, receivers, password, smtpsrv, str(port), tls]):
		print("Configuration is good.")
		sendMail(sender,password, smtpsrv, port, tls,  receivers)
	else:
		print("Error in the config file.")

def sendMail(sender, password, smtpsrv, port, tls, receivers):
	script_path = os.path.abspath(__file__)
	dir_path = script_path.replace("linux-server-report.py","")
	HOSTNAME = os.popen('hostname -f').read().replace("\n","")

	OS_TYPE = os.popen('uname -m').read().replace("\n","")

	os_release = os.popen('cat /etc/os-release | grep PRETTY').read().split('"')
	OS_VERSION = os_release[1]
	try:
		TEMPERATURE = (os.popen('/opt/vc/bin/vcgencmd measure_temp 2> /dev/null').read().split("="))[1]
		if float(TEMPERATURE.replace("'C","")) >= 60:
			TEMPERATURE = """<strong style="color: #ff3300"{}</strong>""".format(TEMPERATURE)
		elif float(TEMPERATURE.replace("'C","")) >= 50:
			TEMPERATURE = """<strong style="color: #E9703E"{}</strong>""".format(TEMPERATURE)
		else: 
			TEMPERATURE = """<strong style="color: #00cc00"{}</strong>""".format(TEMPERATURE)
	except:
		TEMPERATURE = "N/A"
	KERNEL_VERSION = os.popen('uname -r').read().replace("\n","")
	UP_TIME = os.popen('uptime -p').read().replace("\n","")
	CPU_USAGE = os.popen("""grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}'""").read().replace("\n","")
	if float(CPU_USAGE.replace("%","")) >= 60:
		CPU_USAGE = """<strong style="color: #ff3300">{}</strong>""".format(CPU_USAGE)
	elif float(CPU_USAGE.replace("%","")) >= 50:
		CPU_USAGE = """<strong style="color: #E9703E>">{}</strong>""".format(CPU_USAGE)
	else: 
		CPU_USAGE = """<strong style="color: #00cc00">{}</strong>""".format(CPU_USAGE)	






	MEM_USAGE = os.popen("""free | grep Mem | awk '{print $3/$2 * 100.0}'""").read().replace("\n","")+"%"
	if float(MEM_USAGE.replace("%","")) >= 50:
		MEM_USAGE = """<strong style="color: #ff3300">{}</strong>""".format(MEM_USAGE)
	elif float(MEM_USAGE.replace("%","")) >= 30:
		MEM_USAGE = """<strong style="color: #E9703E">{}</strong>""".format(MEM_USAGE)
	else: 
		MEM_USAGE = """<strong style="color: #00cc00">{}</strong>""".format(MEM_USAGE)




	DISK_USAGE = os.popen("""df -h / | tail -1 | awk '{print $5}'""").read().replace("\n","")
	if float(DISK_USAGE.replace("%","")) >= 50:
		DISK_USAGE = """<strong style="color: #ff3300">{}</strong>""".format(DISK_USAGE)
	elif float(DISK_USAGE.replace("%","")) >= 20:
		DISK_USAGE = """<strong style="color: #E9703E">{}</strong>""".format(DISK_USAGE)
	else: 
		DISK_USAGE = """<strong style="color: #00cc00">{}</strong>""".format(DISK_USAGE)




	uptime_average = os.popen('cat /proc/loadavg 2> /dev/null').read().replace("\n","").split(" ")
	LOAD_AVERAGE = uptime_average[2]
	if float(LOAD_AVERAGE) >= 50:
		LOAD_AVERAGE = """<strong style="color: #ff3300">{}</strong>""".format(LOAD_AVERAGE)
	elif float(LOAD_AVERAGE) >= 30:
		LOAD_AVERAGE = """<strong style="color: #E9703E">{}</strong>""".format(LOAD_AVERAGE)
	else: 
		LOAD_AVERAGE = """<strong style="color: #00cc00">{}</strong>""".format(LOAD_AVERAGE)




	running_services = os.popen("""service --status-all 2>&1 | grep -Po '(?<= \[\ \+ \]  ).*' | wc -l""").read().replace("\n","")
	RUN_SRVC = running_services
	stopped_services = os.popen("""service --status-all 2>&1 | grep -Po '(?<= \[\ \- \]  ).*' | wc -l""").read().replace("\n","")
	STP_SRVC = stopped_services
	if int(STP_SRVC) >= 10:
		STP_SRVC = """<strong style="color: #ff3300">{}</strong>""".format(STP_SRVC)
	elif int(STP_SRVC) >= 5:
		STP_SRVC = """<strong style="color: #E9703E">{}</strong>""".format(STP_SRVC)
	else: 
		STP_SRVC = """<strong style="color: #00cc00">{}</strong>""".format(STP_SRVC)

	ALL_SRVC = """<br><br><strong style="color: #ff3300"> DOWN  </strong><br>"""
	for service in (os.popen("""service --status-all 2>&1 | grep -Po '(?<= \[\ \- \]  ).*'""").read()).split("\n"):
		ALL_SRVC += service
		ALL_SRVC += "<br>"
	ALL_SRVC += """<strong style="color: #00cc00">UP  </strong><br>"""
	for service in (os.popen("""service --status-all 2>&1 | grep -Po '(?<= \[\ \+ \]  ).*'""").read()).split("\n"):
		ALL_SRVC += service
		ALL_SRVC += "<br>"
	UPDATE_LIST = "<br>"
	available_update = (os.popen("""apt list --upgradeable 2> /dev/null | sed -n '1!p'""").read()).split("\n")
	for package in available_update:
		package = package.split("/")[0]
		UPDATE_LIST += package
		UPDATE_LIST += "<br>"



	NB_UPDATES = os.popen("""apt list --upgradeable 2> /dev/null | wc -l""").read().replace("\n","")
	if int(NB_UPDATES) >= 5:
		NB_UPDATES = """<strong style="color: #ff3300">{}</strong>""".format(NB_UPDATES)
	elif int(NB_UPDATES) >= 1:
		NB_UPDATES = """<strong style="color: #E9703E">{}</strong>""".format(NB_UPDATES)
	else: 
		NB_UPDATES = """<strong style="color: #00cc00">{}</strong>""".format(NB_UPDATES)
	speedtest = os.popen("speedtest-cli --simple").read().split("\n")
	LATENCY = (speedtest[0].split(":"))[1].replace(" ","")
	if float(LATENCY.replace("ms","")) >= 70:
		LATENCY = """<strong style="color: #ff3300">{}</strong>""".format(LATENCY)
	elif float(LATENCY.replace("ms","")) >= 50:
		LATENCY = """<strong style="color: #E9703E">{}</strong>""".format(LATENCY)
	else: 
		LATENCY = """<strong style="color: #00cc00">{}</strong>""".format(LATENCY)
	DL_SPEED = (speedtest[1].split(":"))[1].replace(" ","")
	UL_SPEED = (speedtest[2].split(":"))[1].replace(" ","")

	body = ""
	with open(dir_path+'templates/report.html', 'r') as template:
		html_code = template.read()
		html_code = html_code.replace("$HOSTNAME",HOSTNAME)
		html_code = html_code.replace("$OS_TYPE",OS_TYPE)
		html_code = html_code.replace("$OS_TYPE",OS_TYPE)
		html_code = html_code.replace("$OS_VERSION",OS_VERSION)
		html_code = html_code.replace("$TEMPERATURE",TEMPERATURE)
		html_code = html_code.replace("$KERNEL_VERSION",KERNEL_VERSION)
		html_code = html_code.replace("$UP_TIME",UP_TIME)
		html_code = html_code.replace("$CPU_USAGE",CPU_USAGE)
		html_code = html_code.replace("$MEM_USAGE",MEM_USAGE)
		html_code = html_code.replace("$DISK_USAGE",DISK_USAGE)
		html_code = html_code.replace("$LOAD_AVERAGE",LOAD_AVERAGE)
		html_code = html_code.replace("$RUN_SRVC",RUN_SRVC)
		html_code = html_code.replace("$STP_SRVC",STP_SRVC)
		html_code = html_code.replace("$ALL_SRVC",ALL_SRVC)
		html_code = html_code.replace("$UPDATE_LIST",UPDATE_LIST)
		html_code = html_code.replace("$NB_UPDATES",NB_UPDATES)
		html_code = html_code.replace("$LATENCY",LATENCY)
		html_code = html_code.replace("$DL_SPEED",DL_SPEED)
		html_code = html_code.replace("$UL_SPEED",UL_SPEED)
	body += html_code.replace("<b>","").replace("</b>","")
	for receiver in receivers:
		print("Sending report email at {}...".format(receiver))
		try:
			smtpserver = smtplib.SMTP(smtpsrv,port)
			msg = MIMEMultipart('HTML')
			msg['Subject'] = 'Healthcheck Report'
			msg['From'] = sender
			msg['To'] = receiver
			msg.attach(MIMEText(body, 'html'))

		except:
			print("Failed to send email.")
			exit()
		try:
			if tls == "yes":
				smtpserver.ehlo()
				smtpserver.starttls()
				smtpserver.login(sender, password)
				smtpserver.sendmail(sender, receiver, msg.as_string())
				print("Email was sent.\n")
			elif tls == "no":
				smtpserver.login(sender, password)
				smtpserver.sendmail(sender, receiver, msg.as_string())
				print("Email was sent.\n")
		except:
			print("An error occurred during authentication with the SMTP server. Check the configuration and try again.")
			exit()

def main():
	checkConfig(sender, receiver, password, smtpsrv, port, tls)
	
main()

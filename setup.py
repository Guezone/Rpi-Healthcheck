import sys, base64, time, os, smtplib,argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mailTester(sender, passwd, smtpsrv, port, tls, receivers):
    script_path = os.path.abspath(__file__)
    dir_path = script_path.replace("setup.py","")
    body = ""
    receivers_email = receivers.split(";")
    with open(dir_path+'templates/test-email.html', 'r') as template:
        body = template.read()
        
    for receiver in receivers_email:
        try:
            print("\nPlease wait. A test message to {} will be sent to test your configuration.\n".format(receiver))
            smtpserver = smtplib.SMTP(smtpsrv,port)
            msg = MIMEMultipart()
            msg['Subject'] = 'HealthCheck-Report - Test email.'
            msg['From'] = sender
            msg['To'] = receiver
            msg.attach(MIMEText(body, 'html'))
        except:
            print("Incorrect configuration. Exit")
            exit()
        try:
            if tls == "yes":
                smtpserver.ehlo()
                smtpserver.starttls()
                smtpserver.login(sender, passwd)
                smtpserver.sendmail(sender, receiver, msg.as_string())
                
            elif tls == "no":
                smtpserver.login(sender, passwd)
                smtpserver.sendmail(sender, receiver, msg.as_string())
            else:
                print("You must specify if you want to use TLS(-tls yes|no). Exit.")
                exit()     

        except:
            print("An error occurred during authentication with the SMTP server. Check the configuration and try again.")
            exit()
    configBuilder(sender, passwd, smtpsrv, port, tls, receivers)
    print("HealthCheck-Report is now ready. Execute healthcheck-report.py now and automate it.")
def configBuilder(sender, passwd, smtpsrv, port, tls, receiver):
    script_path = os.path.abspath(__file__)
    dir_path = script_path.replace("setup.py","")
    enc_pass = (str(base64.b64encode(passwd.encode("UTF-8"))).replace("b'","")).replace("'","")

    conf = open(dir_path+"config.txt","w")

    conf.write("sender(=)"+sender+"\n"+"password(=)"+enc_pass+"\n"+"smtpsrv(=)"+smtpsrv+"\n"+"port(=)"+str(port)+"\n"+"receiver(=)"+receiver+"\n"+"tls(=)"+tls)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sender",nargs=1,required=True,metavar="email-addr",help="set sender email address")
    parser.add_argument("-p",nargs=1,required=True,metavar="your_password",help="set sender SMTP password")
    parser.add_argument("-server",nargs=1,required=True,metavar="smtp_server",help="set SMTP server name")
    parser.add_argument("-port",nargs=1,required=True,metavar="port",help="set SMTP port used by the server", type=int)
    parser.add_argument("-tls",nargs=1,required=True,metavar="yes|no",help="use TLS for SMTP authentication")
    parser.add_argument("-r",nargs=1,required=True,metavar="email-addr1;email-addr2",help="set receivers email address")
    args = parser.parse_args()
    sender = ''.join(args.sender)
    passwd = ''.join(args.p)
    server = ''.join(args.server)
    port = args.port[0]
    tls = ''.join(args.tls)
    receivers = ''.join(args.r)
    mailTester(sender, passwd, server, port, tls, receivers)
main()

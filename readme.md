# Rpi-Healthcheck

Rpi-Healthcheck is a script that allows you to retrieve a certain amount of data on a Raspberry Pi and send an email which reports it. It is also compatible with other Linux distributions (tested on Debian10).

They send the following data in the report by email:
* Hostname
* OS type and version
* Kernel version
* Uptime
* Temperature (°C) inside the Rpi
* Load values (CPU, RAM, disks, load average)
* The number and name of services: inactive, stopped and running
* The number of updates available and the name of upgradable packages
* The flows measured in upload and do

During installation (setup.py), the script writes a configuration file (config.txt) with the information entered on the command line.

**WARNING** : your e-mail credentials (for sending reports) are stored in this file with an encoding. Please run this script on a machine over which you have control and which is protected. No one should be able to read the file created.


**Example of mail sent by Rpi-Healthcheck:**
<p align="center"><a href="url"><img src="https://github.com/Guezone/Rpi-Healthcheck/blob/master/img/mail-1.jpg" height="" width="263" ></a><br><br></p>
<p align="center"><a href="url"><img src="https://github.com/Guezone/Rpi-Healthcheck/blob/master/img/mail-2.jpg" height="" width="263" ></a><br><br></p>
<p align="center"><a href="url"><img src="https://github.com/Guezone/Rpi-Healthcheck/blob/master/img/mail-3.jpg" height="" width="263" ></a><br><br></p>


## Requirements 
Rpi-Healthcheck require **Python 3** (tested with 3.7.3) and **Linux based system** (tested on Raspbian 10 & Debian 10).

    root@host:~/Desktop/# pip3 install speedtest-cli && apt install speedtest-cli

## Configuration
    root@host:~/Desktop/# git clone https://github.com/Guezone/Rpi-Healthcheck && cd Rpi-Healthcheck/
    root@host:~/Desktop/Rpi-Healthcheck# python3 setup.py -h
**Output :** 

      -h, --help            show this help message and exit
      -sender email-addr    set sender email address
      -p your_password      set sender SMTP password
      -server smtp_server   set SMTP server name
      -port port            set SMTP port used by the server
      -tls yes|no           use TLS for SMTP authentication
      -r email-addr1;email-addr2   set receivers email address

----------------
Start a setup script to build your configuration : 

    root@host:~/Desktop/Rpi-Healthcheck# python3 setup.py -sender account@mail.com -p 'mYPASSw0rd' -server smtp.mail.com -port 587 -tls yes -r johndoe@mail.com
    

**Output :** 
Please wait. A test message to johndoe@mail.com will be sent to test your configuration.

Rpi-Healthcheck is now ready. Execute Rpi-Healthcheck.py now and automate it.




## Usage
    
If the script does not find new news in your RSS feed (s), here is the result:
    
    root@host:~/Desktop/Rpi-Healthcheck# python3 Rpi-Healthcheck.py 

**Output :** 
Configuration is good.
Sending report email at johndoe@mail.com...
Email was sent.

   

## Automating
  
You can (and must) automate it periodically with cron for example, in order to check your RSS feeds:

     root@host:~/Desktop/Rpi-Healthcheck# crontab -e
     00 20 * * * python3 /root/Desktop/Rpi-Healthcheck/Rpi-Healthcheck.py (>> /root/Desktop/Rpi-Healthcheck/hc.log 2>&1)


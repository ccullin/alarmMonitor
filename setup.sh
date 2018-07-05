sudo mv *.py /usr/local/src/alarmMonitor  
sudo mv alarmMonitor /etc/init.d


sudo chmod 755 /usr/local/src/alarmMonitor/main.py
sudo chmod 755 /etc/init.d/alarmMonitor
sudo update-rc.d alarmMonitor defaults

# you can start alarmMonitor with "sudo service alarmMonitor start" ore simply reboot
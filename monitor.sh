#!/usr/bin/bash
# Michael MCKibbin 20092733
# Adapted from course provided script.
#
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
MEMORYUSAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
PROCESSES=$(expr $(ps -A | grep -c .) - 1)
HTTPD_STATUS=$(systemctl status $1 | awk 'NR == 3')
HTTPD_UPTIME=$(uptime | awk '{print $3,$4}' | cut -d, -f1)
HTTPD_PROCESSES=$(ps -A | grep -c httpd)
APACHE_PROCESSES=$(ps -A | grep -c apache)
APACHE_PROCESSES_NoGREP=$(ps -ef | grep -v grep | grep -c apache)
HTTP_PORT=$(netstat -tuln | grep -c ":80")
HTTPS_PORT=$(netstat -tuln | grep -c ":443")
AVAILABILITY_ZONE=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
AMI_ID=$(curl -s http://169.254.169.254/latest/meta-data/ami-id)
SECURITY_GROUP=$(curl -s http://169.254.169.254/latest/meta-data/security-groups)
IPV4=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
SSH_PORT=$(netstat -tuln | grep -c ":22")

echo "Instance ID: $INSTANCE_ID"
echo "Memory utilisation: $MEMORYUSAGE"
if [ $HTTPD_PROCESSES -ge 1 ]
then
    echo "Web server is running"
else
    echo "Web server is NOT running"
fi

echo "No of HTTPD processes: $PROCESSES"
echo "HTTPD server status: $HTTPD_STATUS"
echo "HTTPD server uptime: $HTTPD_UPTIME"
echo "No of Apache processes: $APACHE_PROCESSES"
echo "No of Apache processes (No grep): $APACHE_PROCESSES_NoGREP"
echo "No of SSH connections: $SSH_PORT"
echo "No of HTTP connections: $HTTP_PORT"
echo "No of HTTPS connections: $HTTPS_PORT"
echo "Availability zone: $AVAILABILITY_ZONE"
echo "AMI ID: $AMI_ID"
echo "Security group: $SECURITY_GROUP"
echo "Public IPv4: $IPV4"

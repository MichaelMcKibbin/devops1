# DevOps Assignment 1
# Michael McKibbin 20092733
#
# Requires:
# python3 & boto3
#
# AWS CLI credentials are stored in a separate file, (~/.aws/credentials)
#
# AMI:
# Amazon Linux2 AMI image: ami-07761f3ae34c4478d
# Instance type: nano
# Keypair: key6.pem (~/key6.pem)
# Security group ID: sg-0a85d9abc0cd3a1f4 (MyDevOpsSecurityGroup01)
#
# ====================
#
# Problem with metadata display in browser.
# Browser persistently ignores settings and forces connection to HTTPS requiring manual change to HTTP
#
# Tried:
# Browser setup before first use:
# Browser (Firefox) settings changed to prevent automatic redirect from HTTP to HTTPS
# Settings > Privacy & Security (about:preferences#privacy)
# HTTPS-Only Mode > Don’t enable HTTPS-Only Mode
# Restart browser to take effect
#
# Result:
# Works briefly, then problem returns.
#
# Fix:
# Set config parameter 'network.stricttransportsecurity.preloadlist' to false
#
# Result:
# Fix appears to work.
# https://stackoverflow.com/questions/38754131/firefox-redirects-localhost-to-https/52528804#52528804
#
# ====================
#
# References/Sources:
# https://boto3.amazonaws.com/
# https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html
# Some code suggestions & comments from VisualStudio/AmazonQ
#
# Lots of reference to course files/documents/labs/examples
# Lots of reading on stackoverflow, geeksforgeeks, superuser.com, & AWS documentation
#
# ====================
#


import boto3
import time
import webbrowser
import random
import string
import urllib
import os
from cgitb import html
from ipaddress import ip_address
from os import system
from urllib import response
from botocore.exceptions import ClientError
import json

# Part A Core Functionality

# 1. Launch New EC2 Instance
# 2. Configure instance settings
# 3. Set up EC2 website
# Download and install Apache web server
# Create index.html and add content
# Get meta data
# Get image
# copy index.html to local drive
ec2 = boto3.resource("ec2")
try:
    print("\nCreating new EC2 instance\n")

    new_ec2_instance = ec2.create_instances(
        # Amazon Linux2 AMI (check current available AMIs before assignment submission)
        ImageId="ami-07761f3ae34c4478d",
        # How many instances to launch. Min and Max
        MinCount=1,
        MaxCount=1,
        # Instance type (t2.nano)
        InstanceType="t2.nano",
        # Tag the instance
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "DevOps_1"},
                    {"Key": "Owner", "Value": "mmckibbin"},
                ],
            },
        ],
        # MyDevOpsSecurityGroup01 Security group ID
        SecurityGroupIds=["sg-0a85d9abc0cd3a1f4"],
        KeyName="key6",
        UserData="""#!/bin/bash
            yum install httpd -y
            systemctl enable httpd
            systemctl start httpd

            echo "Content-type: text/html"
            echo '<html>' > index.html
            echo '<head>' >> index.html
            echo '<title>DevOps Assignment 1</title>' >> index.html
            echo '</head>' >> index.html
            echo '<body>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:200%;">Assignment 1: DevOps_1</p>' >> index.html   
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">AMI: ' >> index.html
            echo $(curl http://169.254.169.254/latest/meta-data/ami-id) >> index.html
            echo '</p>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">Instance ID: ' >> index.html
            echo $(curl http://169.254.169.254/latest/meta-data/instance-id) >> index.html
            echo '</p>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">Instance Type: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/instance-type) >> index.html
            echo '</p>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">Instance IP: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/public-ipv4) >> index.html
            echo '</p>' >> index.html

            echo '<p style="font-family:Helvetica, sans-serif;">Security Group: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/security-groups) >> index.html
            echo '</p>' >> index.html

            echo '<p style="font-family:Helvetica, sans-serif;">Availability Zone: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/placement/availability-zone-id ) >> index.html
            echo '</p>' >> index.html

            echo '<img src="http://devops.witdemo.net/logo.jpg"> logo.jpg ' >> index.html
            echo '</body>' >> index.html
            echo '</html>' >> index.html

            cp index.html /var/www/html/index.html
        """,
    )

except Exception as e:
    print("Error! \nThe EC2 creation process has encountered an error.\n")
    print(e)
    errorfile = open("error.log", "w")
    errorfile.write(str(e))
    errorfile.close()
    print("See error.log for details.")

else:
    # Print instance ID, type, & state
    print(
        "\nNew EC2 instance created successfully!"
        + "\n[ID: "
        + new_ec2_instance[0].id
        + "]"
        + "\n[Type: "
        + new_ec2_instance[0].instance_type
        + "]"
        +
        #'\n[Region: ' + new_ec2_instance[0].region['Name'] + ']' +
        "\n[Current state: "
        + new_ec2_instance[0].state["Name"]
        + "]"
    )

    # Check instance state every 5 seconds.
    print("\nWaiting for instance to run...")
    while new_ec2_instance[0].state["Name"] != "running":
        time.sleep(5)
        new_ec2_instance[0].reload()

    # Print instance state & public ip address
    print(
        "\n\n[Current state: "
        + new_ec2_instance[0].state["Name"]
        + "]\n"
        + "[Public IP: "
        + new_ec2_instance[0].public_ip_address
        + "]\n"
    )

    # Wait x seconds for webserver to initialise
    print("\n\nAllowing time for web server to initialise...")
    time.sleep(60)
    print("\nOpening webpage at: " + new_ec2_instance[0].public_ip_address)
    print("\n\n")
    ip_address = new_ec2_instance[
        0
    ].public_ip_address  # Set variable to instance public IP
    webbrowser.open(
        "http://" + new_ec2_instance[0].public_ip_address
    )  # Open web browser to instance public IP

    # 6. Monitoring
    # Out of sequence numerically as connection timed out when running later on, after s3 setup (Sections 4 & 5)
try:
    time.sleep(30)  # wait a bit...
    # set keypair permissions for ssh access
    print("\nSet keypair permission")
    system("chmod 400 key6.pem")
    print("\nDone.")
    print("\n")

    # copy monitoring script to instance, run it.
    print("\nCopying monitor.sh to ec2 instance")
    system(
        f"scp -o StrictHostKeyChecking=no -i key6.pem monitor.sh ec2-user@{ip_address}:."
    )
    print("\nDone.")
    print("\n")
    print("\nSet permissions on monitor.sh")
    system(f"ssh -i key6.pem ec2-user@{ip_address} 'chmod 700 monitor.sh'")
    print("\nDone.")
    print("\n")
    print("\nRun monitor.sh (on ec2 instance)")
    system(f"ssh -i key6.pem ec2-user@{ip_address} './monitor.sh'")
    print("\nend of monitoring script")
    print("\n")

    # list files in instance
    print("\nList files in instance" + new_ec2_instance[0].id + "...")
    system(f"ssh -i key6.pem ec2-user@{ip_address} 'ls -l'")
    print("\nDone.")
    print("\n")

except Exception as e:
    print(e)

# 4. Set up S3 bucket and website
#
# Generate 6 character random prefix for bucket name
# Download and display image
# Configure the S3 bucket for static website hosting

# Generate 6 character random prefix for bucket name
random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
bucket_name = random_string + "-mmckibbin"
region = "us-east-1"

# Create S3 client
s3_client = boto3.client("s3", region_name=region)

# Create the S3 bucket
print("Creating new S3 bucket...")
try:
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket {bucket_name} created successfully.")
except ClientError as e:
    print(f"Error creating bucket: {e}")
    exit(1)

# Wait for the bucket to be created
print("\nWaiting for bucket to initialize...")
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(bucket_name)
bucket.wait_until_exists()
print("\nBucket successfully created: " + bucket_name)

# Setting ACLs is not (no longer) supported here,
# so public access block settings need to be disabled
# and a bucket policy is required to allow public access to the contents.
# This bucket access was the most difficult part of the assignment to get working.
#
# I even asked ChatGPT for help on this and it produced the same code I already had.
# The real problem turned out to be an indentation error causing
# the public access block and bucket policy to be skipped.

# Disable block public access settings
try:
    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False,
        },
    )
    print(f"Public access block settings disabled for bucket {bucket_name}.")
except ClientError as e:
    print(f"Error disabling public access block settings: {e}")
    exit(1)

# Set the bucket policy to make the contents publicly readable
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*",
        }
    ],
}

try:
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
    print(f"Bucket policy set to make {bucket_name} publicly accessible.")
except ClientError as e:
    print(f"Error setting bucket policy: {e}")
    exit(1)

# Enable static website hosting
website_configuration = {
    "ErrorDocument": {"Key": "error.html"},
    "IndexDocument": {"Suffix": "index.html"},
}

try:
    s3_client.put_bucket_website(
        Bucket=bucket_name, WebsiteConfiguration=website_configuration
    )
    print(f"Static website hosting enabled for bucket {bucket_name}.")
except ClientError as e:
    print(f"Error configuring bucket for static website hosting: {e}")
    exit(1)

# Upload the index.html file
file_path = "index.html"
if os.path.exists(file_path):
    try:
        s3_client.upload_file(
            file_path, bucket_name, "index.html", ExtraArgs={"ContentType": "text/html"}
        )
        print(f"File {file_path} uploaded as index.html.")
    except ClientError as e:
        print(f"Error uploading {file_path}: {e}")
        exit(1)
else:
    print(f"File {file_path} does not exist.")
    exit(1)

# Download and upload logo image
url = "http://devops.witdemo.net/logo.jpg"
logo_path = "logo.jpg"
urllib.request.urlretrieve(url, logo_path)
print("Downloading logo.jpg from " + url)

# Upload logo.jpg to S3 bucket
print("Uploading logo.jpg to S3 bucket...")
try:
    s3_client.upload_file(
        logo_path, bucket_name, "logo.jpg", ExtraArgs={"ContentType": "image/jpeg"}
    )
    print(f"File {logo_path} uploaded as logo.jpg.")
except ClientError as e:
    print(f"Error uploading {logo_path}: {e}")
    exit(1)

# Open web browser and display S3 bucket website
website_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
print("\nOpening web browser to: " + website_url)
webbrowser.open(website_url)
print(f"Static website URL: {website_url}")

# 5. Write EC2 & S3 URLs to file
try:
    # write EC2 website URL and s3 website URLs to mmckibbin-websites.txt file
    print("\nWriting URLs to file...")
    file = open("mmckibbin-websites.txt", "w")
    file.write(
        "Instance URL: http://"
        + new_ec2_instance[0].public_ip_address
        + "\nS3 Bucket URL: http://"
        + bucket_name
        + ".s3-website-us-east-1.amazonaws.com"
    )
    file.close()
    print("\nURLs written to mmckibbin-websites.txt")
    print("\n")
except Exception as e:
    print(
        "An error occurred while writing URLs to file, check error.log or console for more details."
    )
    print(e)
    errorfile = open("error.log", "w")
    errorfile.write(str(e))
    errorfile.close()
    print("Error file created")
    print("\n")


# cloudwatch alarms
# https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/cw-example-using-alarm-actions.html
#
# CloudWatch alarms setup
#
print("Setting up CloudWatch alarms...")
cloudwatch = boto3.client("cloudwatch")

# CPU utilization greater than 85%
try:
    cloudwatch.put_metric_alarm(
        AlarmName="HighCPUUtilization",
        ComparisonOperator="GreaterThanThreshold",
        EvaluationPeriods=1,
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Period=60,
        Statistic="Average",
        Threshold=85.0,
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:automate:us-east-1:ec2:reboot",
        ],
        AlarmDescription="Alarm if server CPU utilization exceeds 85%",
        Dimensions=[
            {"Name": "InstanceId", "Value": new_ec2_instance[0].id},
        ],
        Unit="Percent",
    )
    print("High CPU utilization alarm created.")
except ClientError as e:
    print(f"Error creating high CPU utilization alarm: {e}")

# CPU utilization less than 30%
try:
    cloudwatch.put_metric_alarm(
        AlarmName="LowCPUUtilization",
        ComparisonOperator="LessThanThreshold",
        EvaluationPeriods=1,
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Period=60,
        Statistic="Average",
        Threshold=30.0,
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:automate:us-east-1:ec2:terminate",
        ],
        AlarmDescription="Alarm if server CPU utilization below 30%",
        Dimensions=[
            {"Name": "InstanceId", "Value": new_ec2_instance[0].id},
        ],
        Unit="Percent",
    )
    print("Low CPU utilization alarm created.")
except ClientError as e:
    print(f"Error creating low CPU utilization alarm: {e}")

try:
    # Describe alarms
    print("\nDescribing alarms...")
    response = cloudwatch.describe_alarms()
    for alarm in response["MetricAlarms"]:
        print(f"Alarm Name: {alarm['AlarmName']}")
        print(f"Alarm Description: {alarm['AlarmDescription']}")
        print(f"Alarm State: {alarm['StateValue']}")
        print(f"Alarm Actions: {alarm['AlarmActions']}")
        print(f"Alarm Comparison: {alarm['ComparisonOperator']}")
        print(f"Evaluation Periods: {alarm['EvaluationPeriods']}")
        print(f"Metric Name: {alarm['MetricName']}")
        print(f"Namespace: {alarm['Namespace']}")
        print(f"Period: {alarm['Period']}")
        print(f"Statistic: {alarm['Statistic']}")
        print(f"Threshold: {alarm['Threshold']}")
        print(f"Unit: {alarm['Unit']}")
        print("\n")
except ClientError as e:
    print(f"Error describing alarms: {e}")

# ask user for 'yes' input to delete the s3 bucket and if the answer is yes, delete the contents and then the bucket.
print("\nWould you like to delete the S3 bucket and its contents? (yes/no)")
user_input = input()
if user_input.lower() == "yes":
    print("\nDeleting S3 bucket and its contents...")
    try:
        # Delete bucket contents
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.all().delete()
        print(f"All objects deleted from {bucket_name}.")

        # Delete the bucket
        bucket.delete()
        print(f"Bucket {bucket_name} deleted successfully.")
    except ClientError as e:
        print(f"Error deleting bucket or its contents: {e}")

# ask user for 'yes' input to delete the ec2 instance.
print("\nWould you like to delete the EC2 instance? (yes/no)")
user_input = input()
if user_input.lower() == "yes":
    print("\nDeleting EC2 instance...")
    try:
        new_ec2_instance[0].terminate()
        # delete cloudwatch alarmsalarms
        print("Deleting Cloudwatch Alarms associated with ec2 instance...")
        cloudwatch.delete_alarms(AlarmNames=["HighCPUUtilization", "LowCPUUtilization"])
        print(f"Alarm HighCPUUtilization deleted successfully.")
        print(f"Alarm LowCPUUtilization deleted successfully.")
        print(f"Instance {new_ec2_instance[0].id} terminated successfully.")
    except ClientError as e:
        print(f"Error terminating instance: {e}")

print("\n\nexiting...")
time.sleep(5)
exit()

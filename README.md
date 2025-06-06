# DevOps Project – EC2 & S3 Automation with Monitoring

**Author:** Michael McKibbin  
**Student ID:** 20092733  
**Course:** DevOps Assignment 1, BSc Computer Science (SETU Waterford)

---

## 📘 Overview

This project automates the deployment of an AWS EC2 instance and S3-hosted static website using Python and Boto3. It installs and configures a web server on EC2, serves dynamic metadata, uploads web content and media to S3, and enables basic monitoring and teardown features.

---

## 🚀 Features

- **EC2 Automation**  
  - Launches a `t2.nano` Amazon Linux 2 instance  
  - Applies tags, security group, key pair, and user data  
  - Installs Apache and dynamically generates an `index.html` using instance metadata  
  - Automatically opens the web server in a browser after provisioning

- **S3 Static Website Hosting**  
  - Generates a unique bucket name, sets access policies  
  - Uploads a pre-built `index.html` and a `logo.jpg` image  
  - Configures static website hosting and opens the S3 site in a browser

- **Monitoring**  
  - Custom Bash script (`monitor.sh`) runs on the EC2 instance to report status, ports, services, and usage  
  - Includes Apache, SSH, HTTP/S, and memory usage diagnostics

- **CloudWatch Integration**  
  - Sets up alarms for high (≥85%) and low (≤30%) CPU utilization  
  - Alarm actions include rebooting or terminating the instance  
  - Describes active CloudWatch alarms for verification

- **Resource Cleanup (Optional)**  
  - Prompts the user to delete the EC2 instance and/or S3 bucket after execution

---

## 🛠️ Tools & Technologies

- **Python 3**  
- **Boto3 (AWS SDK for Python)**  
- **AWS EC2 & S3**  
- **CloudWatch Alarms**  
- **Apache Web Server**  
- **Bash Scripting**  
- **SSH/SCP File Transfer**  

---

## 📁 Files

| File | Description |
|------|-------------|
| `devops_1.py` | Main automation script to launch and configure EC2 & S3 resources. |
| `monitor.sh` | Shell script run remotely on EC2 to monitor system and service status. |
| `key6.pem` | SSH private key used to connect to EC2 instance (not included in repo). |
| `index.html` | Dynamically generated on EC2 and pre-existing for S3 (see script comments). |
| `logo.jpg` | Pulled from a public URL and uploaded to S3 for web display. |
| `mmckibbin-websites.txt` | Stores the URLs of the EC2 and S3 web pages created. |
| `error.log` | Generated automatically if any part of the script fails. |

---

## 🌐 Output URLs

- EC2 Web Server (dynamic metadata): `http://<EC2-IP-Address>`
- S3 Static Website: `http://<bucket-name>.s3-website-us-east-1.amazonaws.com`

---

## 🧠 Lessons Learned

- Challenges with **ACL deprecation** and switching to `PublicAccessBlock` & bucket policies  
- **HTTP vs. HTTPS redirects** in modern browsers and how to bypass them for metadata access  
- Importance of **error handling and logging** during automation and cleanup  
- **AWS permissions** and object ownership nuances with S3 hosting

---

## 📜 License

This project was developed for academic purposes. Feel free to reuse or adapt the code for personal learning with appropriate attribution.

---

**Michael McKibbin**  
AWS Cloud Practitioner | CompTIA Security+ | BSc Computer Science  
[LinkedIn](https://www.linkedin.com/in/michaelkevinmckibbin) | [GitHub](https://github.com/MichaelMcKibbin)


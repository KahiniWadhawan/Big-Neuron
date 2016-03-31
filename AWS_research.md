

AWS Setup and Important Instructions 

Login - for developers - CLI tools and API access 

Instructions for create, find, deploy and terminate an instance: 

1. Login to AWS management console to get started. 
2. Click Amazon EC2 icon 
3. Click launch instance to begin the process. 
4. You will AMI’s already configured machines - choose Linux AMI 
5. choose an Instance type. - leave it the default. 
6. click next - configure instance details.
7. click add storage 
8. click tag instance - but how to make the volume encrypted ?? Free tier subscription allows up to 30gb of SSD
9. setup security group - setup ssh rules to allow access from known IP addresses only. 
10. Always back up your instance by - EBS - “root device type” = EBS, then its backed up. 
11. Initializing instance after launching it may take some time - 2-3 minutes approx. 

***donot forget to terminate it during our experiments to learn it as number of hours are limited. 

Some Important Notes:

1. AWS EC2 provides elastic virtual hardware.
2. It has pre-configured templates known as Amazon Machine Images AMI’s. These AMI templates can include just an operating system like Windows and Linux. 
3. Their computing power can range from small micro powered machines for small jobs to high powered machines. 
4. Security - you can have security groups. Security groups are similar to traditional firewalls.
1. Amazon linux is usually easier to support 
3. Network - VPC one - generally the default 
4. Its good to share key with team members - don’t get into the trouble of creating individual users and user mgmt. 
5.		mv perm file to .ssh/ folder 
6. 		chmod 400 .ssh/perm_file
7. 		ssh -i path-to-key.perm -l c2_user publicIP_ofInstance 
8. for cron job - write crontab file - google up 
9. chef tool - for securing oath access tokens - maintain a file 
10. security group - one security group per team, edit inbound rules, 
11. sudo service httpd start 
12. dos setup - dnsmadeeasy, or buy a domain name instead.  
13. AWS lambda 
14. saving instance state - after some time run from that image - create image. 
15. 	Always back up your instance by - EBS - “root device type” = EBS, then its backed up. 
16. revision history of instances - chef, puppet tools 


Things to dig up more:- 
1. What is our subscription plan - is it Free tier? 
2. where to set EIP ??- elastic ip address - if you want to associate an ip address permanently with your instance. 
3. IAM role?? 
4. Additional charges apply for Cloudwatch - is it covered for us by grant? 
5. Tenancy - which is works for us - dedicated or shared? 
6. What is Virtualization type? - HVM 
7. Different Instance types??  

'Research Done by Kahini Wadhawan'
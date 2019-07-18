Security Group Monitoring
==========================


* Scripts for security group monitoring (run every day using cron or jenkins)
  * get_items_s3.py : Get security group items from AWS account
  *  get_diff_sg.py : Check difference between today and yesterday items
  * monitoring.conf : Configuration for scripts (AWS credentials, DB info, etc)
  * sg_items.sql : DB table schema for store security group items

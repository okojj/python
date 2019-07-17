#!/usr/bin/python3
#########################################################################################
# Purpose:
# Input Params: None
# Usage:        ./
# Author:       OJJ
# Doc. Ref:     http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_security_groups#
#########################################################################################
from __future__ import print_function

import json
import boto3
import MySQLdb
from configparser import ConfigParser
import sys,os,ntpath

script_path=ntpath.dirname(sys.argv[0])
config_path= script_path + "/monitoring.conf"

# load config
if not os.path.exists(config_path):
        print("File not found - " + config_path)
        sys.exit(1)

config = ConfigParser()
config.read(config_path)

# get config
db_host = config.get('db', 'db_host')
db_database = config.get('db', 'db_database')
db_id = config.get('db', 'db_id')
db_pw = config.get('db', 'db_pw')

access_key = config.get('aws', 'access_key')
secret_key = config.get('aws', 'secret_key')

# Explicitly declaring variables here grants them global scope
cidr_block = ""
ip_protpcol = ""
from_port = ""
to_port = ""
from_source = ""


# connect db
db = MySQLdb.connect(host=db_host, user=db_id, passwd=db_pw, db=db_database, charset='utf8')
cursor = db.cursor()

#print("%s,%s,%s,%s,%s,%s,%s" % ("Group-Name", "Group-ID", "In/Out", "Protocol", "Port", "Source/Destination", "Description"))


def insert_item(sg_name,sg_id,direction,protocol,port,ip,desc):

	print("%s,%s,%s,%s,%s,%s,%s" % (sg_name, sg_id, direction, protocol, port, ip, desc) )
	query="INSERT INTO sg_items (date,sg_name,sg_id,direction,protocol,port,ip,description,reg_time) values (CURRENT_DATE(),'%s','%s','%s','%s','%s','%s','%s',now())" % (sg_name,sg_id,direction,protocol,port,ip,desc)
	cursor.execute(query)
	db.commit()

	return True
# end of insert_item()


client = boto3.client(
		's3',
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_key,
)
response = client.list_buckets()

#print(response)

#sys.exit(0)


for bucket in response['Buckets']:
	bucket_name = bucket['Name']
	bucket_date = bucket['CreationDate']

	res = client.get_bucket_location(Bucket=bucket_name)
	region = res['LocationConstraint']

	#res = client.get_bucket_policy_status(Bucket=bucket_name)
	#is_public = res['PolicyStatus']['IsPublic']
	is_public = 'N/A'
	print("Name:%s / Region:%s / isPublic:%s / CreationDate:%s " % (bucket_name,region,is_public,bucket_date) )

	continue



cursor.close()
db.close()

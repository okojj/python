#!/usr/bin/python3

#from __future__ import print_function

import sys
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


def get_diff(date_from, date_to):

	result_list = []

	query="select * from sg_items where date='%s' and (sg_name,sg_id,direction,protocol,port,ip) not in (select sg_name,sg_id,direction,protocol,port,ip from sg_items where date='%s')" % (date_to,date_from)
	cursor.execute(query)
	for row in cursor.fetchall():
		result_list.append(row)

	return result_list
# end of get_diff()


def make_email_body (result_list):
	global mail_body_html

	for item in result_list:
		mail_body_html += "<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (item[0],item[1].strftime('%Y-%m-%d'),item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9].strftime('%Y-%m-%d'))


# end of make_email_body

#################################################################
# main
#################################################################
if len(sys.argv) != 3:
	print( "Usage: %s YYYY-MM-DD YYYY-MM-DD" % sys.argv[0])
	print("e.g.) %s 2019-05-17 2019-05-18" % sys.argv[0])
	sys.exit(1)
else:
	date1 = sys.argv[1]
	date2 = sys.argv[2]

	if len(date1) != 10 or len(date2) != 10:
		print( "Invalid date format - %s / %s" % (date1,date2) )
		sys.exit(1)

# connect db
db = MySQLdb.connect(host=db_host, user=db_id, passwd=db_pw, db="infra",charset='utf8')
cursor = db.cursor()


mail_body_html = "<html>\n<body>"


# items in date1 not in date2
print("* New Item(s) (Items in %s and not in %s)" % (date2,date1))
mail_body_html += "* New Item(s) (Items in %s and not in %s)<br>\n" % (date2,date1)
result_list = get_diff(date1,date2)

mail_body_html += "<table border=1 cellspacing=0 cellpadding=5>\n"
mail_body_html += "<tr bgcolor='#ccffff'><th>No</th><th>Date</th><th>SG Name</th><th>SG ID</th><th>In/Out</th><th>Protocol</th><th>Port</th><th>IPs</th><th>Description</th><th>Reg Date</th></tr>\n"
if len(result_list) > 0:
	make_email_body(result_list)
else:
	mail_body_html += "<tr><td colspan=10 align=center>N/A</td></tr>"

mail_body_html += "</table>\n"
mail_body_html += "<br><br>\n"

# items in date2 not in date1
print("* Removed Item(s) (Items in %s and not in %s)" % (date1,date2))
mail_body_html += "* Removed Item(s) (Items in %s and not in %s)<br>\n" % (date1,date2)
result_list = get_diff(date2,date1)

mail_body_html += "<table border=1 cellspacing=0 cellpadding=5>\n"
mail_body_html += "<tr bgcolor='#ccffff'><th>No</th><th>Date</th><th>SG Name</th><th>SG ID</th><th>In/Out</th><th>Protocol</th><th>Port</th><th>IPs</th><th>Description</th><th>Reg Date</th></tr>\n"
if len(result_list) > 0:
	make_email_body(result_list)
else:
	mail_body_html += "<tr><td colspan=10 align=center>N/A</td></tr>"
mail_body_html += "</table>\n"
mail_body_html += "</body>"
mail_body_html += "</html>"

cursor.close()
db.close()


# write email to file
file = "/tmp/sg_diff_email.html"
f = open(file, "w")
f.write(mail_body_html)
f.close()
#print( mail_body_html)



# coding=utf-8
# auth: zhangyiling

"""
import MySQLdb
import commands

db = MySQLdb.connect("192.168.10.191", "cmdb", "65daigou@ezbuy", "cmdb")
#  mysql -h192.168.10.191 -u'cmdb' -p  # p-hsg-ops-3
cursor = db.cursor()
cursor.execute("select DISTINCT name from asset_goservices where ports is NULL")
for i in cursor.fetchall():
    i = ''.join(i)
    s, r = commands.getstatusoutput(
        "sudo netstat -lntup | grep `sudo supervisorctl pid %s` | awk -F: '{print $4}' " % (i))
    try:
        if int(r):
            print i, r
            sql = "update asset_goservices set ports='%s' where name='%s';" % (r.strip(), i)
            print sql
            cursor.execute(sql)
            db.commit()
    except Exception, e:
        pass
db.close()
"""
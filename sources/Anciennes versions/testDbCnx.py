import os, sys, MySQLdb
# Connexions to DB
db1 = MySQLdb.connect("localhost", "AxwayautomatorMS", "AxwayautomatorMS", "axwayautomator_ms")
cursor1 = db1.cursor()

db2 = MySQLdb.connect("localhost", "AxwayautomatorMS", "AxwayautomatorMS", "axwayautomator_ms")
cursor2 = db2.cursor()
# Default values
default_queue="queue_wnt"
default_user="vtom"
default_cal = "tljo"
default_host="localhost"

def selectData (tname, idkey, value, idkeyvalue):
	query = """SELECT %s FROM %s WHERE %s=\"%s\" """ %(value, tname, idkey, idkeyvalue)
	#query = """SELECT V_VALUE FROM ie_var WHERE ID_KEY = \"VA0000030352\" """  # %(column2, tname, column1, value)
	lines = cursor1.execute(query)
	data = cursor1.fetchone()
	if data == None: 
		data = "None"
	else: 
		data = data[0]
	print data
	return data

if __name__ == "__main__":
	query = """SELECT ID_KEY, V_ENAME, T1_PSTART, T2_PEND, ID_PLNG, ID_USER, ID_AGENT FROM to_env"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	dic_env = {}
	for d in data:
		print "Data = \n", d
		(env_id, env_name, d_hmin, d_hmax, idplng, iduser, idhost) = d
		dic_env[env_id]= (env_name, d_hmin, d_hmax)
		# get real value from ie_var table
		if iduser[0:2] == "VA":
			iduser = selectData("ie_var", "ID_KEY", "V_VALUE", iduser)
		if idhost[0:2] == "VA":
			idhost = selectData("ie_var", "ID_KEY", "V_VALUE", idhost)
		if idplng[0:2] == "VA":
			idplng = selectData("ie_var", "ID_KEY", "V_VALUE", idplng)
		
		# get the name from the right table
		if iduser == "None": user = default_user
		else: user  = selectData("cf_user", "ID_KEY", "V_UNAME", iduser)
		if idhost == "None": host = default_host
		else:  host  = selectData("cf_agt", "ID_KEY", "M_HNAME", idhost)
		if idplng == "None": cal = default_cal
		else : 
			idcal = selectData("cf_plng", "ID_KEY", "ID_CAL", idplng)
			if idcal == "None": cal = default_cal 
			else: cal   = selectData("cf_cal", "ID_KEY", "V_CNAME", idcal)
		# Creation de l'environnement
		cmd = "vtaddenv /Name=%s /Calendar=%s/2015 /User=%s /HostGroup=%s /Queue=%s /Profile=Tom_prf" % (env_name, cal, user, host, default_queue) 
		print "%s \n" % cmd
	db1.close()
	db2.close()
	print dic_env
import os, sys, MySQLdb
import exceptions
import traceback
import ConfigParser
from myTools import *
from subprocess import Popen

config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths, file & database infos
fname            = ''.join( (sys.argv[0]).split('.')[:-1] )
server_name      = config.get('DATABASE', 'db_server') 
database_name    = config.get('DATABASE', 'db_name')
db_username      = config.get('DATABASE', 'db_user')
db_password      = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs        = config.get('PATHS', 'p_logs')
path_trace       = config.get('PATHS', 'p_trace')

fvtcmd           = os.path.join(path_res ,  "%s.cmd"%fname)

# Default values
default_queue    = config.get('REF', 'default_queue')
typequeue        = config.get('REF', 'typequeue')
queue            = config.get('REF', 'queue')
default_user     = config.get('REF', 'default_user')
default_cal      = config.get('REF', 'default_cal')
default_host     = config.get('REF', 'default_host')
default_app      = config.get('REF', 'default_app')


# Connexions to DB
db1 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor1 = db1.cursor()

db2 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor2 = db2.cursor()

# Fn Logs 
def myprint(s):
	flog.write("%s\n" % s)
	print "%s" % s

def myprinterr(s):
        flog.write("%s\n" % s)
        err("%s" % s)

def myprintcorr(s):
        fcor.write("%s\n" % s)
        warn("%s" % s)

def logappDef(s):
	flog.write("\t\tINAPP: %s\n"%s)

def logjobDef(s):
	flog.write("\t\t\t\t%s\n"%s)
	
def envSansApp (id_env):
	query = """SELECT * FROM to_obj_app WHERE ID_ENV=\"%s\" """ %(id_env)
	#query = """SELECT V_VALUE FROM to_var WHERE ID_KEY = \"VA0000030352\" """  # %(column2, tname, column1, value)
	lines = cursor1.execute(query)
	data = cursor1.fetchone()
	if data == None: 
		return True
	else:
		return False

def selectData (tname, idkey, value, idkeyvalue):
	query = """SELECT %s FROM %s WHERE %s=\"%s\" """ %(value, tname, idkey, idkeyvalue)
	#query = """SELECT V_VALUE FROM to_var WHERE ID_KEY = \"VA0000030352\" """  # %(column2, tname, column1, value)
	lines = cursor1.execute(query)
	data = cursor1.fetchone()
	if data == None: 
		data = "None"
	else: 
		data = data[0]
	#print data
	return data

if __name__ == "__main__":
	query = """SELECT ID_KEY, V_ENAME FROM to_env"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	dic_env = {}
	i = 0
	l = 0
	nb = 0
	Liste_elem_vu = []
	Liste_dates_vues = []
	print "--------------- Checking if each environment contains at least one application ---------------\n"
	#-----------------------------------------------------------------------------------------------------------------------
	corr_cpt = 0  # a mettre avant la boucle for
	fcorname       = "correspondances"    # a mettre avant la boucle for
	fcorrtab       = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	
	corrTab        = getTab(fcorrtab)
	corrTab["job"] = []    # a mettre avant la boucle for
	lvtom_envnames = getListVTnames("env", corrTab)
	#-----------------------------------------------------------------------------------------------------------------------
	# Creation de fichiers pour contenir les informations.
	fname = os.path.normpath("%s\Env_sans_app.txt" % path_logs)
	f = open(fname, "w")
	fres = os.path.normpath("%s\Env_need_app.cmd" % path_res)
	fres = open(fres, "w")
	
	for d in data:
		nb += 1
		(env_id, env_name) = d
		env_name = getVTname (env_name, corrTab, 'env')
		if(envSansApp(env_id)==True):
			print "environnement sans app: %s\n" % env_name
			f.write("%s\n" % (env_name))
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"application par defaut pour l'environnement\"\n" % (env_name, env_name))
		else:
			print "--------- environnement avec app: %s -----------\n" % env_name
	print "Number of elements processed: %s\n" % nb
	db1.close()
	db2.close()
	cursor1.close()
	cursor2.close()
	savetab(corrTab, "%s_tab.txt"%fcorname)      # a mettre en fin de script
	saveTabinDB(corrTab,"%s_tab.db"%fcorname)    # a mettre en fin de script
	f.close()
	fres.close()
	print "------------ End of processing for environments ------------\n"
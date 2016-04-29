import os, sys, MySQLdb
import exceptions
import traceback
import ConfigParser
from myTools import *
from subprocess import Popen

config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths, file & database infos
#fname            = ''.join( (sys.argv[0]).split('.')[:-1] )

server_name      = config.get('DATABASE', 'db_server') 
database_name    = config.get('DATABASE', 'db_name')
db_username      = config.get('DATABASE', 'db_user')
db_password      = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs        = config.get('PATHS', 'p_logs')
path_trace       = config.get('PATHS', 'p_trace')
fname            = os.path.normpath("%s\Crea_env" % path_res)
fvtcmd           = os.path.join(path_res ,  "%s.cmd"%fname)

# Default values
default_queue    = config.get('REF', 'default_queue')
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
	query = """SELECT ID_KEY, V_ENAME, T1_PSTART, T2_PEND, ID_PLNG, ID_USER, ID_AGENT FROM to_env"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	dic_env = {}
	nb = 0
	# get the number of rows in the resultset
	numrows = int(cursor2.rowcount)
	Liste_elem_vu = []
	Liste_dates_vues = []
	print "--------------- Processing of environments ---------------\n"
	#-----------------------------------------------------------------------------------------------------------------------
	corr_cpt = 0  # a mettre avant la boucle for
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab          = getTab(fcorrtab)
	corrTab["env"] = []    # a mettre avant la boucle for
	
	lvtom_ressnames  = getListVTnames("ressources", corrTab)
	lvtom_hostnames  = getListVTnames("agt", corrTab)
	lvtom_usrnames   = getListVTnames("usr", corrTab)
	lvtom_calnames   = getListVTnames("cal", corrTab)
	#-----------------------------------------------------------------------------------------------------------------------
	# Creation de fichiers pour contenir les informations.
	#fname = os.path.normpath("%s\Crea_env.cmd" % path_res)
	f = open(fvtcmd, "w")
	fname2 = os.path.normpath("%s\env_16char.txt" % path_logs)
	f2 = open(fname2, "w")
	fname3 = os.path.normpath("%s\EnvAvecProblemesUsers.txt" % path_logs)
	f3 = open(fname3, "w")
	fname4 = os.path.normpath("%s\Log_env" % path_trace)
	flog = open(fname4, "w")
	
	for d in data:
		nb += 1
		if (nb == numrows/10):
			print "10% processed"
		if (nb == numrows/4):
			print "25% processed"
		if (nb == numrows*4/10):
			print "40% processed"
		if (nb == numrows/2):
			print "50% processed"
		if (nb == numrows*6/10):
			print "60% processed"
		if (nb == numrows*3/4):
			print "75% processed"
		if (nb == numrows*9/10):
			print "90% processed"
		if (nb == numrows):
			print "100% processed"
		typequeue = 0 # By default, the queue will be unknown if it is not defined
		#print "Data = \n", d
		(env_id, env_name, d_hmin, d_hmax, idplng, iduser, idhost) = d
		dic_env[env_id]= (env_name, d_hmin, d_hmax)
		# get real value from to_var table
		if iduser[0:2] == "VA":
			iduser = selectData("to_var", "ID_KEY", "V_VALUE", iduser)
		if idhost[0:2] == "VA":
			idhost = selectData("to_var", "ID_KEY", "V_VALUE", idhost)
		if idplng[0:2] == "VA":
			idplng = selectData("to_var", "ID_KEY", "V_VALUE", idplng)
		
		# get the name from the right table
		if iduser == "None": user = default_user
		else: user  = selectData("cf_user", "ID_KEY", "V_UNAME", iduser)
		if idhost == "None": host = default_host
		else:  host  = selectData("cf_agt", "ID_KEY", "M_HNAME", idhost)

		if host == default_host: queue = default_queue
		else: typequeue = selectData("cf_agt", "ID_KEY", "V_SYSTYPE", idhost)
		if typequeue == 0: queue = "queue_unknown"
		if typequeue == 1: queue = "queue_wnt"
		if typequeue == 2: queue = "queue_as400"
		if typequeue == 20: queue = "queue_gcos7"
		if typequeue == 21: queue = "queue_gcos8"
		if typequeue == 25: queue = "queue_mvs"
		if typequeue == 4 or typequeue == 5 or typequeue == 6 or typequeue == 8 or typequeue == 10: queue = "queue_ksh"
		
		if idplng == "None": cal = default_cal
		else : 
			idcal = selectData("cf_plng", "ID_KEY", "ID_CAL", idplng)
			if idcal == "None": cal = default_cal
			else: cal   = selectData("cf_cal", "ID_KEY", "V_CNAME", idcal)
		
		# Changement des valeurs pour qu'elles soient adaptees a vtom
		if ("*" in user):
			user = user.replace("*", "")
		if("\\" in user):
			f3.write("%s ---> Agent associe : %s\n  l'environnement ci-dessus est: %s\n\n" % (user, host, env_name))
			user = user.split('\\')[2]
	
		# 16 char problems		
		if len(env_name) > 16:
			f2.write("Nom de l'env depasse 16 char : %s\n" % env_name)
		if env_name in Liste_elem_vu :
			if len(env_name)>= 16: #retirer ce if d'ici et mettre en dessous un if a la place
				f2.write(" /!\\ Environnement vu en double: %s\n" % app_name)
		if len(user) > 16:
			f3.write("Le user: '%s' depasse 16 caracteres il a donc ete tronque\n" % user)
			user = getVTname (user, corrTab, 'usr')
		if len(cal) > 16:
			f2.write("Le calendrier: '%s' depasse 16 caracteres il a donc ete tronque\n" % cal)
			cal = getVTname (cal, corrTab, 'cal')
		if len(host) > 16:
			f2.write("L'agent: '%s' depasse 16 caracteres il a donc ete tronque\n" % host)
			host = getVTname (host, corrTab, 'agt')
		# Env_name = 16 char ou moins
		if len(env_name) > 16:
			env_name = getVTname (env_name, corrTab, 'env')

		#-------------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM -----------------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.
		automator_envname = env_name
		lvtenvs = getListVTnames("env", corrTab)
		(vtom_envname, isnum) = formatObjName(automator_envname, corr_cpt, lvtenvs)
		if ((vtom_envname != automator_envname) and isnum):
			corr_cpt += 1
			corr = (automator_envname, vtom_envname)
			corrTab["env"].append(corr)
		elif ((vtom_envname != automator_envname) and not isnum): 
			corr = (automator_envname, vtom_envname)
			corrTab["env"].append(corr)

		#---------------------------------------------------------------------------------------

		# Creation variable date
		Id_Date = "d_"+vtom_envname[:14]
		if Id_Date in Liste_dates_vues :
			if len(Id_Date)>= 16:
				Id_Date = Id_Date[0:16]
		# Creation de l'environnement
		f.write("vtaddenv /Name=%s /Date=%s /Calendar=%s/2015 /User=%s /Host=%s /Queue=%s /Profile=TOM_prf\n" % (vtom_envname, Id_Date, cal, user, host, queue))
		Liste_elem_vu.append(env_name)
		Liste_dates_vues.append(Id_Date)
	print "Number of elements processed: %s\n" % nb
	db1.close()
	db2.close()
	cursor1.close()
	cursor2.close()
	savetab(corrTab, "%s_tab.txt"%fcorname)      # a mettre en fin de script
	saveTabinDB(corrTab,"%s_tab.db"%fcorname)    # a mettre en fin de script
	f.close()
	f2.close()
	f3.close()
	#exit(0)
	try :
		execVtomCmd(fvtcmd, flog)
	except IOError, ioe:
		myprinterr("****** Read File Error ******\n%s\n%s\n"%(ioe, traceback.extract_tb(sys.exc_traceback)))
		exit(1)
	except Exception, e:
		myprinterr("****** Error ******\n%s\n%s\n"% (e, traceback.extract_tb(sys.exc_traceback)))  
		exit(1)
	except VTCmdException:
		myprint("# -- CMD file : %s " %fvtcmd)
                myprinterr("Migration aborded\n%s"%(traceback.extract_tb(sys.exc_traceback)))
                exit(1)
	flog.close()
	print "------------ End of processing for environments ------------\n"
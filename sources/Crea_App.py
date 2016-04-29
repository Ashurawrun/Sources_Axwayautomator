#VERIFIER LES CAS OU ON A PLUSIEURS DOUBLONS DE MOINS DE 16 CHAR
#LA TABLE DE CORRESPONDANCE A UN SOUCIS
import os, sys, MySQLdb
import ConfigParser
from subprocess import Popen
from myTools import *


config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths, file & database infos
#fname              = ''.join( (sys.argv[0]).split('.')[:-1] )
server_name        = config.get('DATABASE', 'db_server') 
database_name      = config.get('DATABASE', 'db_name')
db_username        = config.get('DATABASE', 'db_user')
db_password        = config.get('DATABASE', 'db_pass') 
path_res           = config.get('PATHS', 'p_reslt')  
path_tmp           = config.get('PATHS', 'p_tmp')
path_logs          = config.get('PATHS', 'p_logs')
path_trace         = config.get('PATHS', 'p_trace')
fname              = os.path.normpath("%s\Crea_app" % path_res)

fvtcmd             = os.path.join(path_res ,  "%s.cmd"%fname)
# Default values
default_queue      = config.get('REF', 'default_queue')
queue              = config.get('REF', 'queue')
default_user       = config.get('REF', 'default_user')
default_cal        = config.get('REF', 'default_cal')
default_host       = config.get('REF', 'default_host')
hddmax             = config.get('REF', 'hddmax')

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
	query = """SELECT ID_KEY, V_ANAME, T2_ATEARLY, T2_ATLATER, ID_PLNG, ID_USER, ID_AGENT, ID_ENV, V_CYCLE, V_DESC FROM to_obj_app"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	# get the number of rows in the resultset
	numrows = int(cursor2.rowcount)
	dic_env = {}
	nb = 0
	Liste_elem_vu = []
	Liste_elem_vu2 = []
	#-------------------------------------------------------------------------------------------------------------------------
	# si la table de correspondance et le fichier existent deja
	#corr_cpt = 0
	corr_cptapp = 0  # a mettre avant la boucle for
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab          = getTab(fcorrtab)
	corrTab["app"]   = []    # a mettre avant la boucle for
	#corrTab["env"] ==> peut etre utilisee pour pacourir les environnements trouves avec le nom vt correspondant

	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	
	lvtom_envnames = getListVTnames("env", corrTab)
	lvtom_ressnames = getListVTnames("ressources", corrTab)
	lvtom_hostnames  = getListVTnames("agt", corrTab)
	lvtom_usrnames   = getListVTnames("usr", corrTab)
	#-------------------------------------------------------------------------------------------------------------------------
	# Creation de fichiers pour contenir les informations.
	f = open(fvtcmd, "w")
	fname2 = os.path.join(path_logs, "App_16char.txt" )
	f2 = open(fname2, "w")
	fname3 = os.path.join(path_logs, "AppAvecProblemesUsers.txt" )
	f3 = open(fname3, "w")
	fname4 = os.path.join(path_trace,"Log_job")
	flog = open(fname4, "w")
	print "--------------- Processing of applications ------------------\n"
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
		(app_id, app_name, d_hmin, d_hmax, idplng, iduser, idhost, env_name, cycle, desc) = d
		dic_env[app_id]= (app_name, d_hmin, d_hmax)
		# get real value from to_var table
		if iduser[0:2] == "VA":
			iduser = selectData("to_var", "ID_KEY", "V_VALUE", iduser)
		if idhost[0:2] == "VA":
			idhost = selectData("to_var", "ID_KEY", "V_VALUE", idhost)
		if idplng[0:2] == "VA":
			idplng = selectData("to_var", "ID_KEY", "V_VALUE", idplng)
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
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
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		
		
		
		# Changement des valeurs pour qu'elles soient adaptees a vtom
		if(user=="*ALL"):
			user = "ALL"
		if("\\" in user):
			f3.write("%s ---> Agent associe : %s\n  l'environnement ci-dessus est: %s\n\n" % (user, host, env_name))
			user = user.split('\\')[2]
		desc = str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		# Env_name = 16 char ou moins
		if len(env_name) > 16:
			f2.write("Nom de l'env depasse 16 char: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		if env_name in Liste_elem_vu :
			if len(env_name)>= 16: f2.write(" /!\\ Environnement vu en double: %s\n" % app_name)
		# Get host from our dictionary
		if len(host) > 16:
			host = getVTname (host, corrTab, 'agt')
		# Get user from our dictionary
		if len(user) > 16:
			user = getVTname (user, corrTab, 'usr')
		# Get cal from our dictionary
		if len(cal) > 16:
			cal = getVTname (cal, corrTab, 'cal')
		#App_name = 16 char ou moins
		if len(app_name) > 16:
			app_name = getVTname (app_name, corrTab, 'app')
			f2.write("Nom de l'app depasse 16 char: %s\n" % app_name)
		#	app_name = str(app_name[0:16])
		if app_name in Liste_elem_vu2:
			if len(app_name)>= 16: f2.write(" /!\\ Application vue en double: %s\n" % app_name)
			
		#------ON FORMATE LE NOM DE L'APPLICATION SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_appname = app_name
		lvtapps = getListVTnames("app", corrTab)
		(vtom_appname,isnum) = formatObjName(automator_appname, corr_cptapp, lvtapps)

		
		if ((vtom_appname != automator_appname) and isnum):
			#print vtom_appname, "<- vtom_appname et automator_appname->", automator_appname, "\n"
			corr_cptapp += 1
			corr = (automator_appname, vtom_appname)
			#corrTab["app"].append(corr)
		elif ((vtom_appname != automator_appname) and not isnum): 
			corr = (automator_appname, vtom_appname)
			corrTab["app"].append(corr)
		#---------------------------------------------------------------------------------------		
		app_name = vtom_appname
		
		d_hmin = str(d_hmin)
		d_hmax = str(d_hmax)
		
		# Creation variable heure debut et heure fin
		# If d_hmin is between 1 day and unlimited
		if (int(d_hmin[0:2]) >= 1 and int(d_hmin[0:2])< 99):
			heure=int(d_hmin[2:4])+24*int(d_hmin[0:2])
			d_hmin = str(heure)+":"+d_hmin[4:]+":"+"00"
			myprint("\tWARNING : Min hour for the application [ %s ] in environment [ %s ] is beyond one day."%app_name, env_name)
		elif(d_hmin[0:2] == "00"):
			d_hmin = d_hmin[2:4]+":"+d_hmin[4:]+":"+"00"
		# h max
		# If d_hmin is between 1 day and unlimited
		if (int(d_hmax[0:2]) >= 1 and int(d_hmax[0:2])< 99):
			heure=int(d_hmax[2:4])+24*int(d_hmax[0:2])
			d_hmax = str(heure)+":"+d_hmax[4:]+":"+"00"
			myprint("\tWARNING : Max hour for the application [ %s ] in environment [ %s ] is beyond one day."%app_name, env_name)
		elif(d_hmax[0:2] == "00"):
			d_hmax = d_hmax[2:4]+":"+d_hmax[4:]+":"+"00"
		if(d_hmax[0:2] == "99"):
			d_hmax = "illimite"
		
		
		# Si ce n'est pas cyclique
		if cycle == len(cycle) * cycle[0]:
		# Creation de l'environnement
			f.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Hdeb=%s /Hfin=%s /Bloquant=non /ApplErr=non /Calendar=%s/2015 /User=%s /Machine=%s /Queue=%s\n" % (env_name, app_name, desc, d_hmin, d_hmax, cal, user, host, queue))
		else:
		# Si c'est cyclique
			if str(d_hmax) == "illimite" :
				d_hmax = hddmax
			if len(cycle)>7:
				if cycle[:2] == cycle[3:5]:
					cycle=cycle[:2]+cycle[5:]
			else:	
				cycle = str(cycle[:2])+":"+str(cycle[2:4])+":"+str(cycle[4:]) 
			f.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Hdeb=%s /Hfin=%s /Bloquant=non /ApplErr=non /Calendar=%s/2015 /User=%s /Machine=%s /Queue=%s /Cyclique=oui /Cycle=%s\n" % (env_name, app_name, desc, d_hmin, d_hmax, cal, user, host, queue, cycle))
		Liste_elem_vu2.append(app_name)
		Liste_elem_vu.append(env_name)
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
	print "------------ End of processing for applications ------------\n"
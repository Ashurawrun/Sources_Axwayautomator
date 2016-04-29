#VERIFIER LES CAS OU ON A PLUSIEURS DOUBLONS DE MOINS DE 16 CHAR
# Creer en vert les notifs, 
# en rougeatre les jobs as400, 
# en violet les jobs commandes, 
# en turquoise les "OU",
# en jaune les "ET",
# en orange pour les test,
# en noir pour les abort,
# en gris pour les sleep,
# le reste est en bleu par defaut
import os, sys, MySQLdb
import ConfigParser
import string
from subprocess import Popen
from myTools import *
from datetime import datetime

config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths & database infos
server_name      = config.get('DATABASE', 'db_server') 
database_name    = config.get('DATABASE', 'db_name')
db_username      = config.get('DATABASE', 'db_user')
db_password      = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs        = config.get('PATHS', 'p_logs')
path_trace       = config.get('PATHS', 'p_trace')
fname            = os.path.normpath("%s\Crea_Job" % path_res)
fvtcmd           = os.path.join(path_res ,  "%s.cmd"%fname)
# Default values
default_queue    = config.get('REF', 'default_queue')
queue            = config.get('REF', 'queue')
default_user     = config.get('REF', 'default_user')
default_cal      = config.get('REF', 'default_cal')
default_year     = config.get('REF', 'default_year')
default_host     = config.get('REF', 'default_host')
default_app      = config.get('REF', 'default_app')
default_script   = config.get('REF', 'default_script')
default_spath    = config.get('REF', 'default_script_path')
default_hddmax   = config.get('REF', 'hddmax')
currentYear      = datetime.now().year

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
	

# Connexions to DB
db0 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor0 = db0.cursor()

db1 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor1 = db1.cursor()

db2 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor2 = db2.cursor()

db3 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor3 = db3.cursor()

db4 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor4 = db4.cursor()

db5 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor5 = db5.cursor()

db6 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor6 = db6.cursor()

db7 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor7 = db7.cursor()

db8 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor8 = db8.cursor()

db9 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor9 = db9.cursor()

db10 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor10 = db10.cursor()

db11 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor11 = db11.cursor()

db12 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor12 = db12.cursor()

db13 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor13 = db13.cursor()

db14 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor14 = db14.cursor()

db15 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor15 = db15.cursor()

db16 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor16 = db16.cursor()

# This function takes an environment id as parameters and it will look if there is any application attached to this environment
# if there is none it will return the value 'True' else it will return 'False'
def envSansApp (id_env):
	query = """SELECT * FROM to_obj_app WHERE ID_ENV=\"%s\" """ %(id_env)
	#query = """SELECT V_VALUE FROM to_var WHERE ID_KEY = \"VA0000030352\" """  # %(column2, tname, column1, value)
	lines = cursor15.execute(query)
	data = cursor15.fetchone()
	if data == None: 
		return True
	else:
		return False
	cursor15.close()
	db15.close()

# Function that is not yet used its use is to convert the Axwayautomator coord to VTOM coords
def ConvertCoord(s):
	coord = s.split(" ")
	X = coord[0]
	Y = coord[1]
	# Make the numbers positives only
	if "-" in X:
		X = X.replace("-", "")
		X = 0
	else:
		X = int(X)
		X = 2*X 
	if "-" in Y:
		Y = Y.replace("-", "")
		Y = 0
	else:
		Y = int(Y)
		Y = 3*Y
	X=int(X)
	Y=int(Y)
	return (X, Y)
	
# This function takes a file where it will write cmd commands to create applications as parameters,
# and it will look into all the environments and print in another file every environment without any application in it;
# it will also create a default application that will have the same name as the environment inside of applicationless environments
def EnvNeedApp(fres):
	dbEnvNeedApp = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
	cursorEnvNeedApp = dbEnvNeedApp.cursor()
	queryEnvNeedApp = """SELECT ID_KEY, V_ENAME FROM to_env"""
	lines = cursorEnvNeedApp.execute(queryEnvNeedApp)
	data = cursorEnvNeedApp.fetchall()
	print "[ Checking if each environment contains at least one application ]\n"
	#-----------------------------------------------------------------------------------------------------------------------
	fcorname       = "correspondances"    # a mettre avant la boucle for
	fcorrtab       = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	
	corrTab        = getTab(fcorrtab)
	corrTab["job"] = []    # a mettre avant la boucle for
	lvtom_envnames = getListVTnames("env", corrTab)
	#-----------------------------------------------------------------------------------------------------------------------
	# Creation de fichiers pour contenir les informations.
	fEnvNeedApp = os.path.normpath("%s\Env_sans_app.txt" % path_logs)
	fEnvApp = open(fEnvNeedApp, "w")
	
	for d in data:
		(env_id, env_name) = d
		env_name = getVTname (env_name, corrTab, 'env')
		if(envSansApp(env_id)==True):
			fEnvApp.write("%s\n" % (env_name))
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"application creee par la migration VTOM\"\n" % (env_name, env_name))
	dbEnvNeedApp.close()
	cursorEnvNeedApp.close()
	fEnvApp.close()
	print "[ End of the check for applicationless environments ]\n"

# Fn to find a string inside of a file
def isStringInFile(mystring):
	fcheck = os.path.normpath("%s\Env_sans_app.txt" % path_logs)
	fcheckenv = open(fcheck, "r") # Check if the env has at least one app	
	mystring = mystring + "\n" # to avoid finding a string name inside a bigger string
	for line in fcheckenv:
		if mystring in line:
			return True
	return False
	fcheckenv.close()
	
# Permet de recuperer une donnee dans une table en indiquant le nom de la table en question 
# et le nom de la colonne contenant un ID que l'on possede ainsi que l'ID que l'on possede
# et le nom de la colonne dans laquelle on souhaite recuperer la donnee 
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
	
# This function takes an ID from a job and will search all the parameters associated to this job in the table to_obj_prm
def getParams (idjob):
	query = """SELECT PROP_VAL FROM to_obj_job_prm WHERE ID=\"%s\" """ %(idjob)
	lines = cursor0.execute(query)
	data = cursor0.fetchall()
	if data == None:
		data = "None"
	return data
	
# This function takes a string 's', a first expression 'first' and a last expression 'last' and will give back what's inbetween
# Example: find_between(<$RG0000000004:CHEMIN_SCRIPTS>, <$RG, :) => '<$RG0000000004:'
def find_between(s, first, last ):
    try:
        start = s.index( first ) #+ len( first )
        end = s.index( last, start )
        return s[start:end+1]
    except ValueError:
        return ""

# This function takes a string looking like: "<$RG0000000004:CHEMIN_SCRIPTS>" 
# and will convert it into the value associated to the ID 'RG0000000004'
def replaceInsideParam(s):
	db16 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
	cursor16 = db16.cursor()
	for i in s:
		if '<$VA' in s:
			idtoreplace = find_between(s, "<$VA", ":")
			idtoreplace = idtoreplace.replace("<$", "")
			idtoreplace = idtoreplace.replace(":", "")
			#print "idtoreplace2 vaut %s\n" % idtoreplace
			query = """SELECT V_VALUE FROM to_var WHERE ID_KEY=\"%s\" """ %(idtoreplace)
			lines = cursor16.execute(query)
			data = cursor16.fetchone()
			if data == None :
				data == "None"
			else:
				data = data[0]
				storeplace = find_between(s, '<$VA', '>')
				#print "storeplace vaut :",storeplace,"il doit etre remplace par data qui vaut: ", data,"\n"
				s = s.replace(str(storeplace), str(data))
				#print "s vaut %s \n" % s
		if '<$DA' in s:
			idtoreplace = find_between(s, '<$DA', ':')
			idtoreplace = idtoreplace.replace("<$", "")
			idtoreplace = idtoreplace.replace(":", "")
			query = """SELECT V_DNAME FROM cf_date WHERE ID_KEY=\"%s\" """ %(idtoreplace)
			lines = cursor16.execute(query)
			data = cursor16.fetchone()
			if data == None :
				data = "None"
			else:
				data = data[0]
				storeplace = find_between(s, '<$', '>')
				s = s.replace(str(storeplace), str(data))
		if '<$RL' in s:
			idtoreplace = find_between(s, "<$RL", ":")
			idtoreplace = idtoreplace.replace("<$", "")
			idtoreplace = idtoreplace.replace(":", "")
			query = """SELECT V_VALUE FROM to_lres WHERE ID_KEY=\"%s\" """ %(idtoreplace)
			lines = cursor16.execute(query)
			data = cursor16.fetchone()
			if data == None :
				data == "None"
			else:
				data = data[0]
				storeplace = find_between(s, '<$RL', '>')
				s = s.replace(str(storeplace), str(data))
		if '<$RG' in s:
			idtoreplace = find_between(s, "<$RG", ":")
			idtoreplace = idtoreplace.replace("<$", "")
			idtoreplace = idtoreplace.replace(":", "")
			query = """SELECT V_VALUE FROM cf_gres WHERE ID_KEY=\"%s\" """ %(idtoreplace)
			lines = cursor16.execute(query)
			data = cursor16.fetchone()
			if data == None :
				data == "None"
			else:
				data = data[0]
				storeplace = find_between(s, '<$RG', '>')
				s = s.replace(str(storeplace), str(data))
	s = s.replace("*", "")
	cursor16.close()
	db16.close()
	return s

# This function will return the CMD in a string it is used for AS400 models
def getCMD(mystring):
	listCMD = ['CALL ', 'CLR', 'CHG', 'CPY', 'DLT', 'DLY', 'END', 'RUN','STRT']
	idtoreplace = ""
	for s in listCMD:
		if s in mystring:
			idtoreplace = find_between(mystring, s, ';')
			mystring = mystring.replace(idtoreplace, "")
			idtoreplace = idtoreplace.replace(";", "")
	if idtoreplace == "":
		idtoreplace = "ERREUR AUCUNE COMMANDE TROUVEE"
	return (mystring, idtoreplace)
	
# This function returns the total numbers of rows for all the jobs
def getNbRows():
	db = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
	cursor = db.cursor()
	# execute SQL select statement
	cursor.execute("SELECT * FROM to_obj_job")
	# get the number of rows in the resultset
	numrows = int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_wait")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_notif_wait")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_and")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_or")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_affectation")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_notif_monitor")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_notif_auto")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_command")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_test_res")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_focal")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_abort")
	numrows = numrows + int(cursor.rowcount)
	cursor.execute("SELECT * FROM to_obj_stop")
	numrows = numrows + int(cursor.rowcount)
	db.close()
	cursor.close()
	return numrows

# Creer les jobs de la table to_obj_wait
def creerJobwait (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC, DS_DELAY, T2_TIME FROM to_obj_wait"""
	lines = cursor3.execute(query)
	data = cursor3.fetchall()
	liste_script_vu = []
	print "--------------- Traitement des jobs \"wait\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		#print "Data = \n", d
		(job_id, job_name, env_name, app_name, desc, delay, d_hmax) = d
		dic_env[job_id]= (job_name, d_hmax, delay)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table			
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		if str(delay) == "None": script_name = default_script
		else: script_name = "Sleep.bat"
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = str(env_name[0:16])
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = str(app_name[0:16])
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
			job_name = str(job_name[0:16])
		# Creation variable heure debut et heure fin
		d_hmax = str(d_hmax)
		# h max
		# If d_hmax is between 1 day and unlimited
		if (int(d_hmax[0:2]) >= 1 and int(d_hmax[0:2])< 99):
			heure=int(d_hmax[2:4])+24*int(d_hmax[0:2])
			d_hmax = str(heure)+":"+d_hmax[4:]+":"+"00"
			myprint("\tWARNING : Max hour for the application [ %s ] in environment [ %s ] is beyond one day." % (app_name, env_name))
		elif(d_hmax[0:2] == "00"):
			d_hmax = d_hmax[2:4]+":"+d_hmax[4:]+":"+"00"
		if(d_hmax[0:2] == "99"):
			d_hmax = "illimite"
		
		
		desc=str(desc)
		if desc != "None": desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Hfin=%s /Machine=localhost /Cfond=DimGray\n" % (env_name, app_name, desc, d_hmax))
		fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /Par=\"%s\" /Comm=\"%s\" /Hfin=%s /Machine=localhost /Cfond=DimGray\n" % (env_name, app_name, job_name, default_spath, script_name, delay, desc, d_hmax))
		if script_name not in liste_script_vu :
			liste_script_vu.append(script_name)
			f4.write("%s ----> a creer\n" % script_name)
	db3.close()
	cursor3.close()
	return nb

# Creer les jobs de la table to_obj_notif_wait
def creerJob_notif_wait (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC, ID_AGENT, T2_TIME, V_MESSAGE FROM to_obj_notif_wait"""
	lines = cursor4.execute(query)
	data = cursor4.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"notif wait\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		typequeue = 0 # By default, the queue will be unknown if it is not defined
		#print "Data = \n", d
		(job_id, job_name, env_name, app_name, desc, idhost, d_hmax, desc2) = d
		dic_env[job_id]= (job_name, d_hmax)
		# get real value from to_var table
		idhost = str(idhost)
		if idhost[0:2] == "VA":
			idhost = selectData("to_var", "ID_KEY", "V_VALUE", idhost)
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
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
		
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)

		if queue == "queue_as400":
			script_name = "#OS400#"
		else:
			script_name = default_script
		desc = str(desc2) + " => V_MESSAGE. " + str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")

		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.
		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)
		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname		
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
			
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
		
		# Creation variable heure debut et heure fin
		d_hmax = str(d_hmax)
		# If d_hmax is between 1 day and unlimited
		if (int(d_hmax[0:2]) >= 1 and int(d_hmax[0:2])< 99):
			heure=int(d_hmax[2:4])+24*int(d_hmax[0:2])
			d_hmax = str(heure)+":"+d_hmax[4:]+":"+"00"
			myprint("\tWARNING : Max hour for the application [ %s ] in environment [ %s ] is beyond one day." % (app_name, env_name))
		elif(d_hmax[0:2] == "00"):
			d_hmax = d_hmax[2:4]+":"+d_hmax[4:]+":"+"00"
		if(d_hmax[0:2] == "99"):
			d_hmax = "illimite"
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Mode=simu /Comm=\"%s\" /Hfin=%s /Machine=%s /User=%s /Queue=%s /Cfond=DarkGreen\n" % (env_name, app_name, desc, d_hmax, default_host, default_user, queue))
		fres.write("vtaddjob /Nom=%s/%s/%s /Mode=simu /Script=#%s\%s /Comm=\"%s Machine => %s\" /Bloquant=non /ApplErr=non /Hfin=%s /Machine=%s /User=%s /Queue=%s /Cfond=DarkGreen\n" % (env_name, app_name, job_name, default_spath, script_name, desc, host, d_hmax, default_host, default_user, queue))
	db4.close()
	cursor4.close()
	return nb

# Creer les jobs de la table to_obj_and
def creerJob_ET (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC FROM to_obj_and"""
	lines = cursor5.execute(query)
	data = cursor5.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"et\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		#print "Data = \n", d
		(job_id, job_name, env_name, app_name, desc) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)

		script_name = default_script
		
		desc=str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
			
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Mode=simu /Comm=\"%s\" /Cal=tljours/%s /Machine=%s /Cfond=GoldenRod\n" % (env_name, app_name, desc, currentYear, default_host))
		fres.write("vtaddjob /Nom=%s/%s/%s /Mode=simu /Script=#%s\jobok.bat /Comm=\"%s\" /Bloquant=non /ApplErr=non /Cal=%s/%s /Machine=%s /Cfond=GoldenRod\n" % (env_name, app_name, job_name, default_spath, desc, default_cal, default_year, default_host))
	db5.close()
	cursor5.close()
	return nb

# Creer les jobs de la table to_obj_or	
def creerJob_OU (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC, XYWH FROM to_obj_or"""
	lines = cursor6.execute(query)
	data = cursor6.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"ou\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc, coord) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		script_name = default_script
		
		desc=str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")

		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)	
		
		(X,Y) = ConvertCoord(coord)
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Mode=simu /Comm=\"%s\" /Cal=tljours/%s /Machine=%s /User=%s /Cfond=DarkTurquoise\n" % (env_name, app_name, desc, currentYear, default_host, default_user))
		fres.write("vtaddjob /Nom=%s/%s/%s /Mode=simu /Script=#%s\jobok.bat /Comm=\"%s\" /Bloquant=non /ApplErr=non /Cal=%s/%s /Machine=%s /User=%s /Cfond=DarkTurquoise /Geom=65x65+%s+%s\n" % (env_name, app_name, job_name, default_spath, desc, default_cal, default_year, default_host, default_user, Y, X))
	db6.close()
	cursor6.close()
	return nb

# Creer les jobs de la table to_obj_affectation
def creerJob_Affectation (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC FROM to_obj_affectation"""
	lines = cursor7.execute(query)
	data = cursor7.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"affectation\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)

		script_name = default_script
		
		desc=str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
			
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Bloquant=non /ApplErr=non\n" % (env_name, app_name, desc))
		fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /Comm=\"%s\" /Bloquant=non /ApplErr=non\n" % (env_name, app_name, job_name, default_spath, script_name, desc))
	db7.close()
	cursor7.close()
	return nb

# Creer les jobs de la table to_obj_notif_monitor	
def creerJob_notif_monitor (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_MESSAGE, M_THOST FROM to_obj_notif_monitor"""
	lines = cursor8.execute(query)
	data = cursor8.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"notif monitor\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc, idhost) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		idhost = str(idhost)
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		
		desc=str(desc)
		desc = desc.replace("\n", "")
		
		typequeue = selectData("cf_agt", "M_HNAME", "V_SYSTYPE", idhost)
		if typequeue == 0: queue = "queue_unknown"
		if typequeue == 1: queue = "queue_wnt"
		if typequeue == 2: queue = "queue_as400"
		if typequeue == 20: queue = "queue_gcos7"
		if typequeue == 21: queue = "queue_gcos8"
		if typequeue == 25: queue = "queue_mvs"
		if typequeue == 4 or typequeue == 5 or typequeue == 6 or typequeue == 8 or typequeue == 10: queue = "queue_ksh"
		if queue == "queue_as400":
			script_name = "#OS400#"
		else:
			script_name = '#'

		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else:
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)	

		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Mode=simu /Comm=\"%s\" /Machine=%s /User=%s /Cfond=DarkGreen\n" % (env_name, app_name, desc, default_host, default_user))		
		if idhost[:1] == "<":
			fres.write("vtaddjob /Nom=%s/%s/%s /Mode=simu /Script=#%s\%s /Comm=\"%s\" /Bloquant=non /ApplErr=non /Machine=%s /Cfond=DarkGreen\n" % (env_name, app_name, job_name, default_spath, script_name, desc, default_host))
		else:
			fres.write("vtaddjob /Nom=%s/%s/%s /Mode=simu /Script=#%s\%s /Comm=\"%s | Machine => %s\" /Bloquant=non /ApplErr=non /Machine=%s /Cfond=DarkGreen\n" % (env_name, app_name, job_name, default_spath, script_name, desc, idhost, default_host))
	db8.close()
	cursor8.close()
	return nb

# Creer les jobs de la table to_obj_notif_auto
def creerJob_notif_auto (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC, V_MESSAGE FROM to_obj_notif_auto"""
	lines = cursor9.execute(query)
	data = cursor9.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"notif auto\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc, desc2) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		script_name = default_script
		
		script_name = default_script
		desc = str(desc2) + " => V_MESSAGE." + str(desc)
		desc = desc.replace("\n", "")
		
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Mode=simu /Comm=\"%s\" /Machine=%s /User=%s /Cfond=DarkGreen\n" % (env_name, app_name, desc, default_host, default_user))
		fres.write("vtaddjob /Nom=%s/%s/%s /Mode=simu /Script=#%s\%s /Comm=\"%s\" /Bloquant=non /ApplErr=non /Machine=%s /User=%s /Cfond=DarkGreen\n" % (env_name, app_name, job_name, default_spath, script_name, desc, default_host, default_user))
	db9.close()
	cursor9.close()
	return nb

# Creer les jobs de la table to_obj_command
def creerJob_command (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC, ID_AGENT, V_CMD FROM to_obj_command"""
	lines = cursor10.execute(query)
	data = cursor10.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"command\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		typequeue = 0 # By default, the queue will be unknown if it is not defined
		(job_id, job_name, env_name, app_name, desc, idhost, desc2) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		idhost = str(idhost)
		if idhost[0:2] == "VA":
			idhost = selectData("to_var", "ID_KEY", "V_VALUE", idhost)
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		if idhost == "None": host = default_host
		else: host  = selectData("cf_agt", "ID_KEY", "M_HNAME", idhost)
		
		if host == default_host: queue = default_queue
		else: typequeue = selectData("cf_agt", "ID_KEY", "V_SYSTYPE", idhost)
		if typequeue == 0: queue = "queue_unknown"
		if typequeue == 1: queue = "queue_wnt"
		if typequeue == 2: queue = "queue_as400"
		if typequeue == 20: queue = "queue_gcos7"
		if typequeue == 21: queue = "queue_gcos8"
		if typequeue == 25: queue = "queue_mvs"
		if typequeue == 4 or typequeue == 5 or typequeue == 6 or typequeue == 8 or typequeue == 10: queue = "queue_ksh"
		if queue == "queue_as400":
			script_name = "#OS400#"
		else:
			script_name = "\"" + desc2 + "\"" # Script <=> V_CMD
		desc = str(desc2) + " <= CMD | " + str(desc)
		desc = desc.replace("\n", "")
		
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)

		desc = str(desc) + " " + str(desc2)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		desc2 = replaceInsideParam(desc2)
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
			
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Machine=%s /Queue=%s /Cfond=DarkOrchid\n" % (env_name, app_name, desc, host, queue))
		if script_name == "#OS400#":
			fres.write("vtaddjob /Nom=%s/%s/%s /Script=\"%s\" /Comm=\"%s\" /Bloquant=non /ApplErr=non /Par=CMD=\"%s\" /Machine=%s /Queue=%s /Cfond=DarkOrchid\n" % (env_name, app_name, job_name, script_name, desc, desc2, host, queue))
		else:
			fres.write("vtaddjob /Nom=%s/%s/%s /Script=\"%s\" /Comm=\"%s\" /Bloquant=non /ApplErr=non /Machine=%s /Queue=%s /Cfond=DarkOrchid\n" % (env_name, app_name, job_name, script_name, desc, host, queue))
	db10.close()
	cursor10.close()
	return nb

# Creer les jobs de la table to_obj_test_res
def creerJob_test (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC FROM to_obj_test_res"""
	lines = cursor11.execute(query)
	data = cursor11.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"test\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)

		script_name = default_script
		
		desc=str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)			
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name		
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Cfond=Orange\n" % (env_name, app_name, desc))
			
		fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /Comm=\"%s\" /Bloquant=non /ApplErr=non /Cfond=Orange\n" % (env_name, app_name, job_name, default_spath, script_name, desc))
	db11.close()
	cursor11.close()
	return nb

# Creer les jobs de la table to_obj_focal
def creerJob_focal (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC, V_MESSAGE, M_THOST FROM to_obj_focal"""
	lines = cursor12.execute(query)
	data = cursor12.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"focal\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc, desc2, idhost) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		idhost = str(idhost)
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)

		script_name = default_script
		desc = str(desc2) + " " + str(desc)
		desc=str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Bloquant=non /ApplErr=non\n" % (env_name, app_name, desc))
		if idhost[:1] == "<":
			fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /Comm=\"%s\" /Bloquant=non /ApplErr=non\n" % (env_name, app_name, job_name, default_spath, script_name, desc))
		else:
			fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /Comm=\"%s\" /Bloquant=non /ApplErr=non /Machine=%s\n" % (env_name, app_name, job_name, default_spath, script_name, desc, idhost))
	db12.close()
	cursor12.close()
	return nb

# Creer les jobs de la table to_obj_abort	
def creerJob_abort (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC FROM to_obj_abort"""
	lines = cursor13.execute(query)
	data = cursor13.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"abort\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)

		script_name = default_script
		
		desc=str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Cfond=Black\n" % (env_name, app_name, desc))
		fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /Comm=\"%s\" /Bloquant=non /ApplErr=non /Cfond=Black\n" % (env_name, app_name, job_name, default_spath, script_name, desc))
	db13.close()
	cursor13.close()
	return nb
	
# Creer les jobs de la table to_obj_stop
def creerJob_stop (nb, numrows):
	query = """SELECT ID, V_USRNAME, ID_ENV, ID_APP, V_DESC FROM to_obj_stop"""
	lines = cursor14.execute(query)
	data = cursor14.fetchall()
	corr_cptjob = 0
	print "--------------- Traitement des jobs \"stop\" en cours ------------------"
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False
		(job_id, job_name, env_name, app_name, desc) = d
		dic_env[job_id]= (job_name)
		# get real value from to_var table
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		
		# get the name from the right table
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		if str(app_name) == "None": app_name = str(job_name[0:16])
		else: app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		script_name = default_script
		
		desc=str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

		
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		# Env_name = 16 char or less
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		# App_name = 16 char or less
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = getVTname (app_name, corrTab, 'app')
		# job_name = 16 char or less
		if len(job_name) > 16:
			f2.write("Nom du job: %s\n" % job_name)

		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name	
		if creerapp == True:
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Cfond=Red\n" % (env_name, app_name, desc))
		fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /Comm=\"%s\" /Cfond=Red\n" % (env_name, app_name, job_name, default_spath, script_name, desc))
	db14.close()
	cursor14.close()
	return nb

	
if __name__ == "__main__":
	query = """SELECT ID_KEY, V_JNAME, T2_ATEARLY, T2_ATLATER, ID_PLNG, ID_USER, ID_AGENT, ID_ENV, V_CYCLE, V_DESC, ID_APP, V_PATH, V_SCRIPT FROM to_obj_job"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	# get the number of rows in the resultset
	numrows = getNbRows()
	nb = 0
	warning = 0
	dic_env = {}
	Liste_elem_vu = []
	Liste_elem_vu2 = []
	Liste_elem_vu3 = []
	#-------------------------------------------------------------------------------------------------------------------------
	# si la table de correspondance et le fichier existent deja
	#corr_cpt = 0
	corr_cptjob = 0  # a mettre avant la boucle for
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab          = getTab(fcorrtab)
	corrTab["job"]   = []    # a mettre avant la boucle for
	

	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	
	lvtom_envnames   = getListVTnames("env", corrTab)
	lvtom_appnames   = getListVTnames("app", corrTab)
	lvtom_ressnames  = getListVTnames("ressources", corrTab)
	lvtom_hostnames  = getListVTnames("agt", corrTab)
	lvtom_usrnames   = getListVTnames("usr", corrTab)
	lvtom_calnames   = getListVTnames("cal", corrTab)
	#-------------------------------------------------------------------------------------------------------------------------
	
	print "--------------- Processing of jobs ------------------\n"
	# Creation of the file to contain informations of the problems met
	fres = open(fvtcmd, "w")
	fname2 = os.path.normpath("%s\Job_16char.txt" % path_logs)
	f2 = open(fname2, "w")
	fname3 = os.path.normpath("%s\JobAvecProblemesUsers.txt" % path_logs)
	f3 = open(fname3, "w")
	fname4 = os.path.normpath("%s\Scripts_a_creer.txt" % path_logs)
	f4 = open(fname4, "w")
	fname5 = os.path.normpath("%s\Log_job" % path_trace)
	flog = open(fname5, "w")
	# Creates application in applicationless environments
	EnvNeedApp(fres)
	fres.write("vtaddcal -n tljours -y %s /daysInWeek=wwwwwww /publicHolidays=n\n" % currentYear)
	######################################################################################################if False : 
	for d in data:
		nb += 1 # Count main table number of row
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
		creerapp = False # By default, you don't want to create an application, but you will create one if the job isn't in any
		typequeue = 0 # By default, the queue will be unknown if it is not defined
		(job_id, job_name, d_hmin, d_hmax, idplng, iduser, idhost, env_name, cycle, desc, app_name, script_path, script_name) = d
		# get real value for user, host, planning and environment from to_var table
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
		
		#----------------Define the queue according to the host-----------------
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
		if str(app_name) == "None":
			app_name = str(job_name)
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		if str(script_name) == "None" or str(script_name)[:1] == "<" : script_name = default_script
		
		if str(script_path) =="None":
			script_path = default_spath
		else:
			if str(script_path[0:2]) == "<$":
				script_path = replaceInsideParam(script_path) 
		
		#----------------------Adapting the values names to VTOM---------------------
		if ("*" in user):
			user = user.replace("*", "")
		if("\\" in user):
			f3.write("%s ---> Agent associe : %s\n  l'environnement ci-dessus est: %s\n\n" % (user, host, env_name))
			user = user.rsplit('\\')[-1]
		desc = str(desc)
		desc = desc.replace("\n", "")
		desc = desc.replace("None", "")
		# Get env_name from our dictionary
		if len(env_name) > 16:
			env_name = getVTname (env_name, corrTab, 'env')
		# 'Analyse' files for Env_name (= + of 16 char)
		if env_name not in Liste_elem_vu:
			if len(env_name)>= 16: f2.write("Nom de l'env: %s\n" % env_name)
		# Get App_name from our dictionary
		if len(app_name) > 16:
			app_name = getVTname (app_name, corrTab, 'app')
		# Get host from our dictionary
		if len(host) > 16:
			host = getVTname (host, corrTab, 'agt')
		# Get user from our dictionary
		if len(user) > 16:
			user = getVTname (user, corrTab, 'usr')
		# Get cal from our dictionary
		if len(cal) > 16:
			cal = getVTname (cal, corrTab, 'cal')
		# Get job from our dictionary if it is already in it
		if len(job_name) > 16:
			job_name = getVTname (job_name, corrTab, 'job')
		# 'Analyse' files for App_name (= + of 16 char)
		if app_name not in Liste_elem_vu2:
			if len(app_name)>= 16: f2.write("Nom de l'app: %s\n" % app_name)
		# 'Analyse' files for job_name (= + of 16 char)
		if job_name not in Liste_elem_vu3:
			if len(job_name)>= 16: f2.write("Nom du job: %s\n" % job_name)

		#------ON FORMATE LE NOM DU JOB SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_jobname = job_name
		lvtjobs = getListVTnames("job", corrTab)
		(vtom_jobname,isnum) = formatObjName(automator_jobname, corr_cptjob, lvtjobs)

	
		if ((vtom_jobname != automator_jobname) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptjob += 1
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		elif ((vtom_jobname != automator_jobname) and not isnum): 
			corr = (automator_jobname, vtom_jobname)
			corrTab["job"].append(corr)
		
		#---------------------------------------------------------------------------------------		
		job_name = vtom_jobname	
		
		#--------------Creation variable heure debut et heure fin-----------------		
		# Creation of a variable heure debut & heure fin for the beginning and ending time of executions
		d_hmin = str(d_hmin)
		d_hmax = str(d_hmax)
		# If d_hmin is between 1 day and unlimited
		if (int(d_hmin[0:2]) >= 1 and int(d_hmin[0:2])< 99):
			heure=int(d_hmin[2:4])+24*int(d_hmin[0:2])
			d_hmin = str(heure)+":"+d_hmin[4:]+":"+"00"
			flog.write("\tWARNING : Min hour for the application [ %s ] in environment [ %s ] is beyond one day." % (app_name, env_name))
			warning = 1
		elif(d_hmin[0:2] == "00"):
			d_hmin = d_hmin[2:4]+":"+d_hmin[4:]+":"+"00"
		# h max
		# If d_hmax is between 1 day and unlimited
		if (int(d_hmax[0:2]) >= 1 and int(d_hmax[0:2])< 99):
			heure=int(d_hmax[2:4])+24*int(d_hmax[0:2])
			d_hmax = str(heure)+":"+d_hmax[4:]+":"+"00"
			flog.write("\tWARNING : Max hour for the application [ %s ] in environment [ %s ] is beyond one day." % (app_name, env_name))
			warning = 1
		elif(d_hmax[0:2] == "00"):
			d_hmax = d_hmax[2:4]+":"+d_hmax[4:]+":"+"00"
		if(d_hmax[0:2] == "99"):
			d_hmax = "illimite"
		
		#--------------------------------Parametres--------------------------
		z=0
		params = ''
		for i in getParams(job_id):
			params = params +str(getParams(job_id)[0+z][0])+';'
			z = z+1
		params = params[:-1]
		params = replaceInsideParam(params)
		params = params.replace("\"", "")
		params = " ".join(params.split())
		#-------------------------------------------------------------------
		
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			creerapp = False
			app_name = env_name
		if creerapp == True:
			app_name = job_name
			(params, CMD) = getCMD(params)
			fres.write("vtaddapp /Nom=%s/%s /Comm=\"%s\" /Hdeb=%s /Hfin=%s /sepopt=\";\" /Par=CMD=\"%s\" /Cal=%s/2015 /User=%s /Machine=%s /Queue=%s\n" % (env_name, app_name, desc, d_hmin, d_hmax, CMD, cal, user, host, queue))
		# if not a cycle
		if cycle == len(cycle) * cycle[0]:
			if queue == "queue_as400":
				(params, CMD) = getCMD(params)
				fres.write("vtaddjob /Nom=%s/%s/%s /Script=#OS400# /sepopt=\";\" /Par=\"%s\" /Comm=\"%s\" /Hdeb=%s /Hfin=%s /Bloquant=non /ApplErr=non /Par=CMD=\"%s\" /Cal=%s/2015 /User=%s /Machine=%s /Queue=%s /Cfond=Brown\n" % (env_name, app_name, job_name, params, desc, d_hmin, d_hmax, CMD, cal, user, host, queue))
			else:
				# Creation of the environment
				fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /sepopt=\";\" /Par=\"%s\" /Comm=\"%s\" /Hdeb=%s /Hfin=%s /Bloquant=non /ApplErr=non /Cal=%s/2015 /User=%s /Machine=%s /Queue=%s\n" % (env_name, app_name, job_name, script_path, script_name, params, desc, d_hmin, d_hmax, cal, user, host, queue))
		else:
		# if it is a cycle
			if (str(d_hmax) == "illimite"):
				d_hmax = default_hddmax
			if len(cycle)>7:
				if cycle[:2] == cycle[3:5]:
					cycle=cycle[:2]+cycle[5:]
			else:
				cycle = str(cycle[:2])+":"+str(cycle[2:4])+":"+str(cycle[4:])
			if queue == "queue_as400":
				(params, CMD) = getCMD(params)
				fres.write("vtaddjob /Nom=%s/%s/%s /Script=#OS400# /sepopt=\";\" /Par=\"%s\" /Comm=\"%s\" /Hdeb=%s /Hfin=%s /Bloquant=non /ApplErr=non /Par=CMD=\"%s\" /Cal=%s/2015 /User=%s /Machine=%s /Queue=%s /Cyclique=oui /Cycle=%s /Cfond=Brown\n" % (env_name, app_name, job_name, params, desc, d_hmin, d_hmax, CMD, cal, user, host, queue, cycle))
			else:
				fres.write("vtaddjob /Nom=%s/%s/%s /Script=#%s\%s /sepopt=\";\" /Par=\"%s\" /Comm=\"%s\" /Hdeb=%s /Hfin=%s /Bloquant=non /ApplErr=non /Cal=%s/2015 /User=%s /Machine=%s /Queue=%s /Cyclique=oui /Cycle=%s\n" % (env_name, app_name, job_name, script_path, script_name, params, desc, d_hmin, d_hmax, cal, user, host, queue, cycle))
		Liste_elem_vu2.append(app_name)
		Liste_elem_vu.append(env_name)
	if warning == 1:
		print "\tWARNING: One (or more) job's latest execution time possible is beyond 24 hours after the time it starts !"
	nb = creerJobwait (nb, numrows)
	nb = creerJob_notif_wait(nb, numrows) # a un host
	nb = creerJob_ET(nb, numrows)
	nb = creerJob_OU(nb, numrows)
	nb = creerJob_command(nb, numrows) # a un host
	nb = creerJob_Affectation(nb, numrows)
	nb = creerJob_notif_monitor(nb, numrows) # a un host
	nb = creerJob_notif_auto(nb, numrows)
	nb = creerJob_test(nb, numrows)
	nb = creerJob_abort (nb, numrows)
	#creerJob_focal () # Ne pas reprendre # a un host
	#creerJob_stop () # Ne pas reprendre
	print "100% of the jobs were processed\n"
	print "Number of elements processed: %s\n" % nb
	db0.close()
	db1.close()
	db2.close()
	db16.close()
	cursor0.close()
	cursor1.close()
	cursor2.close()
	savetab(corrTab, "%s_tab.txt"%fcorname)      # a mettre en fin de script
	saveTabinDB(corrTab,"%s_tab.db"%fcorname)    # a mettre en fin de script
	fres.close()
	f2.close()
	f3.close()
	f4.close()
	flog.close()
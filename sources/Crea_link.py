#VERIFIER LES CAS OU ON A PLUSIEURS DOUBLONS DE MOINS DE 16 CHAR
import os, sys, MySQLdb
from myTools import *
import ConfigParser
from subprocess import Popen

# Paths & database infos
config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

server_name      = config.get('DATABASE', 'db_server') 
database_name    = config.get('DATABASE', 'db_name')
db_username      = config.get('DATABASE', 'db_user')
db_password      = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs        = config.get('PATHS', 'p_logs')
path_trace       = config.get('PATHS', 'p_trace')
fname            = os.path.normpath("%s\Crea_link" % path_res)
fvtcmd           = os.path.join(path_res ,  "%s.cmd"%fname)
# Default values
default_app      = config.get('REF', 'default_app')
default_script   = config.get('REF', 'default_script')
default_spath    = config.get('REF', 'default_script_path')

# Connexions to DB
db0 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor0 = db0.cursor()

db1 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor1 = db1.cursor()

db2 = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
cursor2 = db2.cursor()


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
	
# Fn to find a string inside of a file
def isAS400(idjob):
	query = """SELECT ID_AGENT FROM to_obj_job WHERE ID_KEY=\"%s\" """ %(idjob)
	lines = cursor0.execute(query)
	data = cursor0.fetchone()
	if data == None:
		data = "None"
	else:
		idhost = data[0]
		if idhost[0:2] == "VA":
			idhost = selectData("to_var", "ID_KEY", "V_VALUE", idhost)
	typequeue = selectData("cf_agt", "ID_KEY", "V_SYSTYPE", idhost)
	if typequeue == 2: 
		#queue = "queue_as400"
		return True
	else: return False
		

def IDtoString (id):
	typequeue = 0
	if id[0:2] == "AT":
		idname = selectData("to_obj_wait", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_wait", "ID", "ID_APP", id)
		id_script = selectData("to_obj_wait", "ID", "DS_DELAY", id)
		id_script = "Sleep.bat /Par=\""+str(id_script)+"\" "
	if id[0:2] == "NW": # Risque de devoir ajouter les memes lignes qu'A "CM" pour considerer les jobs AS400
		idname = selectData("to_obj_notif_wait", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_notif_wait", "ID", "ID_APP", id)
		id_script = default_script
	if id[0:2] == "ET":
		idname = selectData("to_obj_and", "ID", "V_USRNAME", id) # A VERIFIER (probleme = si le job est lie a une app cas non traite => regarder si ID_APP != "None")
		id_app = selectData("to_obj_and", "ID", "ID_APP", id)
		id_script = "jobok.bat"
	if id[0:2] == "OU":
		idname = selectData("to_obj_or", "ID", "V_USRNAME", id)	 # A VERIFIER (probleme = si le job est lie a une app cas non traite => regarder si ID_APP != "None")
		id_app = selectData("to_obj_or", "ID", "ID_APP", id)
		id_script = "jobok.bat"
	if id[0:2] == "AF":
		idname = selectData("to_obj_affectation", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_affectation", "ID", "ID_APP", id)
		id_script = default_script
	if id[0:2] == "NM": # Risque de devoir ajouter les memes lignes qu'A "CM" pour considerer les jobs AS400
		idname = selectData("to_obj_notif_monitor", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_notif_monitor", "ID", "ID_APP", id)
		id_script = default_script
	if id[0:2] == "CM":
		idname = selectData("to_obj_command", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_command", "ID", "ID_APP", id)
		idhost = selectData("to_obj_command", "ID", "ID_AGENT", id)
		if idhost[0:2] == "VA":
			idhost = selectData("to_var", "ID_KEY", "V_VALUE", idhost)
		else:
			if idhost == "None": 
				typequeue = 0
			else: 
				typequeue = selectData("cf_agt", "ID_KEY", "V_SYSTYPE", idhost)
		if typequeue == 2:
			id_script = "#OS400#"
		else:
			id_script = default_script
	if id[0:2] == "TE":
		idname = selectData("to_obj_test_res", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_test_res", "ID", "ID_APP", id)
		id_script = default_script
	if id[0:2] == "AB":
		idname = selectData("to_obj_abort", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_abort", "ID", "ID_APP", id)
		id_script = default_script
	if id[0:2] == "JO":	
		idname = selectData("to_obj_job", "ID_KEY", "V_JNAME", id)
		id_app = selectData("to_obj_job", "ID_KEY", "ID_APP", id)
		id_script = selectData("to_obj_job", "ID_KEY", "V_SCRIPT", id)
		if isAS400(id): id_script = "#OS400#"
		if str(id_script) == "None" or str(id_script)[:1] == "<" : id_script = default_script
	if id[0:2] == "NA":
		idname = selectData("to_obj_notif_auto", "ID", "V_USRNAME", id)
		id_app = selectData("to_obj_notif_auto", "ID", "ID_APP", id)
		id_script = default_script
	return (idname, id_app, id_script)
	
def WhichLink (idtype):
	if idtype == -1:
		idtype = "obli"
	if idtype == 0:
		idtype = "obli"
	elif idtype == 1:
		idtype = "excl"
	elif idtype == 3:
		idtype = "facu"
	elif idtype == 4:
		idtype = "erre"
	elif idtype == 5:
		idtype = "obli"
	elif idtype == 6:
		idtype = "obli"
	elif idtype == 7:
		idtype = "obli"
	elif idtype == 8:
		idtype = "facu"
	else:
		idtype = "obli"
	return idtype

	
if __name__ == "__main__":
	query = """SELECT ID, ID_ENV, ID_APP, V_USRNAME, OBJ_FROM, OBJ_TO, LTYPE FROM to_obj_link"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	# get the number of rows in the resultset
	numrows = int(cursor2.rowcount)
	dic_env = {}
	i = 0
	k = 0
	z = 0
	nb = 0
	Liste_elem_vu = []
	Liste_elem_vu2 = []
	print "--------------- Processing of links ------------------\n"
	#-------------------------------------------------------------------------------------------------------------------------
	# si la table de correspondance et le fichier existent deja
	corr_cptlink = 0
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab          = getTab(fcorrtab)
	#corrTab["env"] ==> peut etre utilisee pour pacourir les environnements trouves avec le nom vt correspondant
	corrTab["link"]   = []    # a mettre avant la boucle for
	
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	
	lvtom_envnames = getListVTnames("env", corrTab)
	lvtom_appnames = getListVTnames("app", corrTab)
	lvtom_jobnames = getListVTnames("job", corrTab)
	#-------------------------------------------------------------------------------------------------------------------------
	
	# Creation de fichiers pour contenir les informations.
	fname = os.path.normpath("%s\Crea_link.cmd" % path_res)
	f = open(fname, "w")
	fname2 = os.path.normpath("%s\link_App_16char.txt" % path_logs)
	f2 = open(fname2, "w")
	fname3 = os.path.normpath("%s\Log_lien" % path_trace)
	f3 = open(fname3, "w")
	
	for d in data:
		creerapp = False
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
		(lien_id, env_name, app_name, lien_name, idfrom, idto, idtype) = d
		dic_env[lien_id]= (lien_name, idfrom, idto, idtype)

		# Don't migrate job "FCL", "ST" or "SF"
		if str(idfrom[0:3]) == "FCL" or str(idto[0:3]) == "FCL":
			continue
		if str(idfrom[0:2]) == "ST" or str(idto[0:2]) == "ST":
			continue
		if str(idfrom[0:2]) == "SF" or str(idto[0:2]) == "SF":
			continue			
		# get real value from to_var table
		# idfrom is the source of the link:
		if (idfrom[0:2] == "AP"):
			idfrom = selectData("to_obj_app", "ID_KEY", "V_ANAME", idfrom)
		else:
			(idfrom,idfrom_app,idfrom_script) = IDtoString(idfrom)

		# idto is the direction of the link:
		if (idto[0:2] == "AP"):
			idto = selectData("to_obj_app", "ID_KEY", "V_ANAME", idto)
		else:
			(idto,idto_app,idto_script) = IDtoString(idto)
		# Get the right environment ID
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		
		
		idtype = WhichLink(idtype)
		
		
		# On va faire des liens entre les app pour eviter les cas ou les jobs ne sont pas dans des apps mais relies a des app
		if str(app_name) == "None": 
			app_name = default_app
			creerapp = True
		else: 
			app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		

		# job_name = 16 char ou moins
		if len(idto) > 16:
			idto = getVTname (idto, corrTab, 'job')
		if len(idfrom) > 16:
			idfrom = getVTname (idfrom, corrTab, 'job')
		# job_name = 16 char ou moins
		if len(idto) > 16:
			idto = getVTname (idto, corrTab, 'link')
		if len(idfrom) > 16:
			idfrom = getVTname (idfrom, corrTab, 'link')
		
		# VERIFIER SI CELA CONVIENT (rajouter un booleen garde l'etat au cas ou on veuille relier des jobs dans des apps a d'autres app sans relier les app entre elle X-liens)
		# On donne a tout les jobs une app 
		# Si idfrom_app n'est pas nul chercher son app
		if idto_app != "None": 
			idto_app = selectData("to_obj_app", "ID_KEY", "V_ANAME", idto_app)
		if idfrom_app != "None":
			idfrom_app = selectData("to_obj_app", "ID_KEY", "V_ANAME", idfrom_app)

		#------ON FORMATE LE NOM DES JOBS SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_job1name = idto
		lvtjobs = getListVTnames("link", corrTab)
		(vtom_job1name,isnum) = formatObjName(automator_job1name, corr_cptlink, lvtjobs)
		automator_job2name = idfrom
		lvtjobs = getListVTnames("link", corrTab)
		(vtom_job2name,isnum) = formatObjName(automator_job2name, corr_cptlink, lvtjobs)


	
		if ((vtom_job1name != automator_job1name) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptlink += 1
			corr = (automator_job1name, vtom_job1name)
			corrTab["link"].append(corr)
		elif ((vtom_job1name != automator_job1name) and not isnum): 
			corr = (automator_job1name, vtom_job1name)
			corrTab["link"].append(corr)
		if ((vtom_job2name != automator_job2name) and isnum):
			#print vtom_jobname, "<- vtom_jobname et automator_jobname->", automator_jobname, "\n"
			corr_cptlink += 1
			corr = (automator_job2name, vtom_job2name)
			corrTab["link"].append(corr)
		elif ((vtom_job2name != automator_job2name) and not isnum): 
			corr = (automator_job2name, vtom_job2name)
			corrTab["link"].append(corr)
		
		#---------------------------------------------------------------------------------------
		idto = vtom_job1name
		idfrom = vtom_job2name
		
		# Si idfrom_app ou idto_app est nul lui donner idfrom en app
		if idto_app == "None": idto_app = str(idto[0:16])
		if idfrom_app == "None": idfrom_app = str(idfrom[0:16])
		
		if str(idto) == "None":
			idto = str(idto_app)
		if str(idfrom) == "None":
			idfrom = str(idfrom_app)
		
		#Test pour voir si il est possible qu'un job ne soit pas relie a une app mais que l'on ait un id d'app dans la table
		if((idfrom_app == "None" or idto_app == "None") and str(app_name) != "None"):
			f2.write("ATTENTION LIEN A PROBLEME !\n ID du lien : %s\n IDFROM %s\n IDTO %s\n NOM DE L'APP %s \n" % (lien_id, idfrom, idto, app_name))
			continue
		
		# Env_name = 16 char ou moins
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = getVTname (env_name, corrTab, 'env')
		if env_name in Liste_elem_vu :
			if len(env_name)>= 16: f2.write(" /!\\ Environnement vu en double: %s\n" % env_name)
		# App_name = 16 char ou moins
		if len(app_name) > 16:
			app_name = getVTname (app_name, corrTab, 'app')
		if app_name not in Liste_elem_vu2:
			if len(app_name)>= 16: f2.write(" /!\\ Application vue en double: %s\n" % app_name)


		
		# On verifie que les jobs sont bien dans une application
		if (app_name == "None" and idfrom_app == "None" or idto_app =="None"):
			f2.write("%s  --appname--> , %s et %s --idfromapp-->, %s et %s idto_app--> %s -- Lien_id\n" % (app_name, idfrom_app, idfrom, idto_app, idto, lien_id))
			break;
			
		# If our environment isn't containing any application
		# we create our job in an app named after the environment
		if isStringInFile(env_name) == True:
			# Don't create an app for each job
			app_name = env_name
			
		if idfrom_script != "#OS400#" :
			idfrom_script = '#' + default_spath + "\\" + idfrom_script
		if idto_script != "#OS400#" :
			idto_script = '#' + default_spath + "\\" + idto_script
		# If our job doesn't need to have an application created for it
		if (app_name != default_app):
			f.write("vtaddjob /Nom=%s/%s/%s /Script=%s /LienDe=%s/%s/%s[%s]\n" % (env_name, app_name, idfrom, idfrom_script, env_name, app_name, idto, idtype))
		# If our job may not end up in an application, we'll create one for it
		else:
			# We start by processing idto because idfrom is being processed while we create the link
			f.write("vtaddapp /Nom=%s/%s /Comm=\"Application correspondante au job %s\"\n" % (env_name, idto_app, idto))
			# We create the link and process idfrom at the same time
			f.write("vtaddapp /Nom=%s/%s /LienDe=%s/%s[%s]\n" % (env_name, idfrom_app, env_name, idto, idtype))
			# VERIFIER POURQUOI IDFROM PEUT DEPASSER 16 CHAR (vtaddjob /Nom=CAIXA_SOIR/SAUVEGARDE_AV_TO/SAUVEGARDE_AV_TOUT)
			# On place les jobs correspondants dans les app que l'on vient de creer plutot que de les laisser dans des app par defaut
			f.write("vtaddjob /Nom=%s/%s/%s /Script=%s\n" % (env_name, idfrom_app, idfrom, idfrom_script))
			f.write("vtaddjob /Nom=%s/%s/%s /Script=%s\n" % (env_name, idto_app, idto, idto_script))
		Liste_elem_vu2.append(app_name)
		Liste_elem_vu.append(env_name)
	print "Number of elements processed: %s\n" % nb
	db0.close()
	db1.close()
	db2.close()
	cursor0.close()
	cursor1.close()
	cursor2.close()
	savetab(corrTab, "%s_tab.txt"%fcorname)      # a mettre en fin de script
	saveTabinDB(corrTab,"%s_tab.db"%fcorname)    # a mettre en fin de script
	f.close()
	f2.close()
	f3.close()
	# print dic_env
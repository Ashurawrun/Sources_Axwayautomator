#VERIFIER LES CAS OU ON A PLUSIEURS DOUBLONS DE MOINS DE 16 CHAR
import os, sys, MySQLdb
from myTools import *
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths & database infos
fname            = ''.join( (sys.argv[0]).split('.')[:-1] )
server_name        = config.get('DATABASE', 'db_server') 
database_name        = config.get('DATABASE', 'db_name')
db_username        = config.get('DATABASE', 'db_user')
db_password        = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs      = config.get('PATHS', 'p_logs')
# Default values
default_queue      = config.get('REF', 'default_queue')
typequeue      = config.get('REF', 'typequeue')
queue      = config.get('REF', 'queue')
default_user      = config.get('REF', 'default_user')
default_cal      = config.get('REF', 'default_cal')
default_host      = config.get('REF', 'default_host')


# Connexions to DB
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
	print data
	return data

if __name__ == "__main__":
	query = """SELECT ID_KEY, V_ANAME, T2_ATEARLY, T2_ATLATER, ID_PLNG, ID_USER, ID_AGENT, ID_ENV, V_CYCLE, V_DESC FROM to_obj_app"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	dic_env = {}
	i = 0
	k = 0
	Liste_elem_vu = []
	Liste_elem_vu2 = []
	#-------------------------------------------------------------------------------------------------------------------------
	# si la table de correspondance et le fichier existent deja
	#corr_cpt = 0
	corr_cptapp = 0  # a mettre avant la boucle for
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab          = getTab(fcorrtab)
	corrTab["app"] = []    # a mettre avant la boucle for
	#corrTab["env"] ==> peut etre utilisee pour pacourir les environnements trouves avec le nom vt correspondant

	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	
	lvtom_envnames = getListVTnames("env", corrTab)
	#-------------------------------------------------------------------------------------------------------------------------
	# Creation de fichiers pour contenir les informations.
	fname = os.path.normpath("%s\Crea_app.cmd" % path_res)
	f = open(fname, "w")
	fname2 = os.path.normpath("%s\App_16char.txt" % path_logs)
	f2 = open(fname2, "w")
	fname3 = os.path.normpath("%s\AppAvecProblemesUsers.txt" % path_logs)
	f3 = open(fname3, "w")
	for d in data:
		print "Data = \n", d
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
			print "ok -----------------------------------------------"
			user = user.split('\\')[2]
		desc = str(desc)
		desc = desc.replace("\n", "")
		
		# Env_name = 16 char ou moins
		if len(env_name) > 16:
			f2.write("Nom de l'env depasse 16 char: %s\n" % env_name)
		#	env_name = str(env_name[0:16])
		if env_name in Liste_elem_vu :
			if len(env_name)>= 16: #retirer ce if d'ici et mettre en dessous un if a la place
				f2.write(" /!\\ Environnement vu en double: %s\n" % app_name)
		#		number = format (i, '02d')
		#		env_name = env_name[0:14]+number
		#		i=i+1
		#App_name = 16 char ou moins
		if len(app_name) > 16:
			f2.write("Nom de l'app depasse 16 char: %s\n" % app_name)
		#	app_name = str(app_name[0:16])
		if app_name in Liste_elem_vu2:
			if len(app_name)>= 16: #retirer ce if d'ici et mettre en dessous un if a la place
				f2.write(" /!\\ Application vue en double: %s\n" % app_name)
		#		number = format (k, '02d')
		#		app_name = app_name[0:14]+number
		#		k=k+1
				
		#------ON FORMATE LE NOM DE LENVIRONNEMENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		#automator_envname = env_name
		automator_appname = app_name
		#lvtenvs = getListVTnames("env", corrTab)
		lvtapps = getListVTnames("app", corrTab)
		#vtom_envname = formatObjName(automator_envname, corr_cpt, lvtenvs)
		vtom_appname = formatObjName(automator_appname, corr_cptapp, lvtapps)
		#if (vtom_envname != automator_envname):
		#	corr_cpt += 1
		#	corr = (automator_envname, vtom_envname)
		#	corrTab["env"].append(corr)
		print vtom_appname, "<- vtom_appname et automator_appname->", automator_appname, "\n"
		if (vtom_appname != automator_appname):
			corr_cptapp += 1
			corr = (automator_appname, vtom_appname)
			corrTab["app"].append(corr)
			
		

		#---------------------------------------------------------------------------------------		
		app_name = vtom_appname
		#env_name = vtom_envname
		
		# Creation variable heure debut et heure fin
		d_hmin = str(d_hmin[2:4])+":"+str(d_hmin[4:])+":"+"00"
		d_hmax = str(d_hmax[2:4])+":"+str(d_hmax[4:])+":"+"50"
		
		# Si ce n'est pas cyclique
		if cycle == len(cycle) * cycle[0]:
		# Creation de l'environnement
			f.write("vtaddapp /Nom=%s/%s/Calendar=%s/2015 /Hdeb=%s /Hfin=%s /User=%s /Machine=%s /Queue=%s /Comm=\"%s\"\n" % (env_name, app_name, cal, d_hmin, d_hmax, user, host, queue, desc))
		else:
		# Si c'est cyclique
			if len(cycle)>7:
				if cycle[:2] == cycle[3:5]:
					cycle=cycle[:2]+cycle[5:]
			else:	
				cycle = str(cycle[:2])+":"+str(cycle[2:4])+":"+str(cycle[4:]) 
			f.write("vtaddapp /Nom=%s/%s/Calendar=%s/2015 /User=%s /Machine=%s /Queue=%s /Comm=\"%s\" /Hdeb=%s /Hfin=%s /Cyclique=oui /Cycle=%s \n" % (env_name, app_name, cal,  user, host, queue, desc, d_hmin, d_hmax, cycle))
		Liste_elem_vu2.append(app_name)
		Liste_elem_vu.append(env_name)
	db1.close()
	db2.close()
	cursor1.close()
	cursor2.close()
	savetab(corrTab, "%s_tab.txt"%fcorname)      # a mettre en fin de script
	saveTabinDB(corrTab,"%s_tab.db"%fcorname)    # a mettre en fin de script
	
	f.close()
	f2.close()
	f3.close()
	# print dic_env
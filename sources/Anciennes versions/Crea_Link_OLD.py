#VERIFIER LES CAS OU ON A PLUSIEURS DOUBLONS DE MOINS DE 16 CHAR
import os, sys, MySQLdb
from myTools import *
import ConfigParser
from subprocess import Popen

# Paths & database infos
config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

fname            = ''.join( (sys.argv[0]).split('.')[:-1] )
server_name        = config.get('DATABASE', 'db_server') 
database_name        = config.get('DATABASE', 'db_name')
db_username        = config.get('DATABASE', 'db_user')
db_password        = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs      = config.get('PATHS', 'p_logs')
path_trace      = config.get('PATHS', 'p_trace')
# Default values
default_app      = config.get('REF', 'default_app')
default_script      = config.get('REF', 'default_script')

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
	#print data
	return data

	
	
if __name__ == "__main__":
	query = """SELECT ID, ID_ENV, ID_APP, V_USRNAME, OBJ_FROM, OBJ_TO, LTYPE FROM to_obj_link"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	dic_env = {}
	i = 0
	k = 0
	z = 0
	Liste_elem_vu = []
	Liste_elem_vu2 = []
	print "--------------- Traitement des liens en cours ------------------"
	# Creation de fichiers pour contenir les informations.
	fname = os.path.normpath("%s\Crea_link.cmd" % path_res)
	f = open(fname, "w")
	fname2 = os.path.normpath("%s\link_App_16char.txt" % path_logs)
	f2 = open(fname2, "w")
	for d in data:
		#print "Data = \n", d
		(lien_id, env_name, app_name, lien_name, idfrom, idto, idtype) = d
		dic_env[lien_id]= (lien_name, idfrom, idto, idtype)
		# get real value from to_var table
		if idfrom[0:2] == "AT":
			idfrom = selectData("to_obj_wait", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_wait", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "NW":
			idfrom = selectData("to_obj_notif_wait", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_notif_wait", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "ET":
			idfrom = selectData("to_obj_and", "ID", "V_USRNAME", idfrom) # A VERIFIER (probleme = si le job est lie a une app cas non traite => regarder si ID_APP != "None")
			idfrom_app = selectData("to_obj_and", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "OU":
			idfrom = selectData("to_obj_or", "ID", "V_USRNAME", idfrom)	 # A VERIFIER (probleme = si le job est lie a une app cas non traite => regarder si ID_APP != "None")
			idfrom_app = selectData("to_obj_or", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "AF":
			idfrom = selectData("to_obj_affectation", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_affectation", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "NM":
			idfrom = selectData("to_obj_notif_monitor", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_notif_monitor", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "CM":
			idfrom = selectData("to_obj_command", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_command", "ID", "ID_APP", idfrom)		
		if idfrom[0:2] == "TE":
			idfrom = selectData("to_obj_test_res", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_test_res", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "AB":
			idfrom = selectData("to_obj_abort", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_abort", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "SF":
			idfrom = selectData("to_obj_focal", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_focal", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "ST":
			idfrom = selectData("to_obj_stop", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_stop", "ID", "ID_APP", idfrom)
		if idfrom[0:2] == "JO":	
			idfrom = selectData("to_obj_job", "ID_KEY", "V_JNAME", idfrom)
			idfrom_app = selectData("to_obj_job", "ID_KEY", "ID_APP", idfrom)		
		if idfrom[0:2] == "NA":
			idfrom = selectData("to_obj_notif_auto", "ID", "V_USRNAME", idfrom)
			idfrom_app = selectData("to_obj_notif_auto", "ID", "ID_APP", idfrom)
		if (idfrom[0:2] == "AP"):
			idfrom = selectData("to_obj_app", "ID_KEY", "V_ANAME", idfrom)
		

		# Partie 2:
		if idto[0:2] == "AT":
			idto_app = selectData("to_obj_wait", "ID", "ID_APP", idto)
			idto = selectData("to_obj_wait", "ID", "V_USRNAME", idto)	
		if idto[0:2] == "NW":
			idto_app = selectData("to_obj_notif_wait", "ID", "ID_APP", idto)
			idto = selectData("to_obj_notif_wait", "ID", "V_USRNAME", idto)
		if idto[0:2] == "ET":
			idto_app = selectData("to_obj_and", "ID", "ID_APP", idto)
			idto = selectData("to_obj_and", "ID", "V_USRNAME", idto) # A VERIFIER (probleme = si le job est lie a une app cas non traite => regarder si ID_APP != "None")
		if idto[0:2] == "OU":
			idto_app = selectData("to_obj_or", "ID", "ID_APP", idto)
			idto = selectData("to_obj_or", "ID", "V_USRNAME", idto)	 # A VERIFIER (probleme = si le job est lie a une app cas non traite => regarder si ID_APP != "None")
		if idto[0:2] == "AF":
			idto_app = selectData("to_obj_affectation", "ID", "ID_APP", idto)
			idto = selectData("to_obj_affectation", "ID", "V_USRNAME", idto)
		if idto[0:2] == "NM":
			idto_app = selectData("to_obj_notif_monitor", "ID", "ID_APP", idto)
			idto = selectData("to_obj_notif_monitor", "ID", "V_USRNAME", idto)
		if idto[0:2] == "CM":
			idto_app = selectData("to_obj_command", "ID", "ID_APP", idto)
			idto = selectData("to_obj_command", "ID", "V_USRNAME", idto)
		if idto[0:2] == "TE":
			idto_app = selectData("to_obj_test_res", "ID", "ID_APP", idto)
			idto = selectData("to_obj_test_res", "ID", "V_USRNAME", idto)
		if idto[0:2] == "AB":
			idto_app = selectData("to_obj_abort", "ID", "ID_APP", idto)
			idto = selectData("to_obj_abort", "ID", "V_USRNAME", idto)
		if idto[0:2] == "SF":
			idto_app = selectData("to_obj_focal", "ID", "ID_APP", idto)
			idto = selectData("to_obj_focal", "ID", "V_USRNAME", idto)
		if idto[0:2] == "ST":
			idto_app = selectData("to_obj_stop", "ID", "ID_APP", idto)
			idto = selectData("to_obj_stop", "ID", "V_USRNAME", idto)
		if idto[0:2] == "JO":
			idto_app = selectData("to_obj_job", "ID_KEY", "ID_APP", idto)
			idto = selectData("to_obj_job", "ID_KEY", "V_JNAME", idto)
		if idto[0:2] == "NA":
			idto_app = selectData("to_obj_notif_auto", "ID", "ID_APP", idto)
			idto = selectData("to_obj_notif_auto", "ID", "V_USRNAME", idto)
		if (idto[0:2] == "AP"):
			idto = selectData("to_obj_app", "ID_KEY", "V_ANAME", idto)	
		
		
		if env_name[0:2] != "EB":
			env_name = selectData("to_cenv", "ID_KEY", "ID_ENV", env_name)
		env_name = selectData("to_env", "ID_KEY", "V_ENAME", env_name)
		
		# On va faire des liens entre les app pour eviter les cas ou les jobs ne sont pas dans des apps mais relies a des app
		if str(app_name) == "None": app_name = default_app
		else: app_name = selectData("to_obj_app", "ID_KEY", "V_ANAME", app_name)
		
		#Test des valeurs de idfrom_app et idto_app:
		#print "--idfrom--> ", idfrom, "--idto--> ", idto, "--idfrom_app--> ", idfrom_app, "--idto_app--> ", idto_app, "\n"
		
		# VERIFIER SI CELA CONVIENT (rajouter un booleen garde l'etat au cas ou on veuille relier des jobs dans des apps a d'autres app sans relier les app entre elle X-liens)
		# On donne a tout les jobs une app 
		# Si idfrom_app n'est pas nul chercher son app
		if idto_app != "None": idto_app = selectData("to_obj_app", "ID_KEY", "V_ANAME", idto_app)
		if idfrom_app != "None": idfrom_app = selectData("to_obj_app", "ID_KEY", "V_ANAME", idfrom_app)
		# Si idfrom_app ou idto_app est nul lui donner idfrom en app
		if idto_app == "None": idto_app = str(idto[0:16])
		if idfrom_app == "None": idfrom_app = str(idfrom[0:16])
		
		if str(idto) == "None":
			idto = str(idto_app[0:16])
		if str(idfrom) == "None":
			idfrom = str(idfrom_app[0:16])
		
		#Test des valeurs de idfrom_app et idto_app:
		#print "NEW --idfrom--> ", idfrom, "--idto--> ", idto, "--idfrom_app--> ", idfrom_app, "--idto_app--> ", idto_app, "\n"
		
		#Test pour voir si il est possible qu'un job ne soit pas relie a une app mais que l'on ait un id d'app dans la table
		if((idfrom_app == "None" or idto_app == "None") and str(app_name) != "None"):
			#print "STOP : --idfrom--> ", idfrom, "--idto--> ", idto, "--idfrom_app--> ", idfrom_app, "--idto_app--> ", idto_app, "--app_name--> ", app_name, "\n"
			f2.write("ATTENTION LIEN A PROBLEME !\n ID du lien : %s\n IDFROM %s\n IDTO %s\n NOM DE L'APP %s \n" % (lien_id, idfrom, idto, app_name))
			continue
			#break
		
		# Env_name = 16 char ou moins
		if len(env_name) > 16:
			f2.write("Nom de l'env: %s\n" % env_name)
			env_name = str(env_name[0:16])
		if env_name in Liste_elem_vu :
			if len(env_name)>= 16: #retirer ce if d'ici et mettre en dessous un if a la place
				number = format (i, '02d')
				env_name = env_name[0:14]+number
				i=i+1
		# App_name = 16 char ou moins
		if len(app_name) > 16:
			f2.write("Nom de l'app: %s\n" % app_name)
			app_name = str(app_name[0:16])
		if app_name in Liste_elem_vu2:
			if len(app_name)>= 16: #retirer ce if d'ici et mettre en dessous un if a la place
				number = format (k, '02d')
				app_name = app_name[0:14]+number
				k=k+1
		
		# idfrom = 16 char ou moins
		if len(idfrom) > 16:
			f2.write("Nom de l'idfrom: %s\n" % idfrom)
			idfrom = str(idfrom[0:16])
			
		# idto = 16 char ou moins
		if len(idto) > 16:
			f2.write("Nom de l'idto: %s\n" % idto)
			idto = str(idto[0:16])
		
		script_name = default_script
		
		# On verifie que les jobs sont bien dans une application
		if (app_name == "None" and idfrom_app == "None" or idto_app =="None"):
			f2.write("%s  --appname--> , %s et %s --idfromapp-->, %s et %s idto_app--> %s -- Lien_id\n" % (app_name, idfrom_app, idfrom, idto_app, idto, lien_id))
			#print "STOP 2 -- app_name => ", app_name, "idfrom => ", idfrom, "idto => ", idto, "idto_app => ", idto_app
			break;
		
			
		# Si notre job est dans une application qui n'est pas par defaut
		if (app_name != default_app):
			f.write("vtaddjob /Nom=%s/%s/%s /Script=#F:\\vt-scripts\%s /LienDe=%s/%s/%s[obli]\n" % (env_name, app_name, idfrom, script_name, env_name, app_name, idto))
		# Si notre job risque de ne pas etre dans une application, mettons le dans une application
		else:
			# On commence par traiter idto car idfrom est traite en creant le lien
			f.write("vtaddapp /Nom=%s/%s /Comm=\"Application correspondante au job %s\"\n" % (env_name, idto_app, idto))
			# On creer le lien et on traite idfrom par la meme occasion
			f.write("vtaddapp /Nom=%s/%s /LienDe=%s/%s[obli]\n" % (env_name, idfrom_app, env_name, idto))

			# On place les jobs correspondants dans les app que l'on vient de creer plutot que de les laisser dans des app par defaut
			f.write("vtaddjob /Nom=%s/%s/%s /Script=#F:\\vt-scripts\%s\n" % (env_name, idfrom_app, idfrom, script_name))
			f.write("vtaddjob /Nom=%s/%s/%s /Script=#F:\\vt-scripts\%s\n" % (env_name, idto_app, idto, script_name))
		Liste_elem_vu2.append(app_name)
		Liste_elem_vu.append(env_name)
	#TEST
	db1.close()
	db2.close()
	cursor1.close()
	cursor2.close()
	f.close()
	f2.close()
	# print dic_env
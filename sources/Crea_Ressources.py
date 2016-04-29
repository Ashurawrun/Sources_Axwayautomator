import os, sys, MySQLdb
import exceptions
import traceback
import ConfigParser
from myTools import *
from subprocess import Popen

config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths, file & database infos

server_name      = config.get('DATABASE', 'db_server') 
database_name    = config.get('DATABASE', 'db_name')
db_username      = config.get('DATABASE', 'db_user')
db_password      = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs        = config.get('PATHS', 'p_logs')
path_trace       = config.get('PATHS', 'p_trace')
fname            = os.path.normpath("%s\Crea_Ressources" % path_res)
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
	return data

if __name__ == "__main__":
	query = """SELECT ID_KEY, N_RTYPE, V_RNAME, V_DESC, V_VALUE, N_MAXVALUE FROM cf_gres"""
	lines = cursor2.execute(query)
	data = cursor2.fetchall()
	# get the number of rows in the resultset
	numrows = int(cursor2.rowcount)
	dic_env = {}
	nb = 0
	print "--------------- Processing of environments ---------------\n"
	#-----------------------------------------------------------------------------------------------------------------------
	corr_cpt = 0  # a mettre avant la boucle for
	fcorname              = "correspondances"    # a mettre avant la boucle for
	fcorrtab              = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab               = getTab(fcorrtab)
	
	corrTab["ressources"] = []    # a mettre avant la boucle for
	
	fcorname              = "correspondances"    # a mettre avant la boucle for
	fcorrtab              = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	
	#-----------------------------------------------------------------------------------------------------------------------
	# Creation de fichiers pour contenir les informations.
	f = open(fvtcmd, "w")
	fname2 = os.path.normpath("%s\Ressources_16char.txt" % path_logs)
	f2 = open(fname2, "w")
	fname4 = os.path.normpath("%s\Log_Ressources" % path_trace)
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
		#print "Data = \n", d
		(ress_id, ress_type, ress_name, ress_desc, ress_value, ress_maxvalue) = d
		dic_env[ress_id]= (ress_name, ress_desc, ress_value)
		
		# get the name from the right table
		if ress_desc == "None": ress_desc = ""
		if ress_value == "None": ress_value = ""
		if ress_maxvalue == "None": ress_maxvalue = ""
		
		# Changement des valeurs pour qu'elles soient adaptees a vtom
		ress_value = str(ress_value)
		ress_value = ress_value.replace("*", "")
	
		# 16 char problems		
		if len(ress_name) > 16:
			f2.write("Nom de la ressource depasse 16 char : %s\n" % ress_name)
			ress_name = getVTname (ress_name, corrTab, 'ressources')
		if ress_type == '1':
			ress_type = "poi"
		if ress_type == '2':
			ress_type = "tex"

		#-------------ON FORMATE LE NOM DE LA RESSOURCE SI NON CONFORME A VTOM -----------------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.
		automator_ressname = ress_name
		lvtress = getListVTnames("ressources", corrTab)
		(vtom_ressname, isnum) = formatObjName(automator_ressname, corr_cpt, lvtress)
		if ((vtom_ressname != automator_ressname) and isnum):
			corr_cpt += 1
			corr = (automator_ressname, vtom_ressname)
			corrTab["ressources"].append(corr)
		elif ((vtom_ressname != automator_ressname) and not isnum): 
			corr = (automator_ressname, vtom_ressname)
			corrTab["ressources"].append(corr)

		#---------------------------------------------------------------------------------------

		# Creation de l'environnement
		f.write("vtaddres /name %s /type %s /value=%s\n" % (vtom_ressname, ress_type, ress_value))
	print "Number of elements processed: %s\n" % nb
	db1.close()
	db2.close()
	cursor1.close()
	cursor2.close()
	savetab(corrTab, "%s_tab.txt"%fcorname)      # a mettre en fin de script
	saveTabinDB(corrTab,"%s_tab.db"%fcorname)    # a mettre en fin de script
	f.close()
	f2.close()
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
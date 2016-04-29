# -*- coding: latin-1 -*-
import os, sys, MySQLdb
import ConfigParser
from myTools import *
from subprocess import Popen

# Paths & database infos
config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')


server_name     = config.get('DATABASE', 'db_server') 
database_name   = config.get('DATABASE', 'db_name')
db_username     = config.get('DATABASE', 'db_user')
db_password     = config.get('DATABASE', 'db_pass') 
path_res        = config.get('PATHS', 'p_reslt')  
path_tmp        = config.get('PATHS', 'p_tmp')
path_logs       = config.get('PATHS', 'p_logs')
path_trace      = config.get('PATHS', 'p_trace')
fname            = os.path.normpath("%s\Crea_Agents" % path_res)
fvtcmd           = os.path.join(path_res ,  "%s.cmd"%fname)

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

if __name__ == "__main__":
	#-------------------------------------------------------------------------------------------------------------------------
	# si la table de correspondance et le fichier existent deja
	#corr_cpt = 0
	corr_cptagt = 0  # a mettre avant la boucle for
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab          = getTab(fcorrtab)
	corrTab["agt"]   = []    # a mettre avant la boucle for
	#-----------------------------------------------------------------------------------------------------------------------
	# connect
	db = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
	cursor = db.cursor()
	# execute SQL select statement
	query = """SELECT M_HNAME, V_DESC FROM cf_agt"""
	
	# j'ouvre mon fichier texte en mode écriture
	f = open(fvtcmd, "w")
	fname2 = os.path.normpath("%s\Log_agent" % path_trace)
	flog = open(fname2, "w")
	print "--------------- Processing of agents ------------------\n"
	nb = 0
	lines = cursor.execute(query)
	data = cursor.fetchall()
	# get the number of rows in the resultset
	numrows = int(cursor.rowcount)
	# get and display one row at a time.
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
		(host_name, desc) = d
		# Get host from our dictionary
		if len(host_name) > 16:
			host_name = getVTname(host_name, corrTab, 'agt')
		#------ON FORMATE LE NOM DE L'AGENT SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_hostname = host_name
		lvtagts = getListVTnames("agt", corrTab)
		(vtom_hostname,isnum) = formatObjName(automator_hostname, corr_cptagt, lvtagts)

	
		if ((vtom_hostname != automator_hostname) and isnum):
			#print vtom_hostname, "<- vtom_hostname et automator_hostname->", automator_hostname, "\n"
			corr_cptagt += 1
			corr = (automator_hostname, vtom_hostname)
			corrTab["agt"].append(corr)
		elif ((vtom_hostname != automator_hostname) and not isnum): 
			corr = (automator_hostname, vtom_hostname)
			corrTab["agt"].append(corr)
		
		#---------------------------------------------------------------------------------------
		host_name = vtom_hostname
		
		f.write("vtaddmach /machine %s /comment=\"%s\"\n" % (host_name, desc))
	print "Number of elements processed: %s\n" % nb
	f.close()
	cursor.close()
	db.close()
	savetab(corrTab, "%s_tab.txt"%fcorname)      # a mettre en fin de script
	saveTabinDB(corrTab,"%s_tab.db"%fcorname)    # a mettre en fin de script
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
	print "------------ End of processing for agents ------------\n"
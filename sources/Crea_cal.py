# -*- coding: latin-1 -*-
import os, sys, MySQLdb
import ConfigParser
from myTools import *
from subprocess import Popen

# Paths & database infos
config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')


server_name        = config.get('DATABASE', 'db_server') 
database_name      = config.get('DATABASE', 'db_name')
db_username        = config.get('DATABASE', 'db_user')
db_password        = config.get('DATABASE', 'db_pass') 
path_res           = config.get('PATHS', 'p_reslt')  
path_tmp           = config.get('PATHS', 'p_tmp')
path_logs          = config.get('PATHS', 'p_logs')
path_trace         = config.get('PATHS', 'p_trace')
fname              = os.path.normpath("%s\Crea_cal" % path_res)
fvtcmd             = os.path.join(path_res ,  "%s.cmd"%fname)

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
	corr_cpt = 0  # a mettre avant la boucle for
	fcorname         = "correspondances"    # a mettre avant la boucle for
	fcorrtab         = os.path.join(path_tmp,"%s_tab.db"%fcorname)	 # a mettre avant la boucle for
	corrTab          = getTab(fcorrtab)
	corrTab          = {}   # a mettre avant la boucle for
	corrTab["cal"]   = []    # a mettre avant la boucle for
	#-----------------------------------------------------------------------------------------------------------------------
	# connect
	db = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
	cursor = db.cursor()

	# execute SQL select statement (SELECT CALENDARS ONLY > YEAR 2015)
	query = """SELECT V_CNAME, Y_YEAR, N_HWEEK, cf_cal.V_DESC FROM cf_cal INNER JOIN cf_caly ON cf_cal.ID_KEY = cf_caly.ID_CAL WHERE cf_caly.Y_YEAR >= 2015"""


	# j'ouvre mon fichier texte en mode écriture
	f = open(fvtcmd, "w")
	fname2 = os.path.normpath("%s\Log_cal" % path_trace)
	flog = open(fname2, "w")
	print "--------------- Processing of calendars ---------------\n"
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
		(cal, cal_year, Week_format, desc) = d
		t4 = Week_format.replace("3", "w")
		Week_format = t4.replace("4", "h")
		# Get cal from our dictionary
		if len(cal) > 16:
			cal = getVTname (cal, corrTab, 'cal')
		#------ON FORMATE LE NOM DU CALENDRIER SI NON CONFORME A VTOM ---------
		# REMARQUE: ici on cree la table de correspondance pour les environnements c'est pour ca qu'on l'initalise 
		# a vide corrTab=  {}     et corrTab["env"]   =  []    si on utilise la table de correspondance dans un autre script
		# et que cette derniere est deja remplie => on ouvre le fichier de correspondance, ca suffit.

		automator_calname = cal
		lvtcals = getListVTnames("cal", corrTab)
		(vtom_calname,isnum) = formatObjName(automator_calname, corr_cpt, lvtcals)

		if ((vtom_calname != automator_calname) and isnum):
			#print vtom_calname, "<- vtom_calname et automator_calname->", automator_calname, "\n"
			corr_cpt += 1
			corr = (automator_calname, vtom_calname)
			corrTab["cal"].append(corr)
		elif ((vtom_calname != automator_calname) and not isnum): 
			corr = (automator_calname, vtom_calname)
			corrTab["cal"].append(corr)
		#---------------------------------------------------------------------------------------
		cal = vtom_calname
		
		f.write("vtaddcal -n %s -y %s /daysInWeek=%s\n" % (cal, cal_year, Week_format))
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
	print "------------ End of processing for calendars ------------\n"
# -*- coding: latin-1 -*-
import os, sys, MySQLdb
import ConfigParser
from myTools import *
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
fname            = os.path.normpath("%s\Crea_Date_env" % path_res)
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
	# connect
	db = MySQLdb.connect(host="%s" % server_name, user="%s" % db_username, passwd="%s" % db_password, db="%s" % database_name)
	cursor = db.cursor()

	# execute SQL select statement
	cursor.execute("SELECT ID_KEY, V_ENAME FROM axwayautomator_ms.to_env ORDER BY ID_KEY")

	# commit your changes
	db.commit()

	# get the number of rows in the resultset
	numrows = int(cursor.rowcount)

	# j'ouvre mon fichier texte en mode écriture
	f = open(fvtcmd, "w")
	fname2 = os.path.normpath("%s\date_env_16char.txt" % path_logs)
	f2 = open(fname2, "w")
	fname3 = os.path.normpath("%s\Log_date" % path_trace)
	flog = open(fname3, "w")

	print "--------------- Processing of dates ------------------\n"
	# variables pour gerer doublons
	Liste_elem_vu = []
	Liste_dates_vues = []
	i = 0
	l = 0
	nb = 0
	# get and display one row at a time.
	for x in range(0,numrows):
		nb += 1
		row = cursor.fetchone()
		# tester si les chaines font plus de 16 char, si oui,
		# tronquer row[1] pour qu'il fasse 14 char auquel on ajoute
		if len(str(row[1])) > 16:
			f2.write("%s\n" % row[1])
			Nom_env = str(row[1][0:16]) 
		else:
			Nom_env = str(row[1])
		for j in range(len(Liste_elem_vu)):
			if Liste_elem_vu[j]== Nom_env:
				if len(Nom_env)>= 16: #retirer ce if d'ici et mettre en dessous un if à la place
					number = format (i, '02d')
					Nom_env = Nom_env[0:14]+number
					i=i+1
		##############################################################
		#Règlement des problèmes de dates
		Id_Date = "d_"+Nom_env[:14]
		for k in range(len(Liste_dates_vues)):
			if Liste_dates_vues[k]== Id_Date:
				if len(Id_Date)>= 16: #retirer ce if d'ici et mettre en dessous un if à la place
					number = format (l, '02d')
					Id_Date = Id_Date[0:14]+number
					l=l+1
					f2.write("DATE = %s\n" % Id_Date)
		f.write("vtadddate /Name %s -p non\n" % (Id_Date))
		Liste_elem_vu.append(Nom_env)
		Liste_dates_vues.append(Id_Date)
	print "Number of elements processed: %s\n" % nb
	#Fermer tout les fichiers
	cursor.close()
	db.close()
	f.close()
	f2.close()
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
	print "------------ End of processing for dates ------------\n"
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
fname            = os.path.normpath("%s\Crea_Queue" % path_res)
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
	cursor.execute("SELECT cf_sys_type.NAME FROM %s.cf_sys_type WHERE %s.cf_sys_type.TYPE in (select distinct V_SYSTYPE from %s.cf_agt)" % (database_name, database_name, database_name))

	# commit your changes
	db.commit()

	# get the number of rows in the resultset
	numrows = int(cursor.rowcount)

	# j'ouvre mon fichier texte en mode ecriture
	f = open(fvtcmd, "w")
	fname2 = os.path.normpath("%s\Log_queue" % path_trace)
	flog = open(fname2, "w")
	
	print "--------------- Processing of queue ------------------\n"

	dic_OS = {}
	dic_OS = {'wnt': (('Windows NT', 'Windows Server 2008 R2'), 'queue_wnt'), 
	'Linux': (('IBM AIX', 'Linux', 'HPUX', 'Sun SOLARIS', 'DecUnix'), 'queue_ksh'), 
	'AS400': (('IBM OS400'), 'queue_as400'), 'GCOS7': (('GCOS7'), 'queue_gcos7'), 
	'GCOS8': (('GCOS8'), 'queue_gcos8'), 'MVS': (('MVS'), 'queue_mvs'), 
	'Autre': (('Unknown', 'UNISYS', 'VMS', 'SCO', 'IRIX', 'Netware'), 'queue_unknown')}
	Queue = "queue_unknown"
	nb = 0
	# get and display one row at a time.
	for x in range(0,numrows):
		nb += 1
		row = cursor.fetchone()
		Type_OS = str(row[0])
		Type_OS = Type_OS.replace("/", "")
		for i in dic_OS.values():
			if Type_OS in i[0]:
				Queue = i[1] 
		#Print des valeurs obtenues dans le cmd
		#print "%s" % (Type_OS), "-->", Queue, "\n"
		
		f.write("vtaddqueue /name %s\n" % (Queue))	
	#Fermer tout les fichiers
	print "Number of elements processed: %s\n" % nb
	cursor.close()
	db.close()
	f.close()
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
	print "------------ End of processing for queues ------------\n"
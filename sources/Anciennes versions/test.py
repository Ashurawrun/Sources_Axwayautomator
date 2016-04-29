import os, sys, MySQLdb
import exceptions
import traceback
import ConfigParser
from myTools import *
from subprocess import Popen

config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths, file & database infos
fname            = ''.join( (sys.argv[0]).split('.')[:-1] )
server_name      = config.get('DATABASE', 'db_server') 
database_name    = config.get('DATABASE', 'db_name')
db_username      = config.get('DATABASE', 'db_user')
db_password      = config.get('DATABASE', 'db_pass') 
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs        = config.get('PATHS', 'p_logs')
path_trace       = config.get('PATHS', 'p_trace')

fvtcmd           = os.path.join(path_res ,  "%s.cmd"%fname)

# Default values
default_queue    = config.get('REF', 'default_queue')
typequeue        = config.get('REF', 'typequeue')
queue            = config.get('REF', 'queue')
default_user     = config.get('REF', 'default_user')
default_cal      = config.get('REF', 'default_cal')
default_host     = config.get('REF', 'default_host')
default_app      = config.get('REF', 'default_app')

fname = os.path.normpath("%s\Env_sans_app.txt" % path_res)
f = open(fname, "r")
fname = os.path.normpath("%s\Env_sans_app.txt" % path_res)
f = open(fname, "r")
def isStringInFile(mystring):	
	mystring = mystring + "\n" # to avoid finding a string name inside a bigger string
	for line in f:
		if mystring in line:
			print "true"
			return True
	print "false"
	return False

if __name__ == "__main__":
	env_name = 'DISPATCH_SPOOLS'
	isStringInFile(env_name)
f.close()
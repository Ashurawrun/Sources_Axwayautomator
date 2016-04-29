# N'ecrire que les lignes avec des CAIXA_SOIR et des DISPATCH_SPOOLS_
import os, sys, MySQLdb
import ConfigParser
import string


config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')

# Paths & database infos
path_res         = config.get('PATHS', 'p_reslt')  
path_tmp         = config.get('PATHS', 'p_tmp')
path_logs        = config.get('PATHS', 'p_logs')
path_trace       = config.get('PATHS', 'p_trace')


if __name__ == "__main__":
	# Quel environnement/application/job choisir pour limiter les creations?
	looking_for = ['Nom=CAIXA_SOIR/', 'PASNom=DISPATCH_SPOOLS_']
	
	fname = os.path.normpath("%s\Crea_app.cmd" % path_res)
	fname2 = os.path.normpath("%s\Crea_app_Light.cmd" % path_res)
	oldfile = open(fname, "r")
	newfile = open(fname2, 'w')
	for line in oldfile:
		if not any(looking_for in line for looking_for in looking_for):
			continue
		else: newfile.write(line)
	oldfile.close()
	newfile.close()
	
	fname = os.path.normpath("%s\Crea_Job.cmd" % path_res)
	fname2 = os.path.normpath("%s\Crea_job_Light.cmd" % path_res)
	oldfile = open(fname, "r")
	newfile = open(fname2, 'w')
	for line in oldfile:
		if not any(looking_for in line for looking_for in looking_for):
			continue
		else: newfile.write(line)
	oldfile.close()
	newfile.close()
	
	fname = os.path.normpath("%s\Crea_link.cmd" % path_res)
	fname2 = os.path.normpath("%s\Crea_link_Light.cmd" % path_res)
	oldfile = open(fname, "r")
	newfile = open(fname2, 'w')
	for line in oldfile:
		if not any(looking_for in line for looking_for in looking_for):
			continue
		else: newfile.write(line)
	oldfile.close()
	newfile.close()
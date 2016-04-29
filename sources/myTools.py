import os, sys, re
import ConfigParser
import traceback
import unicodedata
import shelve
import subprocess as sub


config = ConfigParser.ConfigParser()
config.read('../migrationautomator.cfg')
path_tmp     = config.get('PATHS', 'p_tmp')
fvartab      = os.path.join(path_tmp, "var_tab.db")
fmaintab     = os.path.join(path_tmp, "main_tab.db")
carsNok      = "[?*!#/\{}();^:, &%=\"'`]"
carsDifOk    = "[^0-9a-zA-Z.+-_$]" # pour exprimer les caracteres accentues
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[00;32m'
WARNING = '\033[00;33m'
FAIL = "\033[00;31m" #'\033[91m'
ENDC = '\033[00m'
BOLD = "\033[01m"
vartab       = {} # dictionnaire des variables TWS
maintab      = {} # dictionnaire des variables Main TWS

class QueueException:
    """Base class for exceptions in this module."""
    pass

class ResException:
    """Base class for exceptions in this module."""
    pass

class CfgException:
    """Base class for exceptions in this module."""
    pass

class ChkEnvException:
    """Base class for exceptions in this module."""
    pass

class VTCmdException:
    """Base class for exceptions in this module."""
    pass

def disable():
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''

def infog( msg):
    print OKGREEN + msg + ENDC

def info( msg):
    print OKBLUE + msg + ENDC

def warn( msg):
    print WARNING + msg + ENDC

def err( msg):
    print FAIL + msg + ENDC

def unaccent(str):
        return unicodedata.normalize('NFKD', str).encode('ascii','ignore')

def savetab(tab, fname):
        global path_tmp
        if not os.path.isdir(path_tmp):
                os.system("mkdir %s"%path_tmp)
        f = open( os.path.join(path_tmp, fname), "w")
        f.write("%s" % tab)
        f.close()

def saveTabinDB(tab, fname):
        db = shelve.open(os.path.join(path_tmp, fname))
        try:
                db['tab'] = tab
        finally:
                db.close()

def getTab(f):
        res = shelve.open(f, "r")
        tab = res['tab']
        res.close()
        return tab

def find(exp, s):
        regexp = re.compile(exp)
        res = len(regexp.findall(s))
        return res

def findall(exp, s):
	#print "chaine recue : %s" %s
	regexp = re.compile(exp)
	res = regexp.findall(s)
	return res


	
	
#c = nom automator, tab=nom tab correspondance, type=app/env/job...
def getVTname(c, tab, type):
	name=c
	if type in tab.keys():
		for (a, b) in tab[type]:
			if (a==c):
				name= b
				break
	else:
		err("type [%s] not found in matching table"%type) 
		raise ResException
	return name

def getListVTnames(type, tab):
        if not(type in tab.keys()):
                l = []
        else:
                l = [ b for (a,b) in tab[type]]
        return l

def SizeOk(s):
        if len(s) <= 16:
                res=True
        else:
                res=False
        return res

def CharsOk(obj):
	global carsNok, carsDifOk 
	# Si le nom contient un des caracteres suivants : ?, *, !, #, etc...
	# OU un caractere autre que ceux autorises
	if ( find(carsNok, obj) != 0 ) or ( find(carsDifOk, obj) != 0 ): 
		res=False
	else: # nom conforme
		res=True
	return res

def formatObjName(obj, cpt, lvtom):
	global carsNok, carsDifOk
	isnum = False
	if not CharsOk(obj):
		objname = re.sub(carsNok, "", obj)
		#objname = objname.replace(" ","")
		objname = re.sub(carsDifOk, "", objname)
		obj = objname
	if not SizeOk(obj):
		obj=obj[:16]
		if obj in lvtom:
			objname1 = obj[:- (len(str(cpt))+1)]
			#print objname1
			objname2 = str(cpt)
			#print objname2
			obj = "%s_%s" % (objname1, objname2)
			isnum = True
	return (obj, isnum) #obj

def getVTname(c, tab, type):
        name=c
        if type in tab.keys():
                for (a, b) in tab[type]:
                        if (a==c):
                                name= b
                                break
        return name

def addpResPefix(type, name):
	if type=="w":
		newname= "rw_"+name
	if type=="f":
		newname="rf_"+name
	if type=="g":
		newname="rg_"+name
	return newname

def formatResName(obj, cpt, lvtom):
        global carsNok, carsDifOk
	twsobj=obj
        if not CharsOk(obj):
                objname = re.sub(carsNok, "", obj)
                #objname = objname.replace(" ","")
                objname = re.sub(carsDifOk, "", objname)
                obj = objname
        if not SizeOk(obj):
                obj=obj[:16]
                if obj in lvtom:
                        objname1 = obj[:- (len(str(cpt))+1)]
                        #print objname1
                        objname2 = str(cpt)
                        #print objname2
                        obj = "%s_%s" % (objname1, objname2)
        return obj

def execVtomCmd(file, flog):
	f = open(file, "r")
	lines = f.readlines()
	msg = "- Executing VTOM commands"
	flog.write("%s\n" % msg)
	print "%s"%msg
	for line in lines:
		line = line.replace("\n", "")
		# si la ligne n'est pas un echo 
		if not find("^echo", line):
			#flog.write("%s\n" %line)
			p = sub.Popen(line, stdout=sub.PIPE, stderr=sub.PIPE, shell=True )
			output, stderr = p.communicate()
		if (("Modifcation" in output) or ("Rattachement" in output) or ("Application inconnue" in stderr) or ("Source du Lien inconnu" in stderr) or ("Cible du Lien inconnu" in stderr) or ("cycle detecte" in stderr)): 
			warn("****** Warning ******\n")
			msg = "CMD : %s\nOUTPUT : %s\nSTDERR : %s\n"%(line, output, stderr)
			flog.write("%s\n" % msg)
			warn(msg)
		elif (("termine" in output)): pass
		elif ((len(output) != 0) or (len(stderr) != 0)):
			err("****** Error ******\n")
			msg = "CMD : %s\nOUTPUT : %s\nSTDERR : %s\n"%(line, output, stderr)
			flog.write("%s\n" % msg)
			err(msg)
			raise VTCmdException 
	msg = "- Objects created with success"
	flog.write("%s\n" % msg)
	print "%s"%msg	
	f.close()

def writeCorrFile(lcorr, msg, fct, file):
        len_corrTab = len(lcorr)
        if len_corrTab == 0 :
                file.write("- %s name matching: %d\n" %(msg, len_corrTab))
        if len_corrTab > 0:
                fct("- %s name matching: %d" %(msg, len_corrTab))
                fct("  NomTWS\t\t\tNomVTOM")
		cptcorr=0
                for (tws_app, vtom_app) in lcorr:
			cptcorr+=1
			if (cptcorr <= 15):
				fct("  %s\t\t%s" %(tws_app, vtom_app))
			elif (cptcorr == 31):
				if not ("File res" in msg) and not ("Generic res" in msg):
					warn(" ...\n")
				file.write("  %s\t\t%s\n" %(tws_app, vtom_app))
			else: 
				file.write("  %s\t\t%s\n" %(tws_app, vtom_app))
                fct("\n")

def getVarValue(param):
	global vartab, maintab 
	if (len(vartab.keys()) == 0) :
		vartab = getTab(fvartab)
	if (len(maintab.keys()) == 0):
		maintab = getTab(fmaintab)
		#print "len(vartab) = %d  | len(maintab) = %d"%( len(vartab.keys()), len(maintab.keys())) 
        if param in vartab.keys(): 
			#print "la variable est dans la table des variables"
			value=vartab[param]
        else:
                if param in maintab.keys(): 
					#print "la variable est dans la main table"
					value=maintab[param]
                else:   
					# la variable ne se trouve ni dans la table 
					# des variables ni la main table
					#print "variable %s ni dans vartab ni maintab"%param 
                    value="NONE"
        return value

def getResFinfos(l):
	# prend en entrre une ligne OPENS
	# et renvoie :
	#  - le host de la ress fichier
	#  - le nom tws de la ress fichier
	#exemple:
	# l = OPENS EXPLOIT1#"^ITRANSFERT^/import/vyaaaaw0.vy"
	# ou
	# l = OPENS F5BWA#"^ITRANSFERT^/import/lza0waaa.f5" (-f %p)
	l=l.replace("OPENS", "")
	l=l.replace("\n", "")
	[host,file] = l.split("#\"")
	host = host.replace(" ", "")
	fpath = (file.split("\"")[0]).replace(" ", "")
	cond = file.split("\"")[1]
	type="resf"
	if find("\^", fpath):
		param=fpath.split("^")[1]
		if param == "ITRANSFERT":
			valparam="/transfert"
			host="cft"
		else:
			valparam=getVarValue(param)
		fpath=fpath.replace("^%s^"%param, valparam)		

	fname = ( ( fpath.replace("\\", ",") ).replace("/", ",") ).split(",")[-1]
	if find("([ ]*[!]*[ ]*-f[ ]*%p[ ]*/[a-zA-Z0-9.]+[ ]*)", cond):
		fname = cond.split("/")[1]
		fname = fname.replace(")","")
		if fpath.count("/") != 0:
			fpath = fpath+"/"+fname
		else:
			fpath = fpath+"\\"+fname
	elif find("[ ]*-[ao]{1} [ ]*-[sf]{1}", cond):
		# ressource generique on ignore
		if find("[ ]*-a", cond):
			type="resg"
			#fname="f_notnull"
		else:
			type="resgor"
			#fname="f1_or_f2"
	return (host, fpath, fname, type)


def updateJobsDic(dic, lj, la):
	for twsjobname in lj:
		#print "TWSJOBNAME = %s"%twsjobname
		if twsjobname in dic.keys():
			#print "job trouev dans dic"
			l = dic[twsjobname]
			l.extend(la)
			dic[twsjobname] = l
			#print "dic[twsjobname] = ", dic[twsjobname]
		else:	
			dic[twsjobname] = la
			#print "JOB rajoute dans dic : dic[twsjobname] = ", dic[twsjobname]
	return dic

	 

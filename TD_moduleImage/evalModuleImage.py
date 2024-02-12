#!/usr/bin/python3
import os
import shutil
import sys
from sys import platform
import tarfile
import subprocess
import glob
import re
import csv
import random

###          OPTIONS D'EVALUATION       ###
MODES = ["ETU", "PROF"]
MODE = "ETU"

###          AUTRES OPTIONS             ###
VIEWER = 'display'      # visualiseur d'images (display / eog)
EDITOR = 'gedit'        # gedit / code / ... tout éditeur de texte peut faire l'affaire
if platform == 'darwin':    # sous MacOS la commande open ouvre l'app par défaut
    VIEWER = 'open'
    EDITOR = 'open'

######################################################################################################################""
###          FONCTIONNALITES            ###
def msg(pb, penalite=0, sep='', end='\n'):
    global NOTE
    global RETOUR
    if penalite == 0:
        txt = pb
    else:
        txt = "PROBLEME : " + pb + ". J'enleve " + str(round(penalite, 2)) + " points."
    print(txt, sep=sep, end=end)
    if NOTE > 0:
        NOTE = max(round(NOTE - penalite, 2), 0)
    RETOUR = RETOUR + txt + end


def isdir(thefile):
    return os.path.isdir(thefile)


def isfile(thefile):
    return os.path.isfile(thefile)


def listfiles(a):
    if isdir(a):
        l = []
        files = glob.glob(a + "/*")
        for f in files:
            l.extend(listfiles(f))
        return l
    elif isfile(a):
        nom_complet = a.split("/")[-1]
        chemin = "/".join(a.split("/")[0:-1])
        nom = nom_complet.split(".")[0]
        if "." in nom_complet:
            ext = ".".join(nom_complet.split(".")[1:])
        else:
            ext = ""
        return [{"f": a, "nom": nom, "ext": ext, "nc": nom_complet, "ch": chemin}]
    else:
        return []


def rmfiles(thedir):
    if isdir(thedir):
        # files = glob.glob(thedir + "/*")
        # for f in files:
        #    rmfiles(f)
        # os.rmdir(thedir)
        shutil.rmtree(thedir, ignore_errors=True)  # fonctionne meme s'il y a des fichiers caches
    else:
        if isfile(thedir):
            os.remove(thedir)


def filesize(read, enco="utf-8"):
    if read != "":
        en = enco
        # en = "latin1"
        try:
            fs = open(read, 'r', encoding=en)
            texte = fs.read()
        except UnicodeDecodeError:
            en = "latin1"
        except Error as exc_ret:
            raise (exc_ret)
        finally:
            fs.close()
        fs = open(read, 'r', encoding=en)
        texte = fs.read()
        longueur = len(texte)
        fs.close()
        return longueur
    else:
        return 0


def filein(lst):
    read = ""
    for rm in lst:
        if isfile(rm):
            read = rm
    return read


def count_in_file(f, word):
    if isfile(f):
        with open(f, 'r', errors='ignore') as fs:
            texte = fs.read()
            n = texte.count(word)
            fs.close()
        return n
    else:
        return 0


def replace_in_file(fin, fout, wordin, wordout):
    if isfile(fin):
        texte = ''
        with open(fin, 'r', errors='ignore') as fs:
            texte = fs.read()
            texte = texte.replace(wordin, wordout)
            fs.close()
        with open(fout, 'w', errors='ignore') as fs:
            fs.write(texte)
            fs.close()


def is_filedates_ok(filedates, filemodif):
    ok = True
    for f, lm in filedates.items():
        if isfile(f):
            lastModif = os.stat(f).st_mtime_ns
            changed = lastModif != lm
            filedates[f] = lastModif
            if f in filemodif:
                ok = ok and (filemodif[f] == changed)
    return ok


def is_dep_ok(f, filedates, filemodif):
    if isfile(f):
        os.utime(f)
    make_process = subprocess.run(['make'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ok = is_filedates_ok(filedates, filemodif)
    msg('Modif de ' + f + ', recompilation ' + {True: 'ok', False: 'pas ok'}[ok])
    msg("stdout:")
    msg(make_process.stdout.decode("utf-8", "ignore"))
    return ok


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def utilisateur_demande(msgInvit, info):
    preced = persiste_arch_val(info, 'rstr')
    reponse = ''
    while reponse == '':
        reponse = input(msgInvit + ' ? (precedemment:' + preced + ')')
        if reponse == '' and preced != 'None' and preced != '':
            reponse = preced
    persiste_arch_val(info, 'w', reponse)
    return reponse


def utilisateur_evalue(msgInvit, msgPb, penalite, echelle='oui/non'):
    # echelle predefinie dans la liste ci-dessous,
    # ou echelle personnalisee, e.g., utilisateur_evalue('...ok', 'pas bon', 0.5, ['i', '-m', 'm', 'ab', 'b'])
    # l'utilisateur peut falcutativement ajouter un commentaire en le separant de l'appreciation avec '#'
    # par exemple : ...$ readme ok (n/n+/m-/m/m+/o-/o) ? o-#manquent les noms et numeros d'etudiants
    echelles = {
        'oui/non': ['n', 'o'],
        'ech3': ['n', 'm', 'o'],
        'ech7': ['n', 'n+', 'm-', 'm', 'm+', 'o-', 'o']}
    if str(echelle) in echelles:
        ech = echelles[echelle]
    else:
        ech = echelle
    evaluation = ''
    while evaluation not in ech:
        preced = persiste_arch_val(msgInvit, 'rstr')
        reponse = input(msgInvit + ' (' + '/'.join(ech) + ') ? (precedemment:'
            + preced + ') ')
        if reponse == '' and preced != 'None' and preced != '':
            reponse = preced
        message = msgPb
        evaluation = reponse
        if '#' in reponse:
            message += ' / ' + reponse.split('#')[1]
            evaluation = reponse.split('#')[0]
        if evaluation in ech[0:-1]:
            msg(message, penalite * ((len(ech) - 1 - ech.index(evaluation)) / (len(ech) - 1)))
        if evaluation in ech:
            persiste_arch_val(msgInvit, 'w', reponse)


def persiste_arch_val(champ_in, action='r', valeur_in=None):
    champs = ['nomArchive', 'nomFichier', 'numsEtu', 'repPrinc', 'note',
        'image1 ok', 'image2 ok', 'affichage image ok', 'zoom/dezoom ok', 'readme ok', 'erreurs code penalite', 'erreurs code detail']
    return persiste_valeur('../eval_archives.csv', champs, NOM_ARCHIVE, champ_in, action, valeur_in)



def persiste_etu_val(num_etu, champ_in='note', action='w', valeur_in=None):
    champs = ['numEtu', 'note']
    return persiste_valeur('../eval_etudiants.csv', champs, num_etu, champ_in, action, valeur_in)


# persite dans le fichier csv 'nom_fichier' pour la ligne identifiee par la clef 'clef'
# une valeur 'valeur_in' d'un champ 'champ_in' parmi le schema defini dans 'champs'
# le premier champ de 'champs' est la clef des lignes du fichier csv
# le fichier csv est editable avec un tableur type Excel avec separateur=tabulation
# parametre 'action' : 'r' lire la valeur du champ, 'rstr' lire+convertir en chaîne, 'w' mettre a jour
# meme si fichier ou ligne absente, toute action creee le fichier et la ligne (avec des valeurs vides)
def persiste_valeur(nom_fichier, champs, clef, champ_in, action='r', valeur_in=None):
    if champ_in not in champs:
        raise (Exception('ERREUR : champ "' + champ_in
                         + '" non present parmi les champs du fichier csv ' + nom_fichier))
    else:
        clef_champ = champs[0]
        clef_valeur = clef
        # creation si besoin fichier csv vide
        if not isfile(nom_fichier):
            with open(nom_fichier, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=champs, dialect='excel-tab', quoting=csv.QUOTE_NONE)
                writer.writeheader()
            csvfile.close()
        # lecture fichier -> modele
        data = {}
        with open(nom_fichier, newline='') as csvfile:
            reader = csv.DictReader(csvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
            for row in reader:
                data[row[clef_champ]] = row
        csvfile.close()
        if reader.fieldnames != champs:
            raise (Exception('ERREUR : les champs du fichier csv ' + nom_fichier + ' ' + ','.join(reader.fieldnames)
                             + ' ne correspondent pas au schema ' + ','.join(champs)))
        else:
            # ajout si besoin d'une entree au modele
            if clef_valeur not in data:
                row = {}
                for champ in champs:
                    row[champ] = None
                row[clef_champ] = clef_valeur
                data[clef_valeur] = row
            # action lecture ou ecriture
            if action == 'r':
                return data[clef_valeur][champ_in]
            elif action == 'rstr':
                return str(data[clef_valeur][champ_in])
            elif action == 'w':
                # maj donnee dans modele
                data[clef_valeur][champ_in] = valeur_in
                # ecriture modele -> fichier
                with open(nom_fichier, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=champs, dialect='excel-tab', quoting=csv.QUOTE_NONE)
                    writer.writeheader()
                    for row in data.values():
                        writer.writerow(row)
                csvfile.close()
            else:
                raise (Exception('ERREUR : action csv inconnue : ' + action))


def command_exist(cmd):
    make_process = subprocess.run(["which", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not cmd in make_process.stdout.decode():
        return False
    else:
        return True



###           EXECUTION DU SCRIPT          ###

###  INIT  ###
os.system('clear')
print("\n\n--------------------EXECUTION DU SCRIPT-----------------------")
print("--------------------------------------------------------------\n\n")
NOTE = 5
RETOUR = ""

msg("Plateforme = " + platform)
###  VERIFICATION OS LINUX + VERSION PYTHON ###
if platform != "linux" and platform != "linux2" and platform != "darwin":
    msg("ERREUR : vous devez executer ce script sous Linux !")
    sys.exit(0)
else:
    msg("======================================================")
    msg("Plateforme = " + platform)
    msg("Verification Linux/MacOS OK")
    msg("======================================================")


if MODE == "PROF":
    msg("======================================================")
    msg("EDITOR="+EDITOR)
    msg("VIEWER="+VIEWER)
    # test EDITOR
    if not command_exist(EDITOR):
        msg("ERREUR : la commande "+EDITOR+" ne semble pas exister ! => changer la commande au début du script ou installer l'éditeur")
        sys.exit(0)
    # test VIEWER
    if not command_exist(VIEWER):
        msg("ERREUR : la commande "+VIEWER+" ne semble pas exister ! => changer la commande au début du script ou installer le viewer d'images")
        sys.exit(0)
    msg("======================================================")

version = sys.version_info
if version[0] != 3 or (version[0] == 3 and version[1] < 5):  # minimum 3.5 pour subprocess.run() et glob recursif
    msg("ERREUR : vous devez executer ce script avec Python 3 (3.5 minimum) !")
    sys.exit(0)
else:
    msg("Python version = " + sys.version)
    msg("Verification Python 3.5 minimum OK")

###  VERIFICATION PARAMETRE DU SCRIPT = NOM ARCHIVE  ###
if len(sys.argv) < 2:
    msg("ERREUR : lancez le script avec l'archive en parametre: " + sys.argv[0] + " NUM_ETU1_NUM_ETU2.tgz")
    sys.exit(0)

### IDENTIFICATION DES ETUDIANTS ET NOM D'ARCHIVE - PRISE EN COMPTE QUE L'ARCHIVE PEUT PROVENIR DE TOMUSS ###
FILENAME = sys.argv[1]
msg("FILENAME = " + FILENAME)
msg("===> note initiale = " + str(NOTE))
NUMEROS_ETU = []
NOM_ARCHIVE_ATTENDU = ""

replaceP = {"p": "1", "P": "1"}
FILENAME_P_REPLACED = replace_all(FILENAME, replaceP)
for mot in FILENAME_P_REPLACED.split(".")[0].split("_"):
    if mot.isdigit() and len(mot) == 8:
        NUMEROS_ETU.append(mot)
        if len(NUMEROS_ETU) > 1:
            NOM_ARCHIVE_ATTENDU += "_"
        NOM_ARCHIVE_ATTENDU += mot

if len(NUMEROS_ETU) == 0:
    msg("ERREUR : aucun numero d'etudiant detecte dans: " + FILENAME)
    sys.exit(0)
if not FILENAME_P_REPLACED.split(".")[0].endswith(NOM_ARCHIVE_ATTENDU):
    msg("L'archive  " + FILENAME + "  ne suit pas le format NUM_ETU1_NUM_ETU2_NUM_ETU3.tgz", 0.5)
f = FILENAME
if "#" in f:
    f = f.split("#")[1]
NOM_ARCHIVE = f[f.find(NUMEROS_ETU[0][1:]) - 1] + NUMEROS_ETU[0][1:] + f.split(".")[0].split(NUMEROS_ETU[0][1:])[1]
msg("NOM_ARCHIVE = " + NOM_ARCHIVE)
msg("Numeros des etudiants =", end=' ')
txtNUM_ETU = " , ".join(NUMEROS_ETU)
msg(txtNUM_ETU, end='\n')

###  EXTRACTION DE L'ARCHIVE  ###
msg("===> decompression de l'archive ...")
tar = tarfile.open(FILENAME)
DIR = "aucun_repertoire_principal"
for tarmember in tar:
    if tarmember.isdir() and '/' not in tarmember.name:
        DIR = tarmember.name
if DIR == "aucun_repertoire_principal":
    msg("Aucun dossier a la racine de l'archive", 5)
    if isdir(DIR):
        shutil.rmtree(DIR, ignore_errors=True)
    os.mkdir(DIR)
msg("Repertoire principal = " + DIR)
if DIR != NOM_ARCHIVE:
    msg("Nom de l'archive et du repertoire principal different: "+str(DIR)+"!="+str(NOM_ARCHIVE), 0.25)
if isdir(DIR):
    DIRNEW = DIR+"___"+str(random.randint(1000,9999))
    msg("Le répertoire "+DIR+" existe déjà. Je renomme l'ancien en "+DIRNEW+" pour repartir d'un test propre")
    os.rename(DIR, DIRNEW)
tar.extractall()
tar.close()
msg("===> decompression de l'archive ... done")

###  VERIFICATION DE L'ARBORESCENCE  ###
msg("===> verification de l'arborescence ...")
if not isdir(DIR) or DIR == ".":
    msg("ERREUR : Repertoire principal inexistant")
    sys.exit(0)
os.chdir(os.getcwd() + "/" + DIR)
if not isdir("bin"):
    msg("Dossier bin inexistant", 0.5)
if not isdir("src"):
    msg("Dossier src inexistant", 0.5)
if not isdir("doc"):
    msg("Dossier doc inexistant", 0.5)
if not isdir("data"):
    msg("Dossier data inexistant", 0.5)
msg("===> verification de l'arborescence ... done")
msg("==> note = " + str(NOTE))

### VERIFICATION DES FICHIERS PRESENTS/ABSENTS ###
FICHIERSATTENDUS = {
    # Fichiers attendus
    "Pixel.h": {"nom": "Pixel", "ext": "h", "loc": "src"},
    "Pixel.cpp": {"nom": "Pixel", "ext": "cpp", "loc": "src"},
    "Image.h": {"nom": "Image", "ext": "h", "loc": "src"},
    "Image.cpp": {"nom": "Image", "ext": "cpp", "loc": "src"},
    "ImageViewer.h": {"nom": "ImageViewer", "ext": "h", "loc": "src"},
    "ImageViewer.cpp": {"nom": "ImageViewer", "ext": "cpp", "loc": "src"},
    "mainTest.cpp": {"nom": "mainTest", "ext": "cpp", "loc": "src"},
    "mainExemple.cpp": {"nom": "mainExemple", "ext": "cpp", "loc": "src"},
    "mainAffichage.cpp": {"nom": "mainAffichage", "ext": "cpp", "loc": "src"},
    "doxyfile": {"nom": "doxyfile", "ext": "", "loc": "doc"},
    # Fichiers générés qui peuvent etre presents
    "test": {"nom": "test", "ext": "", "loc": "bin"},
    "exemple": {"nom": "exemple", "ext": "", "loc": "bin"},
    "affichage": {"nom": "affichage", "ext": "", "loc": "bin"},
    "image1.ppm": {"nom": "image1", "ext": "ppm", "loc": "data"},
    "image2.ppm": {"nom": "image2", "ext": "ppm", "loc": "data"},
    "Makefile": {"nom": "Makefile", "ext": "", "loc": "build"},
    # Fichiers qui peuvent etre presents en cas de reexecution du script sans suppression de l'archive decompressee
    "testRegression": {"nom": "testRegression", "ext": "", "loc": "bin"},
    "mainTestRegression.cpp": {"nom": "mainTestRegression", "ext": "cpp", "loc": "src"},
    "ImageRegression.h": {"nom": "ImageRegression", "ext": "h", "loc": "src"}
}
FICHIERSPRESENTS = listfiles(".")
doclatex = False
for f in FICHIERSPRESENTS:
    if "/html" in f["ch"]:
        continue
    if "/latex" in f["ch"]:
        doclatex = True
        continue
    if "dll" in f["ext"].lower() or "mingw" in f["f"].lower():
        continue
    if "sdl" in f["f"].lower():
        continue
    if f["ext"] in ["cbp", "layout"]:
        continue
    if f["ext"] in ["o", "depend", "d"]:
        continue
    if f["nc"] in ["documentation.h"]:
        continue
    if f["ext"] in ["ttf", "woff", "wav", "mp3"]:
        continue
    if f["ext"] in ["supp"]:
        continue
    if f["nom"].lower() == "makefile":
        continue
    if f["nom"] == "CMakeLists":
        continue
    if f["nom"].lower() == "readme":
        continue
    if f["nc"] in FICHIERSATTENDUS:
        continue
    if "dia" == f["ext"] or "xmi" == f["ext"] or (
                ("png" == f["ext"].lower() or "jpg" == f["ext"].lower()) and "diagramme" in f["nom"].lower()):
        if not "doc" in f["ch"]:
            msg("Le diagramme des classes " + f["nc"] + " doit etre dans le dossier doc/", 0.1)
        continue
    msg("Le fichier/dossier " + f["nc"] + " ne doit pas etre la", 0.1)
if doclatex:
    msg("La documentation n'est pas demandee en latex", 0.1)
msg("===> verification des fichiers presents... done")
msg("==> note = " + str(NOTE))

###  VERIFICATION MAKEFILE-CMAKE ###
msg("===> verification Makefile-CMake ...")
MAKEFILE = "Makefile"
CMAKEFILE = "CMakeLists.txt"
if not isfile(MAKEFILE):
    MAKEFILE = "makefile"
    if not isfile(MAKEFILE):
        MAKEFILE = "???"
if not isfile(CMAKEFILE):
    CMAKEFILE = "???"
if MAKEFILE == "???" and CMAKEFILE == "???":
    msg("Makefile et CMakeLists introuvables", 2)
msg("Makefile = " + MAKEFILE)
msg("CMake = " + CMAKEFILE)
if MAKEFILE != "???" and CMAKEFILE != "???":
    msg("Vous devez choisir entre makefile à la racine et cmake")
    sys.exit(0)
msg("==> note = " + str(NOTE))
msg("===> verification Makefile-CMake ... done")

### GENERATION DU MAKEFILE AVEC CMAKE ###
if CMAKEFILE != "???":
    if not isdir("build"):
        msg("Dossier build inexistant", 0.5)
        make_process = subprocess.run(['mkdir', 'build'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir('build')
    make_process = subprocess.run(['cmake', '..'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    msg("stdout:")
    msg(make_process.stdout.decode("utf-8", "ignore"))
    msg("stderr:")
    msg(make_process.stderr.decode("utf-8", "ignore"))
    if not isfile("Makefile"):
        msg("Erreur dans la génération du makefile")
        sys.exit(0)
    os.chdir('..')

###  CLEAN  ###
if isfile(MAKEFILE):
    msg("===> make clean ...")
    file_makefile = open(MAKEFILE, 'r')
    texte = file_makefile.read()
    if texte.find("clean:") == -1 and texte.find("clean :") == -1:
        msg("Makefile ne contient pas la cible clean", 0.25)
        file_makefile.close()
    else:
        file_makefile.close()
        make_process = subprocess.run(['make', 'clean'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg("stdout:")
        msg(make_process.stdout.decode("utf-8", "ignore"))
        msg("stderr:")
        msg(make_process.stderr.decode("utf-8", "ignore"))

    if isfile("bin/exemple") or isfile("./exemple"):
        msg("make clean ne supprime pas l'executable exemple", 0.1)
    if isfile("bin/test") or isfile("./test"):
        msg("make clean ne supprime pas l'executable test", 0.1)
    if isfile("bin/affichage") or isfile("./affichage"):
        msg("make clean ne supprime pas l'executable affichage", 0.1)

    if len(glob.glob("**/*.o", recursive=True)) != 0:
        msg("make clean ne supprime pas les fichiers objets", 0.5)
        msg("Fichiers objets non supprimes:", end=' ')
        txt_fich_nonsup = " , ".join(glob.glob("**/*.o", recursive=True))
        msg(txt_fich_nonsup)

    for f in glob.glob("**/*.o", recursive=True):
        os.remove(f)
    for f in glob.glob('./exemple') + glob.glob('bin/exemple') + glob.glob('./test') + glob.glob('bin/test') + glob.glob('./affichage') + glob.glob('bin/affichage'):
        os.remove(f)

    msg("===> make clean  ... done")
    msg("==> note = " + str(NOTE))

###  COMPILATION  ###
msg("===> make ...")

if not isfile(MAKEFILE) and isfile(CMAKEFILE):
    os.chdir('build')

make_process = subprocess.run(['make'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

warning = str(make_process.stderr).count("warning:")
msg("stdout:")
msg(make_process.stdout.decode("utf-8", "ignore"))
msg("stderr:")
msg(make_process.stderr.decode("utf-8", "ignore"))
if warning > 0:
    msg("Il y a " + str(warning) + " warnings a la compilation", min(warning * 0.1, 0.5))
else:
    msg("Pas de warning a la compilation")

error = str(make_process.stderr).count("error:")
if error > 0:
    msg("Il y a " + str(error) + " erreurs a la compilation!", 1)
else:
    msg("Pas d'erreur a la compilation")

if (CMAKEFILE != "???"):
    os.chdir('..')

if isfile(MAKEFILE) and len(glob.glob("**/*.o", recursive=True)) != 6:
    msg("Attention : mauvais nombre de fichiers objets")
if isfile(MAKEFILE) and len(glob.glob("obj/*.o")) != len(glob.glob("**/*.o", recursive=True)):
    msg("Fichiers objets dans le mauvais repertoire", 0.5)

if isfile(MAKEFILE) and isfile("src/Pixel.h") and isfile("src/Pixel.cpp") and isfile("src/Image.h") and isfile("src/Image.cpp") and isfile("src/ImageViewer.h") and isfile("src/ImageViewer.cpp") and isfile("src/mainAffichage.cpp"):
    makedepok = True
    filedates = {'obj/mainAffichage.o': 0, 'obj/Pixel.o': 0, 'obj/Image.o': 0, 'obj/ImageViewer.o': 0, 'bin/affichage': 0}
    is_filedates_ok(filedates, {})
    makedepok = is_dep_ok('src/mainAffichage.cpp', filedates,{'obj/mainAffichage.o': True, 'obj/Pixel.o': False, 'obj/Image.o': False, 'obj/ImageViewer.o': False, 'bin/affichage': True}) and makedepok
    makedepok = is_dep_ok('src/Image.cpp', filedates, {'obj/mainAffichage.o': False, 'obj/Pixel.o': False, 'obj/Image.o': True, 'obj/ImageViewer.o': False, 'bin/affichage': True}) and makedepok
    makedepok = is_dep_ok('src/ImageViewer.cpp',filedates,{'obj/mainAffichage.o':False,'obj/Pixel.o':False,'obj/Image.o':False,'obj/ImageViewer.o':True,'bin/affichage':True}) and makedepok
    makedepok = is_dep_ok('src/Image.h', filedates, {'obj/mainAffichage.o': True, 'obj/Pixel.o': False, 'obj/Image.o': True, 'obj/ImageViewer.o': True, 'bin/affichage': True}) and makedepok
    makedepok = is_dep_ok('src/ImageViewer.h', filedates, {'obj/mainAffichage.o': True, 'obj/Pixel.o': False, 'obj/Image.o': False, 'obj/ImageViewer.o': True, 'bin/affichage': True}) and makedepok
    makedepok = is_dep_ok('src/Pixel.cpp', filedates, {'obj/mainAffichage.o': False, 'obj/Pixel.o': True, 'obj/Image.o': False, 'obj/ImageViewer.o': False, 'bin/affichage': True}) and makedepok
    makedepok = (is_dep_ok('src/Pixel.h', filedates, {'obj/mainAffichage.o': True, 'obj/Pixel.o': True, 'obj/Image.o': True, 'obj/ImageViewer.o': True, 'bin/affichage': True}) or
                 is_dep_ok('src/Pixel.h', filedates, {'obj/mainAffichage.o': False, 'obj/Pixel.o': True, 'obj/Image.o': True, 'obj/ImageViewer.o': True, 'bin/affichage': True})) and makedepok
    makedepok = is_dep_ok('aucun_fichier', filedates, {'obj/mainAffichage.o': False, 'obj/Pixel.o': False, 'obj/Image.o': False, 'obj/ImageViewer.o': False, 'bin/affichage': False}) and makedepok
    if not makedepok:
        msg('Les dependances ne sont pas correctement prises en compte dans le Makefile', 0.25)

msg("==> note = " + str(NOTE))
msg("===> make ... done")

###  EXECUTION EXE  ###
## EXEMPLE ##
msg("===> bin/exemple ...")

if not isfile("bin/exemple"):
    msg("make ne genere pas bin/exemple", 0.5)
if isfile("data/image1.ppm"):
    msg("image1.ppm existe, suppression")
    os.remove("data/image1.ppm")
if isfile("data/image2.ppm"):
    msg("image2.ppm existe, suppression")
    os.remove("data/image2.ppm")

if isfile("bin/exemple"):
    make_process = subprocess.run(['bin/exemple'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    msg("stdout:")
    msg(make_process.stdout.decode("utf-8", "ignore"))
    msg("stderr:")
    msg(make_process.stderr.decode("utf-8", "ignore"))

if not isfile("data/image1.ppm"):
    msg("image1.ppm non generee (ou pas dans data)", 0.5)
else:
    if MODE == "PROF":
        if isfile("../image1.ppm"):
            im_file_etu = open("data/image1.ppm", 'r')
            image_etu = im_file_etu.read()
            im_file_prof = open("../image1.ppm", 'r')
            image_prof = im_file_prof.read()
            if image_etu != image_prof:
                msg("image1.ppm erronee", 0.25)
            else:
                msg("image1.ppm OK")
            im_file_prof.close()
            im_file_etu.close()
        else:
            msg("ERREUR PROF : vous devez placer le fichier image1.ppm fourni dans le repertoire du script")
            sys.exit(0)

if not isfile("data/image2.ppm"):
    msg("image2.ppm non generee (ou pas dans data)", 0.5)
else:
    if MODE == "PROF":
        if isfile("../image2.ppm"):
            im_file_etu = open("data/image2.ppm", 'r')
            image_etu = im_file_etu.read()
            im_file_prof = open("../image2.ppm", 'r')
            image_prof = im_file_prof.read()
            if image_etu != image_prof:
                msg("image2.ppm erronee", 0.25)
            else:
                msg("image2.ppm OK")
            im_file_prof.close()
            im_file_etu.close()
        else:
            msg("ERREUR PROF : vous devez placer le fichier image2.ppm fourni dans le repertoire du script")
            sys.exit(0)

msg("===> bin/exemple ... done")
msg("==> note = " + str(NOTE))

## test ##
msg("===> bin/test ...")
if not isfile("bin/test"):
    msg("make ne genere pas bin/test", 0.5)
else:
    make_process = subprocess.run(['bin/test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    msg("stdout:")
    msg(make_process.stdout.decode("utf-8", "ignore"))
    msg("stderr:")
    msg(make_process.stderr.decode("utf-8", "ignore"))
    if make_process.stderr.decode("utf-8", "ignore").find("Assertion") != -1:
        msg("Arret de bin/test non prevu : echec d'une assertion", 0.25)

if MODE == "PROF":
    if isfile("../mainTestRegression.cpp"):
        msg("Test de regression ...")
        replace_in_file('src/Image.h', 'src/ImageRegression.h', 'private', 'public')
        subprocess.run(['cp', '../mainTestRegression.cpp', 'src/mainTestRegression.cpp'])
        subprocess.run(
            ['g++', '-ggdb', '-std=c++11', '-c', 'src/mainTestRegression.cpp', '-o', 'obj/mainTestRegression.o'])
        subprocess.run(['g++', '-ggdb', '-std=c++11', '-c', 'src/Image.cpp', '-o', 'obj/Image.o'])
        subprocess.run(
            ['g++', '-ggdb', '-std=c++11', '-o', 'bin/testRegression', 'obj/mainTestRegression.o', 'obj/Image.o', 'obj/Pixel.o'])
        if not isfile("bin/testRegression"):
            msg("Le test de regression prof ne peut pas compiler (voir ci-dessus les erreurs de compilation)", 0.5)
        else:
            make_process = subprocess.run(['bin/testRegression'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            msg("stdout:")
            msg(make_process.stdout.decode("utf-8", "ignore"))
            msg("stderr:")
            msg(make_process.stderr.decode("utf-8", "ignore"))
            errors = make_process.stdout.decode("utf-8", "ignore")
            nb_errors = errors.count("ERREUR")
            if nb_errors > 0:
                msg("Il y a " + str(nb_errors) + " erreurs dans les tests de regression prof", min(nb_errors * 0.1, 0.5))
            msg("Test de regression ... done")
    else:
        msg("ERREUR PROF : vous devez placer le fichier mainTestRegression.cpp fourni dans le repertoire du script")
        sys.exit(0)

msg("===> bin/test ... done")
msg("==> note = " + str(NOTE))

msg("===> valgrind sur bin/test ...")
if not isfile("bin/test"):
    msg("executable bin/test absent, test valgrind sur bin/test impossible", 1.5)
else:
    make_process = subprocess.run(['valgrind', '--tool=memcheck', '--leak-check=summary', 'bin/test'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    msg("stdout:")
    msg(make_process.stdout.decode("utf-8", "ignore"))
    msg("stderr:")
    msg(make_process.stderr.decode("utf-8", "ignore"))
    str_stderr = make_process.stderr.decode("utf-8", "ignore")
    istart = int(str_stderr.find("definitely lost: "))
    iend = int(str_stderr.find("bytes", istart))
    nb_bytes_lost = 0
    if istart == -1 and iend == -1:
        if str_stderr.find("All heap blocks were freed") == -1:
            msg("Fuite memoire", 0.5)
    else:
        nb_bytes_lost = int(str_stderr[istart + 17:iend].replace(',', ''))
    msg("Nombre de bytes perdus : " + str(nb_bytes_lost))
    if nb_bytes_lost > 0:
        msg("Il y a " + str(nb_bytes_lost) + " octets perdus", min(nb_bytes_lost * 0.01, 0.5))
    else:
        msg("Aucune fuite memoire")

    nb_invalid_write = str_stderr.count("Invalid write")
    nb_invalid_read = str_stderr.count("Invalid read")
    msg("Nombre d'acces invalides : " + str(nb_invalid_write + nb_invalid_read))
    if nb_invalid_write > 0:
        msg("Il y a " + str(nb_invalid_write) + " acces invalides en ecriture a la memoire",
            min(nb_invalid_write * 0.1, 0.5))
    if nb_invalid_read > 0:
        msg("Il y a " + str(nb_invalid_read) + " acces invalides en lecture a la memoire",
            min(nb_invalid_read * 0.1, 0.5))

msg("===> valgrind sur bin/test ... done")
msg("==> note = " + str(NOTE))

## affichage ##
msg("===> bin/affichage ...")
if not isfile("bin/affichage"):
    msg("make ne genere pas bin/affichage", 0.75)
else:
    if MODE == "PROF":
        make_process = subprocess.run(['bin/affichage'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg("stdout:")
        msg(make_process.stdout.decode("utf-8", "ignore"))
        msg("stderr:")
        msg(make_process.stderr.decode("utf-8", "ignore"))
        utilisateur_evalue('affichage image ok', 'bin/affichage non fonctionnel ou incomplet', 0.5, 'ech3')
        # echelle d'appreciations ech3: n (non/insuffisant), m (moyen), o (oui/bien)
        utilisateur_evalue('zoom/dezoom ok', 'zoom/dezoom non fonctionnel ou incomplet', 0.25, 'ech3')

msg("===> bin/affichage ... done")
msg("==> note = " + str(NOTE))

###  README  ###
msg("===> readme ...")
readmes = ["readme.txt", "Readme.txt", "README.txt", "readme.md", "Readme.md", "README.md"]
readme = filein(readmes)
if readme != "":
    longueur = filesize(readme)
    msg("longueur du fichier " + readme + " : " + str(longueur) + " caracteres")
    if MODE == "PROF":
        make_process = subprocess.run([EDITOR, readme], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        utilisateur_evalue('readme ok', 'readme pas assez detaille', 0.5, 'ech7')
        # echelle d'appreciations ech7: n (non/insuffisant), n+, m-, m (moyen), m+, o-, o (oui/bien)
    elif longueur < 500:
        msg(readme + " pas assez detaille", 0.5)
else:
    msg("readme introuvable", 0.5)

msg("===> readme ... done")
msg("==> note = " + str(NOTE))

###  DOCUMENTATION  ###
msg("===> documentation ...")
doxys = ["doc/image.doxy", "doc/doxyfile"]
doxy = filein(doxys)
if doxy != "":
    rmfiles("doc/html")
    rmfiles("doc/latex")
    make_process = subprocess.run(['doxygen', doxy], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not isfile("doc/html/index.html"):
        msg("Doxygen n'a pas genere doc/html/index.html, mauvais chemin dans OUTPUT_DIRECTORY et/ou INPUT?", 0.5)
    v1 = isfile("doc/html/class_image.html")
    v2 = isfile("doc/html/classImage.html")
    if not v1 and not v2:
        msg("Doxygen n'a pas genere de doc pour la classe Image", 0.25)
    v1 = isfile("doc/html/class_image_viewer.html")
    v2 = isfile("doc/html/classImageViewer.html")
    if not v1 and not v2:
        msg("Doxygen n'a pas genere de doc pour la classe ImageViewer", 0.25)
    v1 = isfile("doc/html/struct_pixel.html")
    v2 = isfile("doc/html/structPixel.html")
    if not v1 and not v2:
        msg("Doxygen n'a pas genere de doc pour la structure Pixel", 0.25)
else:
    msg("Fichier de configuration doxygen (doc/doxyfile) introuvable", 1)

files_h = ["src/image.h", "src/Image.h", "src/pixel.h", "src/Pixel.h", "src/imageviewer.h", "src/ImageViewer.h",]
n_brief = 0
n_param = 0
for f in files_h:
    n_brief += count_in_file(f, "brief")
    n_param += count_in_file(f, "param")
msg("Nombre de fonctions commentees : " + str(n_brief))
msg("Nombre de parametres commentes : " + str(n_param))
if n_brief < 20:
    msg("Pas assez de fonctions commentees", 0.25)
if n_param < 20:
    msg("Pas assez de parametres commentees", 0.25)

msg("===> documentation ... done")
msg("==> note = " + str(NOTE))

###  ASSERTIONS  ###
msg("===> assert ...")
search = ["assert(", "assert (", "throw"]
files = ["src/image.h", "src/Image.h", "src/pixel.h", "src/Pixel.h", "src/image.cpp", "src/Image.cpp", "src/imageviewer.cpp", "src/ImageViewer.cpp", "src/pixel.cpp",
         "src/Pixel.cpp"]
n = 0
for f in files:
    for s in search:
        n += count_in_file(f, s)
msg("Nombre d'assertions : " + str(n))
if n < 8:
    msg("Pas assez d'assertions", 0.5)
msg("===> assert ... done")
msg("==> note = " + str(NOTE))

###  CODE  ###
msg("===> code ...")
## Pixel.h ##
if not (isfile("src/Pixel.h") or isfile("src/pixel.h")):
    msg("src/Pixel.h absent, test code Pixel.h impossible", 2)
files = ["src/Pixel.h", "src/pixel.h"]
for f in files:
    if isfile(f):
        fi = open(f, 'r', encoding="latin-1")
        texte = fi.read()
        texte = re.sub("(?<=\/\*)(.*?)(?=\*\/)", "", texte, 0, re.DOTALL)
        texte = re.sub("//.*", "", texte)
        if texte.count("ifndef") == 0:
            msg("Oubli de la directive ifndef dans Pixel", 0.25)
        if texte.count("struct Pixel") == 0 and texte.count("class Pixel") == 1:
            msg("Mauvais type pour Pixel", 0.25)
        if texte.count("unsigned char") == 0:
            msg("Mauvais type des donnees membres de Pixel", 0.25)
        istart = texte.find("afficherPixel")
        if istart == -1:
            msg("Fonction afficherPixel introuvable", 0.25)
        else:
            iend = texte[istart:].find(";") + istart
            if texte[istart:iend].find("const") == -1:
                msg("Erreur entete afficherPixel", 0.25)
        fi.close()
## Image.h ##
if not (isfile("src/Image.h") or isfile("src/image.h")):
    msg("src/Image.h absent, test code Image.h impossible", 2)
files = ["src/Image.h", "src/image.h"]
for f in files:
    if isfile(f):
        fi = open(f, 'r', encoding="latin-1")
        texte = fi.read()
        texte = re.sub("(?<=\/\*)(.*?)(?=\*\/)", "", texte, 0, re.DOTALL)
        texte = re.sub("//.*", "", texte)
        if texte.count("#include") > 2:
            msg("Des include inutiles dans Image.h", 0.25)
        if texte.count("ifndef") == 0:
            msg("Oubli de la directive ifndef dans Pixel", 0.25)
        if texte.count("struct Image") == 1 and texte.count("class Image") == 0:
            msg("Mauvais type pour Image", 0.5)
        istart = texte.find("private")
        iend = texte[istart:].find("public") + istart
        if iend == -1:
            iend = texte[istart:].find("}") + istart
        if texte[istart:iend].find("int") == -1:
            msg("Erreur de type de données membres de Image",0.25)
        if texte[istart:iend].find("dimx") == -1 or texte[istart:iend].find("dimy") == -1:
            msg("Erreur de nom de données membres de Image",0.25)
        if texte[istart:iend].find("Pixel") == -1 or texte[istart:iend].find("*") == -1 or texte[istart:iend].find("tab") == -1:
            msg("Erreur dans donnée membre tab de Image",0.25)
        iend = texte.find("getPix")
        if iend == -1:
            msg("Erreur première fonction getPix introuvable",0.25)
        istart = texte[:iend].rfind("Pixel")
        if texte[istart:iend].find("*") != -1 or texte[istart:iend].find("&") == -1:
            msg("Mauvais type de retour de la premiere version de getPix", 0.5)
        iend = texte[iend:].find("getPix")
        if iend == -1:
            msg("Erreur deuxième fonction getPix introuvable",0.25)
        istart = texte[:iend].rfind("Pixel")
        if texte[istart:iend].find("*") != -1 or texte[istart:iend].find("&") != -1:
            msg("Mauvais type de retour de la deuxieme version de getPix", 0.5)
        istart = texte.find("static")
        if istart == -1:
            msg("La fonction de test de regression doit etre static", 0.25)
        else:
            iend = texte[istart:].find(";") + istart
            if texte[istart:iend].find("testRegression") == -1:
                msg("La fonction de test de regression doit etre static", 0.25)
        if texte.count("const") < 8:
            msg("Manque des const", 0.25)
        if texte.find("Image") == -1 or texte.find("getPix") == -1 or texte.find("setPix") == -1 or texte.find("dessinerRectangle") == -1 or texte.find("effacer") == -1 or texte.find("testRegression") == -1:
            msg("Manque des fonctions ou mauvais noms dans Image", 0.5)
        if texte.find("sauver") == -1 or texte.find("ouvrir") == -1 or texte.find("afficherConsole") == -1:
            msg("Manque les fonctions I/O", 0.5)
        fi.close()

## Image.cpp ##
if not (isfile("src/Image.cpp") or isfile("src/image.cpp")):
    msg("src/Image.cpp absent, test code Image.cpp impossible", 3)
files = ["src/Image.cpp", "src/image.cpp"]
for f in files:
    if isfile(f):
        fi = open(f, 'r', encoding="latin-1")
        texte = fi.read()
        texte = re.sub("(?<=\/\*)(.*?)(?=\*\/)", "", texte, 0, re.DOTALL)
        texte = re.sub("//.*", "", texte)
        istart = texte.find("::Image")
        if istart == -1:
            istart = texte.find(":: Image")
        if istart == -1:
            msg('Constructeur Image impossible a trouver', 0.25)
        iend = texte[istart + 2:].find("::") + istart + 2
        imid = texte[istart:iend].find("NULL")
        if imid == -1:
            imid = texte[istart:iend].find("nullptr")
        imid2 = texte[istart:iend].find("tab")
        if imid == -1 or imid2 == -1 or imid < imid2:
            msg("Erreur initialisation tab", 0.25)
        istart = texte.find("~Image")
        if istart == -1:
            istart = texte.find("~ Image")
        if istart == -1:
            msg('Destructeur Image impossible a trouver', 0.25)
        iend = texte[istart:].find("::") + istart
        imid1 = texte[istart:iend].find("if")
        imid2 = texte[istart:iend].find("tab")
        imid3 = texte[istart:iend].find("NULL")
        if imid3 == -1:
            imid3 = texte[istart:iend].find("nullptr")
        imid4 = texte[istart:iend].find("delete")
        if imid1 == -1 or imid2 == -1 or imid3 == -1 or imid4 == -1:
            msg("Erreur destruction tab", 0.25)
        istart = texte.find("::testRegression")
        if istart == -1:
            istart = texte.find(":: testRegression")
        if istart == -1:
            msg('Fonction de test impossible a trouver', 0.5)
        iend = texte[istart + 2:].find("::")
        if iend == -1:
            iend = len(texte) - 1
        else:
            iend += istart + 2
        nba = texte[istart:iend].count('assert')
        if nba < 6:
            msg('Principe de test regression pas compris', 0.5)
        istart = texte.find("dessinerRectangle")
        iend = texte[istart:].find("::") + istart
        if texte[istart:iend].find("setPix") == -1:
            msg("dessinerRectangle doit appeller getPix itérativement",0.25)
        istart = texte.find("effacer")
        iend = texte[istart:].find("::") + istart
        if texte[istart:iend].find("dessinerRectangle") == -1:
            msg("effacer doit appeller dessinerRectangle",0.25)
        fi.close()

## ImageViewer.h ##
if not (isfile("src/ImageViewer.h") or isfile("src/imageviewer.h")):
    msg("src/ImageViewer.h absent, test code ImageViewer.h impossible", 0.5)
files = ["src/ImageViewer.h", "src/imageviewer.h"]
for f in files:
    if isfile(f):
        fi = open(f, 'r', encoding="latin-1")
        texte = fi.read()
        texte = re.sub("(?<=\/\*)(.*?)(?=\*\/)", "", texte, 0, re.DOTALL)
        texte = re.sub("//.*", "", texte)
        if texte.count("#include") > 3:
            msg("Des include inutiles dans ImageViewer.h", 0.25)
        if texte.count("ifndef") == 0:
            msg("Oubli de la directive ifndef dans ImageViewer", 0.25)
        if texte.count("struct ImageViewer") == 1 and texte.count("class ImageViewer") == 0:
            msg("Mauvais type pour ImageViewer", 0.5)
        istart = texte.find("private")
        iend = texte[istart:].find("public") + istart
        if iend == -1:
            iend = texte[istart:].find("}") + istart
        if texte[istart:iend].find("SDL_Window") == -1 or texte[istart:iend].find("SDL_Renderer") == -1:
            msg("Erreur données membres de ImageViewer ou specificateur d'acces",0.25)
        istart = texte.find("afficher")
        iend = texte[istart:].find(";") + istart
        if texte[istart:iend].find("const") == -1 or texte[istart:iend].find("Image") == -1 or texte[istart:iend].find("&") == -1:
            msg("Erreur parametre afficher de ImageViewer",0.25)
        fi.close()

## mainTest.cpp ##
if not (isfile("src/mainTest.cpp") or isfile("src/maintest.cpp")):
    msg("src/mainTest.cpp absent, test code mainTest.cpp impossible", 0.5)
files = ["src/mainTest.cpp", "src/maintest.cpp"]
for f in files:
    if isfile(f):
        fi = open(f, 'r', encoding="latin-1")
        texte = fi.read()
        texte = re.sub("(?<=\/\*)(.*?)(?=\*\/)", "", texte, 0, re.DOTALL)
        texte = re.sub("//.*", "", texte)
        istart = texte.find("Image::testRegression();")
        if istart == -1:
            msg("Fichier mainTest modifie", 0.25)
        fi.close()

if MODE == "PROF":
    command = [EDITOR]
    command.extend(glob.glob("src/*.*"))
    make_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    reponse = utilisateur_demande('Problemes dans le code, nombre de points a deduire (limite a trois points) ', 'erreurs code penalite')
    points = min(float(reponse), 3)
    if points > 0:
        reponse = utilisateur_demande('Problemes dans le code, commentaires', 'erreurs code detail')
        msg('' + reponse + '\n' + 'Problemes dans le code', points)

msg("===> code ... done")
msg("==> note = " + str(NOTE))

###  RESUME  ###
msg("\nLes etudiants ayant comme numeros : ", end='')
txt_numetu = " , ".join(NUMEROS_ETU)
msg(txt_numetu, end=' ')
msg("ont la note " + str(NOTE) + "\n")

###  FICHIERS FEEDBACK ET NOTES  ###
if MODE == "PROF":
    for etu in NUMEROS_ETU:
        foutput = open('../' + str(etu) + '#feedback.txt', 'w')
        foutput.write(NOM_ARCHIVE + " : " + str(NOTE) + "\n" + RETOUR)
        foutput.close()

    foutput = None
    if isfile("../notesEtudiants.txt"):
        foutput = open('../notesEtudiants.txt', 'r')
        if foutput.read().find(str(NUMEROS_ETU[0])) == -1:
            foutput.close()
            foutput = open('../notesEtudiants.txt', 'a')
            for etu in NUMEROS_ETU:
                foutput.write(str(etu) + " " + str(NOTE) + "\n")
            foutput.close()
        else:
            foutput.close()
    else:
        foutput = open('../notesEtudiants.txt', 'w')
        for etu in NUMEROS_ETU:
            foutput.write(str(etu) + " " + str(NOTE) + "\n")
        foutput.close()

    persiste_arch_val('nomFichier', 'w', FILENAME)
    persiste_arch_val('numsEtu', 'w', '#'.join(NUMEROS_ETU))
    persiste_arch_val('repPrinc', 'w', DIR)
    persiste_arch_val('note', 'w', NOTE)

    for etu in NUMEROS_ETU:
        persiste_etu_val(etu, 'note', 'w', NOTE)

print("-----------------------FIN DU SCRIPT--------------------------")
if "--noinput" not in sys.argv:
    input('Appuyer sur Entree pour quitter...')

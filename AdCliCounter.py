#!/bin/python
import platform
import argparse
import json
import time
import sys
import os

def anyjoin(inputl,sep=""): # joins anything in the fist list by converting it to str
    sep=str(sep)
    out=""
    for i in inputl:
        if out == "":
            out += str(i)
        else:
            out += sep + str(i)
    return out

def savecounterfile(folder,cname,end,clist): #saves a file to provided location with list to place into file
    recfile = os.path.join(folder,cname + end)
    f = open(recfile, "w")
    f.write(anyjoin(clist))
    f.close()

def osmakeshortcut(folder,cname,script): #makes shortcuts to provided locations
    if platform.system() == "Linux" or platform.system() == "Darwin": #mk desktop file for mac and linux
        print("Making Linux shortcuts")
        #add 1 to conter con #description #'/home/marvin/Documents/Coding/Python/Couter/New Folder/Text File.txt' -a 1 #executexargs
        #con add #diplayname #/home/marvin/Documents/Coding/Python/Couter #counterpath
        desktopfile = """[Desktop Entry]
Comment={}
Exec={}
Name={}
Path={}
StartupNotify=true
Terminal=false
Type=Application"""
        Addf = desktopfile.format("add 1 to " + cname,"python '" + script + "' -t '" + cname + "' -a 1",cname + " add",folder)
        savecounterfile(folder,cname + " add",".desktop",[Addf])
        Setf = desktopfile.format("set " + cname + " to 0","python '" + script + "' -t '" + cname + "' -e 0",cname + " reset",folder)
        savecounterfile(folder,cname + " res",".desktop",[Setf])
        Subf = desktopfile.format("subtract 1 of " + cname,"python '" + script + "' -t '" + cname + "' -a -1",cname + " reset",folder)
        savecounterfile(folder,cname + " sub",".desktop",[Subf])
    elif platform.system() == "Windows": #mk vbs file for windows
        print("Making Windows shortcuts")
        #Dim WShell #Set WShell = CreateObject("WScript.Shell")
        #WShell.Run "path\to\app.exe /argument1 /argument2", 0 #Set WShell = Nothing
        vbsfile = """Dim WShell
Set WShell = CreateObject("WScript.Shell")
WShell.CurrentDirectory = "{}"
WShell.Run "{}"
Set WShell = Nothing"""
        Addf = vbsfile.format(folder,"python '" + script + "' -t '" + cname + "' -a 1")
        savecounterfile(folder,cname + " add",".vbs",[Addf])
        Setf = vbsfile.format(folder,"python '" + script + "' -t '" + cname + "' -e 0")
        savecounterfile(folder,cname + " res",".vbs",[Addf])
        Subf = vbsfile.format(folder,"python '" + script + "' -t '" + cname + "' -a -1")
        savecounterfile(folder,cname + " sub",".vbs",[Addf])

fullscript = os.path.realpath(__file__)
scriptdir = os.path.dirname(fullscript)

parser = argparse.ArgumentParser(
    prog='AdCliCounter.py',
    description='A counter manager',
    epilog='')
parser.add_argument('-j', '--json', help='where is your conter config (default ./counters.json)')
parser.add_argument('-d', '--defaultshortcut', action='count', help='make shortcuts when creating counters, add twice to disable')
parser.add_argument('-f', '--defaultprefix', help='set default prefix for when creating counters')
parser.add_argument('-x', '--defaultsuffix', help='set sufix for for when creating counters')
parser.add_argument('-n', '--nodefcounter', action='count', help='allow the counter with the name "default" to be deleted, add twice to revert (warning counter is used for fallback)')
parser.add_argument('-c', '--create', help='create a new counter with a custom name')
parser.add_argument('-r', '--remove', help='remove a counter with a custom name')
parser.add_argument('-t', '--select', help='select a counter to use')
parser.add_argument('-e', '--set', type=int, help='set the counter to any number')
parser.add_argument('-a', '--add', type=int, help='change the counter by +/-x')
parser.add_argument('-m', '--makeshortcut', action='count', help='make shortcuts for selected counter, add twice to disable')
parser.add_argument('-p', '--prefix', help='set prefix for selected counter')
parser.add_argument('-s', '--suffix', help='set sufix for selected counter')
parser.add_argument('-l', '--list', action='store_true', help='list available counters')

args = parser.parse_args()

if args.json == None:
    savedir = scriptdir
    configfull = os.path.join(savedir,"counters.json")
else:
    configfull = os.path.realpath(args.json)
    savedir = os.path.dirname(configfull)

fjson = {}
if os.path.exists(configfull):
    f = open(configfull)
    fjson = json.loads(f.read())
    f.close()

defaultjs = {
    "application":"AdCliCounter.py",
    "version":0.1,
    "defaultshortcut":False,
    "defaultprefix":"",
    "defaultsuffix":"",
    "nodefcounter":False,
    "selected":"default",
    "counters":{
        "default":["default: ",0,""]
    }
}

#ceckcompabilty
try:
    if fjson != {} and fjson["application"] == defaultjs["application"]:
        try:
            if fjson["version"] > defaultjs["version"]:
                print(" Warning json was made for a newer version")
            elif fjson["version"] < defaultjs["version"]:
                print(" Warning json was made for a older version")
        except:
            print(" Error json has no version entry")
            exit(1)
    elif fjson != {}:
        print(" Error the json was made for a other application")
        exit(1)
except:
    print(" Error the json does not belog to any application")
    exit(1)
#nodefaultcounter
if args.nodefcounter == 1:
    fjson["nodefcounter"] = True
elif args.nodefcounter != None and args.nodefcounter > 1:
    fjson["nodefcounter"] = False

#deletecounternameddefault
try:
    if fjson["nodefcounter"] == True: #if the default counter is not wanted delete it
        defaultjs["counters"].pop("default")
    else: #if its wanted
        try: #and not used yet
            excont = fjson["counters"]["default"]
        except: #add the counter back in
            fjson["counters"]["default"] = defaultjs["counters"]["default"]
except:
    pass

comdict = defaultjs | fjson #merge dicts

#defaultshortcut
if args.defaultshortcut == 1:
    comdict["defaultshortcut"] = True
elif args.defaultshortcut != None and args.defaultshortcut > 1:
    comdict["defaultshortcut"] = False
#defaultprefix
if args.defaultprefix:
    comdict["defaultprefix"] = args.defaultprefix
#defaultsuffix
if args.defaultsuffix:
    comdict["defaultprefix"] = args.defaultprefix

#create
selected = None
if args.create:
    if args.prefix: #prefix
        prefix = args.prefix
    else:
        prefix = comdict["defaultprefix"]
    if args.suffix: #suffix
        suffix = args.suffix
    else:
        suffix = comdict["defaultsuffix"]
    if args.makeshortcut == 1: #makeshortcut
        makeshortcut = True
    elif args.makeshortcut != None and args.makeshortcut > 1:
        makeshortcut = False
    else:
        makeshortcut = comdict["defaultshortcut"]
    try: #check if counter exists
        excont = comdict["counters"][args.create]
    except: #if not create it
        comdict["counters"][args.create] = [suffix,0,prefix]
        savecounterfile(savedir,args.create,".txt",comdict["counters"][args.create]) #savecounterfile
        selected = args.create
        print("Created " + args.create)
        if makeshortcut:
            osmakeshortcut(savedir,args.create,fullscript)
    else:
        print(" Warning, counter " + args.create + " can't be created, it exists allready")

#remove
if args.remove:
    try: #check if counter exists
        excont = comdict["counters"][args.remove]
    except:
        print(" Warning, counter " + args.remove + " can't be removed, it does not exist")
    else: #if it does delete it
        comdict["counters"].pop(args.remove)
        end = ".desktop" # Linux + Mac
        if platform.system() == "Windows": # Windows
            end = ".vbs"
        try:
            os.remove(os.path.join(savedir,args.remove + ".txt"))
            os.remove(os.path.join(savedir,args.remove + " add" + end))
            os.remove(os.path.join(savedir,args.remove + " res" + end))
            os.remove(os.path.join(savedir,args.remove + " sub" + end))
        except:
            pass
        print("Counter " + args.remove + " was removed")

#select
if args.select:
    try: #check if counter exists
        excont = comdict["counters"][args.select]
    except:
        print(" Warning, counter " + args.select + " can't be selected, it does not exist")
    else:
        selected = args.select
        print("Selected " + str(args.select))

#defaultselect
if selected == None: #if nothing is selected select default or last selection
    try: #check if counter exists
        excont = comdict["counters"][comdict["selected"]]
    except:
        try:
            excont = comdict["counters"]["default"]
        except:
            print(" Warning, counter \"default\" and the last selected counter " + comdict["selected"] + " do not exist")
        else:
            selected = "default"
    else:
        selected = comdict["selected"]

#saveselected
if selected != None:
    comdict["selected"] = selected

#set
if args.set and selected != None:
    try:
        comdict["counters"][selected][1] = args.set
        savecounterfile(savedir,selected,".txt",comdict["counters"][selected]) #savecounterfile
        print("Setting " + selected + " to " + str(args.set))
    except:
        print(" Warning, counter " + selected + " has a unexpected json format, the conter entry needs to be [\"prefix\",\"0\",\"suffix\"]")
#add
if args.add and selected != None:
    try:
        excont = comdict["counters"][selected]
        comdict["counters"][selected][1] = excont[1] + args.add
        savecounterfile(savedir,selected,".txt",comdict["counters"][selected]) #savecounterfile
        print("Added " + str(args.add) + " to " + selected + ", now its on " + str(excont[1] + args.add))
    except:
        print(" Warning, counter " + selected + " has a unexpected json format, the conter entry needs to be [\"prefix\",\"0\",\"suffix\"] not \"" + str(comdict["counters"][selected]) + "\"")

#changeprefix
if args.prefix != None and selected != None and args.create != selected:
    try:
        comdict["counters"][selected][0] = args.prefix
    except:
        print(" Warning, change of prefix for counter " + selected + " failed, it has a unexpected json format, the conter entry needs to be [\"prefix\",\"0\",\"suffix\"] not \"" + str(comdict["counters"][selected]) + "\"")
    else:
        savecounterfile(savedir,selected,".txt",comdict["counters"][selected]) #savecounterfile
        print("Prefix of counter " + selected + " was change to " + args.prefix)

#changesuffix
if args.suffix != None and selected != None and args.create != selected:
    try:
        comdict["counters"][selected][2] = args.suffix
    except:
        print(" Warning, change of suffix for counter " + selected + " failed, it has a unexpected json format, the conter entry needs to be [\"prefix\",\"0\",\"suffix\"] not \"" + str(comdict["counters"][selected]) + "\"")
    else:
        savecounterfile(savedir,selected,".txt",comdict["counters"][selected]) #savecounterfile
        print("Suffix of counter " + selected + " was changed to " + args.suffix)

#savejson
savedict = {
    "application":comdict["application"],
    "version":comdict["version"],
    "defaultshortcut":comdict["defaultshortcut"],
    "defaultprefix":comdict["defaultprefix"],
    "defaultsuffix":comdict["defaultsuffix"],
    "nodefcounter":comdict["nodefcounter"],
    "selected":comdict["selected"],
    "counters":comdict["counters"]
}
f = open(configfull, "w")
f.write(json.dumps(savedict, indent=4, separators=(',', ': ')))
f.close()


#list
if args.list:
    print("\tThe counters are")
    for cname in comdict["counters"]:
        print(" N = " + cname + " ; V = " + anyjoin(comdict["counters"][cname],""))

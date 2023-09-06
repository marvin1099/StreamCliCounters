# StreamCliCounters Main
https://codeberg.org/marvin1099/StreamCliCounters  


# StreamCliCounters Backup
https://github.com/marvin1099/StreamCliCounters  


# Description
A rework of one of my very old projects.  
Its a shortuct/comandline controlled counter system.  
You can add as many counters as you like,  
for the most interesting numbers, like kills or deaths.  

# Install
get it here:  
https://codeberg.org/marvin1099/StreamCliCounters/releases  
or here:  
https://github.com/marvin1099/StreamCliCounters/releases  

# Explanation
First get python and the script from above.  
Next you can open a terminal in the script folder and run: 

    AdCliCounter.py -d
    AdCliCounter.py -c MyKills -p "Kills: "  
To make a Kills counter with some shortcuts for adding and subtracting.  
The ***-d*** enables shortcut creation on counter creation.  
Now there is also going to be a ***MyKills.txt*** in The script folder to show in your stream.  
Now just use the shortcuts to add subtract or reset the counter.  
There are some more thinks to to for that ceck out the usage bellow.  
It can also be shown in the script by running:

    AdCliCounter.py -h

# Usage
    usage: AdCliCounter.py [-h] [-j JSON] [-d] [-f DEFAULTPREFIX] [-x DEFAULTSUFFIX] [-n] [-c CREATE]
    [-r REMOVE] [-t SELECT] [-e SET] [-a ADD] [-m] [-p PREFIX] [-s SUFFIX] [-l]

    A counter manager

    options:
    -h, --help            show this help message and exit
    -j JSON, --json JSON  where is your conter config (default ./counters.json)
    -d, --defaultshortcut
    make shortcuts when creating counters, add twice to disable
    -f DEFAULTPREFIX, --defaultprefix DEFAULTPREFIX
    set default prefix for when creating counters
    -x DEFAULTSUFFIX, --defaultsuffix DEFAULTSUFFIX
    set sufix for for when creating counters
    -n, --nodefcounter    allow the counter with the name "default" to be deleted, add twice to revert
    (warning counter is used for fallback)
    -c CREATE, --create CREATE
    create a new counter with a custom name
    -r REMOVE, --remove REMOVE
    remove a counter with a custom name
    -t SELECT, --select SELECT
    select a counter to use
    -e SET, --set SET     set the counter to any number
    -a ADD, --add ADD     change the counter by +/-x
    -m, --makeshortcut    make shortcuts for selected counter, add twice to disable
    -p PREFIX, --prefix PREFIX
    set prefix for selected counter
    -s SUFFIX, --suffix SUFFIX
    set sufix for selected counter
    -l, --list            list available counters

# Exaple
Keep in mind the script allways has to run in the script folder  
as a working directory to generate the files in the script folder.  
Lets make up some senarios.  
You want to count the coins of a game manualy.    
There are coins that give 5 points, give 10 coins and one that takes 3 coins.  
To make a counter for this open a terminal and run:  

    AdCliCounter.py -d -c Coins -p "My Collected Coin Count: "
At this point thanks to the -d shortcuts will be created.
But now we have to modify the shortcuts to do what we want.  
So rightclick the add shorcut (vbs file) and open it in you favorite editor (eg. Notepad).  
Now modify "Exec=" on linux or WShell.Run "" on windows to say 5 not 1.  
Next copy the shorcut (vbs file) and open the copy in you favorite editor.  
Make it say 10 not 5.  
Lastly edit the sub shorcut (vbs file) and open it in you favorite editor.  
Change the -1 to -3.  
Now you are done you can use the Coins.txt in your stream.

# DefaultCounter
Keep in mind the script allways has to run in the script folder  
as a working directory to generate the files in the script folder.  
The default counter is used as a fallback.
You can deleted it, if you realy dont want it,
but its not recomended.
To do that open a terminal and run:

    AdCliCounter.py -n -r default
If you want to use it insted you can set it to 0. 
That can be done by opening a terminal and running:  

    AdCliCounter.py -t default -e 0
That will make your ***default.txt*** appear.  
if you want to generate the shortcuts for default,  
you need to do the following.  
First make shure to backup your default data if you want to keep it.  
Then open a terminal and run: 

    AdCliCounter.py -d -n -r default
    AdCliCounter.py -c default

# ManualEdits
You can manualy edit the counter.json file,  
but be carefull to not mess up the format.  
The json in set up strait forward so it sold be posible to edit by hand.
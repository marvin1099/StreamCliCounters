# StreamCliCounters
Main Repo: https://codeberg.org/marvin1099/StreamCliCounters  
Backup Repo: https://github.com/marvin1099/StreamCliCounters

# Table of contents
- [Description](#Description) 
- [Install](#Install)
- [Explanation](#Explanation)  
- [Usage](#Usage)  
- [Example](#Example)  
- [DefaultCounter](#DefaultCounter) 
- [ManualEdits](#ManualEdits) 

# Description
A rework of one of my very old projects.  
Its a shortuct/comandline controlled counter system.  
You can add as many counters as you like,  
for the most interesting numbers, like kills or deaths.  
Keep in mind, to make this as good as can be,  
i took inspiration from an AI suggestion.  

# Install
get it on one of these:  
[Codeberg Releases](https://codeberg.org/marvin1099/StreamCliCounters/releases)   
[Github Releases](https://github.com/marvin1099/StreamCliCounters/releases)   

# Explanation
First get python and the script from above.  
Next you can open a terminal in the script folder and run: 

    AdCliCounter.py -d
    AdCliCounter.py -c MyKills -p "Kills: "  
To make a Kills counter with some shortcuts for adding and subtracting.  
The ***-d*** will create a shortcut for the selected counter.  
Now there is also going to be a ***MyKills.txt*** in The script folder to show in your stream.  
Now just use the shortcuts to add subtract or reset the counter.  
There are some more things to to for that ceck out the usage bellow.  
It can also be shown in the script by running:

    AdCliCounter.py -h

# Usage
    usage: AdCliCounter.py [-h] [-j JSON] [-o] [-c CREATE] [-t SELECT] [-i] [-r] [-n RENAME] [-x DEFAULTPREFIX]
    [-p PREFIX] [-y DEFAULTSUFFIX] [-s SUFFIX] [-u DEFAULTVALUE] [-v VALUE] [-e SET]
    [-a ADD] [-w] [-d] [-l]

    A counter manager

    options:
    -h, --help            show this help message and exit
    -j JSON, --json JSON  where is your conter config (default 'counters.json')
    -o, --selectcreation  auto select counter on creation, add twice to disable
    -c CREATE, --create CREATE
    create a new counter with a custom name
    -t SELECT, --select SELECT
    select a counter to use
    -i, --pointer         print the selected counter
    -r, --remove          remove the selected counter
    -n RENAME, --rename RENAME
    rename the selected counter
    -x DEFAULTPREFIX, --defaultprefix DEFAULTPREFIX
    set default prefix for when creating counters
    -p PREFIX, --prefix PREFIX
    set prefix for created or selected counter
    -y DEFAULTSUFFIX, --defaultsuffix DEFAULTSUFFIX
    set sufix for for when creating counters
    -s SUFFIX, --suffix SUFFIX
    set sufix for created or selected counter
    -u DEFAULTVALUE, --defaultvalue DEFAULTVALUE
    set default value for when creating counters
    -v VALUE, --value VALUE
    set value for when creating counters
    -e SET, --set SET     set the selected counter to any number
    -a ADD, --add ADD     change the counter by +/-x
    -w, --defaultshortcut
    create shortcuts on counter creation, add twice to disable
    -d, --createshortcut  make shortcuts for selected counter, add twice to delete shortcuts
    -l, --list            list available counters

# Example
Keep in mind the script should be run in the desired counter folder  
as a working directory to generate the files in the desired folder. 
Lets make up a senario.  
You want to count the coins of a game manualy.    
There are coins that give 5 points, give 10 points and one that takes 3 points.  
To make a counter for this open a terminal and run:  

    AdCliCounter.py -d -c Coins -p "My Collected Coin Points: "
If you want to always enable shortcuts use "-w".
But now we have to modify the shortcuts to do what we want.  
So rightclick the add shorcut (vbs file) and open it in you favorite editor (eg. Notepad).  
Now modify "Exec=" on linux or WShell.Run "" on windows to say 5 not 1.  
Next copy the shorcut (vbs file) and open the copy in you favorite editor.  
Make it say 10 not 5.  
Lastly edit the sub shorcut (vbs file) and open it in you favorite editor.  
Change the -1 to -3.  
Now you are done you can use the Coins.txt in your stream.

# DefaultCounter
The default counter was removed i version 0.2.
It wasn't that usefull and can be recreated by running:

    AdCliCounter.py -c default -p "Default: "

# ManualEdits
You can manualy edit the counter.json file,  
but be carefull to not mess up the format.  
The json in set up straight forward so it sold be posible to edit by hand.
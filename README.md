# StreamCliCounters
A rework of one of my older projects.  
It's a shortcut/command-line controlled counter system.  
You can add as many counters as you like,  
for the most interesting numbers, like kills or deaths.  
Keep in mind, to make this as good as can be,  
I took inspiration from an AI suggestion.

Main Repo: https://codeberg.org/marvin1099/StreamCliCounters  
Backup Repo: https://github.com/marvin1099/StreamCliCounters

# Install
Get it from one of these:  
[Codeberg Releases](https://codeberg.org/marvin1099/StreamCliCounters/releases)   
[Github Releases](https://github.com/marvin1099/StreamCliCounters/releases)   

Requires Python 3.

# Explanation
First get Python and the script from above.  
Next open a terminal in the script folder and run:

    ./AdCliCounter.py -c MyKills -p "Kills: " -d

To make a Kills counter with shortcuts for adding and subtracting.  
The `-d` flag creates shortcuts right away (use `-w` to make this happen automatically for all future counters).  
A `MyKills.txt` will also be created in the script folder for use in your stream.  

Now use the shortcuts to add, subtract, or reset the counter.  

Run the following to see the full CLI help:

    ./AdCliCounter.py -h

# Usage

    usage: AdCliCounter.py [-h] [-j JSON] [-o] [-c CREATE] [-t SELECT] [-i] [-r] [-n RENAME] [-x PREFIX]
                           [-p PREFIX] [-y SUFFIX] [-s SUFFIX] [-u VALUE] [-v VALUE] [-e SET]
                           [-a ADD] [-w] [-d] [-l] [-m]

    A counter manager

    options:
      -h, --help                 show this help message and exit
      -j, --json JSON            path to counter config (default: 'counters.json')
      -o, --selectcreation       auto-select counter on creation; use twice to disable
      -c, --create CREATE        create a new counter with a name
      -t, --select SELECT        select a counter to use
      -i, --pointer              print the selected counter
      -r, --remove               remove the selected counter
      -n, --rename RENAME        rename the selected counter
      -x, --defaultprefix PREFIX set default prefix for new counters
      -p, --prefix PREFIX        set prefix for the selected counter
      -y, --defaultsuffix SUFFIX set default suffix for new counters
      -s, --suffix SUFFIX        set suffix for the selected counter
      -u, --defaultvalue VALUE   set default value for new counters
      -v, --value VALUE          set value when creating a counter
      -e, --set SET              set the selected counter to a specific number
      -a, --add ADD              add/subtract from the selected counter (+/-)
      -w, --defaultshortcut      create shortcuts on counter creation; use twice to disable
      -d, --createshortcut       create shortcuts for the selected counter; use twice to delete
      -l, --list                 list all counters (** marks the selected one)
      -m, --interactivemode      launch the interactive menu mode

# Interactive Mode

Run the script with `-m` or `--interactivemode` to enter a menu-driven interface:

    ./AdCliCounter.py -m

The menu shows the current state and provides numbered options for all operations:

- **1** – List counters
- **2** – Show selected counter
- **3** – Select a counter
- **4** – Create a counter
- **5** – Rename a counter
- **6** – Remove a counter
- **7** – Set counter value
- **8** – Change counter (+/-)
- **9** – Set prefix
- **10** – Set suffix
- **11–13** – Set default prefix / suffix / value
- **14** – Toggle select on creation
- **15** – Toggle default shortcut
- **16** – Create shortcuts
- **17** – Delete shortcuts
- **q** – Quit

# Example
Keep in mind the script should be run in the desired counter folder  
as a working directory to generate the files in the desired folder.  

Let's make up a scenario.  
You want to count the coins of a game manually.  
There are coins that give 5 points, give 10 points, and one that takes 3 points.  

To make a counter for this open a terminal and run:

    ./AdCliCounter.py -c Coins -p "My Collected Coin Points: " -d

The `-d` flag creates shortcuts right away. Use `-w` if you want all future counters to get shortcuts automatically.  
This creates three shortcut files:

    Coins add.desktop   (or Coins add.vbs on Windows)  – adds 1
    Coins sub.desktop   (or Coins sub.vbs on Windows)  – subtracts 1
    Coins res.desktop   (or Coins res.vbs on Windows)  – resets to 0

Now we need to adjust them for our coin values (5, 10, -3).  
Open `Coins add.desktop` in your favorite editor.  
Modify `Exec=` (Linux) or `WShell.Run ""` (Windows) to use 5 instead of 1, then save.  
Copy that file to `Coins 10.desktop` and change its value to 10.  
Open `Coins sub.desktop` and change -1 to -3.  

Now you're done – you can use `Coins.txt` in your stream.

# DefaultCounter
The default counter was removed in version 0.2.  
It wasn't that useful and can be recreated by running:

    ./AdCliCounter.py -c default -p "Default: "

# ManualEdits
Manual edits to `counters.json` are possible, but I recommend using the CLI interface or the interactive menu (`-m`) instead. That's less error-prone.  
The structure is straightforward, but if you do edit by hand, be careful not to break the JSON format.

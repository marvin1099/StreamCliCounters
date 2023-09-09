#!/bin/python
import os
import json
import shutil
import argparse
import platform

class CounterManager:
    def __init__(self, config_file=None):
        self.fullscript = os.path.realpath(__file__)
        if config_file == None:
            self.config_file = os.path.realpath("counters.json")
        else:
            self.config_file = os.path.realpath(config_file)
        self.savedir = os.path.dirname(self.config_file)
        self.default_application = 'AdCliCounter.py'
        self.config_application = self.default_application
        self.default_version = 0.2
        self.config_version = self.default_version
        self.default_prefix = ''
        self.default_value = 0
        self.default_change = 1
        self.default_suffix = ''
        self.default_shortcut = False
        self.selected_counter = None
        self.select_on_creation = False
        self.counters = {}
        self.load_config()
        self.validate_version()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
                self.config_application = config_data.get('default_application', None)
                self.config_version = config_data.get('default_version', None)
                self.default_prefix = config_data.get('default_prefix', '')
                self.default_value = config_data.get('default_value', 0)
                self.default_change = config_data.get('default_change', 1)
                self.default_suffix = config_data.get('default_suffix', '')
                self.default_shortcut = config_data.get('default_shortcut', False)
                self.selected_counter = config_data.get('selected_counter', None)
                self.select_on_creation = config_data.get('select_on_creation', False)
                self.counters = config_data.get('counters', {})

    def backup_config(self):
        if os.path.exists(self.config_file):
            filename, file_extension = os.path.splitext(self.config_file)
            backupfile = filename + ".backup" + file_extension
            shutil.copyfile(self.config_file, backupfile)
            print(f"A backup of the config file '{self.config_file}' was made to '{backupfile}'")

    def save_config(self):
        config_data = {
            'default_application': self.default_application,
            'default_version': self.default_version,
            'default_prefix': self.default_prefix,
            'default_value': self.default_value,
            'default_change': self.default_change,
            'default_suffix': self.default_suffix,
            'default_shortcut': self.default_shortcut,
            'selected_counter': self.selected_counter,
            'select_on_creation': self.select_on_creation,
            'counters': self.counters
        }
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=4)

    def validate_version(self):
        if self.default_application == self.config_application:
            if self.config_version == None:
                print("Error the config file has no version")
                exit(1)
            elif self.default_version < self.config_version:
                print(f"Warning config file was made for the newer version '{self.config_version}'")
            elif self.config_version == 0.1:
                print(f"Warning config file was made for the older version '{self.config_version}'")
                self.counters = {}
                backup_config()
                print("Deleteing old counter data")
                self.save_config()
            elif self.default_version > self.config_version:
                print(f"Warning config file was made for the older version '{self.config_version}'")
        else:
            print(f"Error the config file was made for the application '{self.config_application}'")
            exit(1)

    def create_counter(self,name=None,prefix=None,value=None,suffix=None):
        if prefix == None:
            prefix = self.default_prefix
        if value == None:
            value = self.default_value
        if suffix == None:
            suffix = self.default_suffix
        if name != None:
            if name not in self.counters:
                data = {"prefix":prefix,"value":value,"suffix":suffix}
                self.counters[name] = data
                print(f"Counter '{name}' was created and is '{prefix}{value}{suffix}'")
                if self.select_on_creation or self.selected_counter == None:
                    self.selected_counter = name
                    print(f"Selected counter '{name}'")
                self.save_config()
                self.save_stream_counter(name)
            else:
                print(f"Warning, counter '{name}' allredy exists, skipping counter creation")

    def rename_counter(self,name=None,new_name=None):
        if name == None:
            name = self.selected_counter
        if new_name != None and name != None and name != new_name:
            if new_name not in self.counters:
                self.delete_stream_counter(name)
                self.counters[new_name] = self.counters.pop(name)
                print(f"Renamed counter '{name}' to '{new_name}'")
                if self.selected_counter == name:
                    self.selected_counter = new_name
                    print(f"Selected counter '{new_name}'")
                self.save_config()
                self.save_stream_counter(name)
            else:
                print(f"Warning, can't rename '{name}' to '{new_name}', the counter '{new_name}' allready exists")
        else:
            print("Warning, old/new counter names are missing or are the same")

    def remove_counter(self,name=None):
        if name == None:
            name = self.selected_counter
        if name in self.counters:
            self.delete_stream_counter(name)
            counternames = list(self.counters.keys())
            self.counters.pop(name)
            print(f"Removed counter '{name}'")
            if self.selected_counter == name:
                if len(counternames) > 1:
                    idx = counternames.index(name)
                    if int(idx+2) > len(counternames):
                        idx = 0
                    else:
                        idx += 1
                    self.selected_counter = counternames[idx]
                    print(f"Selected counter '{counternames[idx]}'")
                else:
                    self.selected_counter = None
                    print("Deselected counter")
            self.save_config()
        else:
            print(f"Warning, counter '{name}' does not exist, skipping counter removal")

    def prefix_counter(self,name=None,prefix=None):
        if name == None:
            name = self.selected_counter
        if prefix == None:
            prefix = self.default_prefix
        if name in self.counters:
            self.counters[name]["prefix"] = prefix
            print(f"Set prefix of '{name}' to '{prefix}'")
            if self.selected_counter != name:
                self.selected_counter = name
                print(f"Selected counter '{name}'")
            self.save_config()
            self.save_stream_counter(name)
        else:
            print(f"Warning, counter '{name}' does not exist, skipping setting prefix")

    def suffix_counter(self,name=None,suffix=None):
        if name == None:
            name = self.selected_counter
        if suffix == None:
            suffix = self.default_suffix
        if name in self.counters:
            self.counters[name]["suffix"] = suffix
            print(f"Set prefix of '{name}' to '{suffix}'")
            if self.selected_counter != name:
                self.selected_counter = name
                print(f"Selected counter '{name}'")
            self.save_config()
            self.save_stream_counter(name)
        else:
            print(f"Warning, counter '{name}' does not exist, skipping setting suffix")

    def select_counter(self,name=None):
        if name != self.selected_counter and name in self.counters:
            self.selected_counter = name
            print(f"Selected counter '{name}'")
            self.save_config()
        elif name == self.selected_counter:
            print(f"Warning, counter '{name}' is allready selected")
        else:
            print(f"Warning, counter '{name}' does not exist, skipping counter selection")

    def get_selected_counter(self):
        name = self.selected_counter
        if name in self.counters:
            data = self.counters[name]
            print(f"Selected is the counter '{name}' that is set to '{data['prefix']}{data['value']}{data['suffix']}'")
        else:
            print(f"No counter is selected")

    def set_counter(self,name=None,value=None):
        if name == None:
            name = self.selected_counter
        if value == None:
            value = self.default_value
        if name in self.counters:
            self.counters[name]["value"] = value
            print(f"Set counter '{name}' to '{value}'")
            self.selected_counter = name
            self.save_config()
            self.save_stream_counter(name)
        else:
            print(f"Warning, counter '{name}' does not exist, skipping setting counter")

    def change_conter(self,name=None,change=None):
        if name == None:
            name = self.selected_counter
        if change == None:
            value = self.default_change
        if name in self.counters:
            self.counters[name]["value"] += change
            print(f"Changed counter '{name}' by '{change}', now it's '{self.counters[name]['value']}'")
            if self.selected_counter != name:
                self.selected_counter = name
                print(f"Selected counter '{name}'")
            self.save_config()
            self.save_stream_counter(name)
        else:
            print(f"Warning, counter '{name}' does not exist, skipping counter change")

    def list_counters(self):
        for name, data in self.counters.items():
            print(f"Counter '{name}' is '{data['prefix']}{data['value']}{data['suffix']}'")
        if self.counters == {}:
            print("Warning, no counters are defined")

    def save_stream_counter(self,name=None):
        if name == None:
            name = self.selected_counter
        if name in self.counters:
            data = self.counters[name]
            self.save_file(name + ".txt",data['prefix'] + str(data['value']) + data['suffix'])
        else:
            print(f"Warning, counter '{name}' does not exist, skipping stream counter save")

    def delete_stream_counter(self,name=None):
        if name == None:
            name = self.selected_counter
        if name in self.counters:
            try:
                os.remove(os.path.join(self.savedir,name + ".txt"))
            except:
                pass
        else:
            print(f"Warning, counter '{name}' does not exist, skipping shortcut deletion")

    def create_shortcuts(self,name=None):
        if name == None:
            name = self.selected_counter
        if name in self.counters:
            if platform.system() == "Linux" or platform.system() == "Darwin":
                ext = ".desktop"
                fcont = """[Desktop Entry]
Comment={C}
Exec={E}
Name={N}
Path={P}
StartupNotify=true
Terminal=false
Type=Application"""
            elif platform.system() == "Windows":
                ext = ".vbs"
                fcont = """Dim WShell
Set WShell = CreateObject("WScript.Shell")
Rem Comment "{C}"
WShell.CurrentDirectory = "{P}"
Rem Name "{N}"
WShell.Run "{E}"
Set WShell = Nothing"""
            else:
                print("Warning, unsuported operating system for shortcuts, skipping shortcut creation")
                return
            script = self.fullscript
            folder = self.savedir
            self.save_file(name + " add" + ext,fcont.format(C="add 1 to " + name,E="python '" + script + "' -t '" + name + "' -a 1",N=name + " add",P=folder))
            self.save_file(name + " sub" + ext,fcont.format(C="sub 1 to " + name,E="python '" + script + "' -t '" + name + "' -a -1",N=name + " sub",P=folder))
            self.save_file(name + " res" + ext,fcont.format(C="set " + name + " to 0",E="python '" + script + "' -t '" + name + "' -e 0",N=name + " res",P=folder))
        else:
            print(f"Warning, counter '{name}' does not exist, skipping shortcut creation")


    def delete_shortcuts(self,name=None):
        if name == None:
            name = self.selected_counter
        if name in self.counters:
            if platform.system() == "Linux" or platform.system() == "Darwin":
                ext = ".desktop"
            elif platform.system() == "Windows":
                ext = ".vbs"
            else:
                return
            self.delete_file(name + " add" + ext)
            self.delete_file(name + " sub" + ext)
            self.delete_file(name + " res" + ext)
        else:
            print(f"Warning, counter '{name}' does not exist, skipping shortcut deletion")

    def delete_file(self,filename=None):
        if filename != None:
            try:
                os.remove(os.path.join(self.savedir,filename))
            except:
                pass

    def save_file(self,filename,savedata):
        with open(os.path.join(self.savedir,filename), 'w') as f:
            f.write(savedata)


def main():
    parser = argparse.ArgumentParser(
    prog='AdCliCounter.py',
    description='A counter manager',
    epilog='')
    parser.add_argument('-j', '--json', help='where is your conter config (default \'counters.json\')')
    parser.add_argument('-o', '--selectcreation', action='count', default=0, help='auto select counter on creation, add twice to disable')
    parser.add_argument('-c', '--create', help='create a new counter with a custom name')
    parser.add_argument('-t', '--select', help='select a counter to use')
    parser.add_argument('-i', '--pointer', action='store_true', help='print the selected counter')
    parser.add_argument('-r', '--remove', action='store_true', help='remove the selected counter')
    parser.add_argument('-n', '--rename', help='rename the selected counter')
    parser.add_argument('-x', '--defaultprefix', help='set default prefix for when creating counters')
    parser.add_argument('-p', '--prefix', help='set prefix for created or selected counter')
    parser.add_argument('-y', '--defaultsuffix', help='set sufix for for when creating counters')
    parser.add_argument('-s', '--suffix', help='set sufix for created or selected counter')
    parser.add_argument('-u', '--defaultvalue', help='set default value for when creating counters')
    parser.add_argument('-v', '--value', type=int, help='set value for when creating counters')
    parser.add_argument('-e', '--set', type=int, help='set the selected counter to any number')
    #parser.add_argument('-b', '--defaultchange', help='set default change for when adding counters') #not needed
    parser.add_argument('-a', '--add', type=int, help='change the counter by +/-x')
    parser.add_argument('-w', '--defaultshortcut', action='count', default=0, help='create shortcuts on counter creation, add twice to disable')
    parser.add_argument('-d', '--createshortcut', action='count', default=0, help='make shortcuts for selected counter, add twice to delete shortcuts')
    parser.add_argument('-l', '--list', action='store_true', help='list available counters')

    args = parser.parse_args()
    counter_manager = CounterManager(args.json)

    if args.selectcreation == 1: #select_on_creation
        counter_manager.select_on_creation = True
        counter_manager.save_config()
    elif args.selectcreation > 1:
        counter_manager.select_on_creation = False
        counter_manager.save_config()

    if args.create: #create_counter
        counter_manager.create_counter(args.create,args.prefix,args.value,args.suffix)
        args.prefix = None
        args.suffix = None
    if args.select: #select_counter
        counter_manager.select_counter(name=args.select)
    if args.pointer:
        counter_manager.get_selected_counter()

    if args.remove: #remove_counter
        counter_manager.remove_counter()
    if args.rename: #rename_counter
        counter_manager.rename_counter(new_name=args.rename)

    if args.defaultprefix: #default_prefix
        counter_manager.default_prefix = args.defaultprefix
        counter_manager.save_config()
    if args.prefix: #prefix_counter
        counter_manager.prefix_counter(prefix=args.prefix)

    if args.defaultsuffix: #default_suffix
        counter_manager.default_suffix = args.defaultsuffix
        counter_manager.save_config()
    if args.suffix: #suffix_counter
        counter_manager.suffix_counter(suffix=args.suffix)

    if args.defaultvalue: #default_value
        counter_manager.default_value = args.defaultvalue
        counter_manager.save_config()
    if args.set != None: #set_counter
        counter_manager.set_counter(value=args.set)

    #if args.defaultchange: #default_change #not needed
    #    counter_manager.default_change = args.defaultchange
    #    counter_manager.self.save_config()
    if args.add != None: #change_counter
        counter_manager.change_conter(change=args.add)

    if args.defaultshortcut == 1: #default_shortcut
        counter_manager.default_shortcut = True
        counter_manager.save_config()
    elif args.defaultshortcut > 1:
        counter_manager.default_shortcut = False
        counter_manager.save_config()
    if args.createshortcut == 1: #create_shortcuts
        counter_manager.create_shortcuts()
    if args.createshortcut > 1:
        counter_manager.delete_shortcuts()

    if args.list: #list_counters
        counter_manager.list_counters()


if __name__ == "__main__":
    main()

#!/bin/python
import os
import json
import shutil
import argparse
import platform


class CounterManager:
    def __init__(self, config_file=None):
        self.fullscript = os.path.realpath(__file__)
        if config_file is None:
            self.config_file = os.path.realpath("counters.json")
        else:
            self.config_file = os.path.realpath(config_file)
        self.savedir = os.path.dirname(self.config_file)
        self.default_application = "AdCliCounter.py"
        self.config_application = self.default_application
        self.default_version = 0.2
        self.config_version = self.default_version
        self.default_prefix = ""
        self.default_value = 0
        self.default_suffix = ""
        self.default_shortcut = False
        self.selected_counter = None
        self.select_on_creation = False
        self.counters = {}
        self.load_config()
        self.validate_version()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config_data = json.load(f)
                self.config_application = config_data.get("default_application", None)
                self.config_version = config_data.get("default_version", None)
                self.default_prefix = config_data.get("default_prefix", "")
                self.default_value = config_data.get("default_value", 0)
                self.default_suffix = config_data.get("default_suffix", "")
                self.default_shortcut = config_data.get("default_shortcut", False)
                self.selected_counter = config_data.get("selected_counter", None)
                self.select_on_creation = config_data.get("select_on_creation", False)
                self.counters = config_data.get("counters", {})

    def backup_config(self):
        if os.path.exists(self.config_file):
            filename, file_extension = os.path.splitext(self.config_file)
            backupfile = filename + ".backup" + file_extension
            shutil.copyfile(self.config_file, backupfile)
            print(f"Backup saved to '{backupfile}'")

    def save_config(self):
        config_data = {
            "default_application": self.default_application,
            "default_version": self.default_version,
            "default_prefix": self.default_prefix,
            "default_value": self.default_value,
            "default_suffix": self.default_suffix,
            "default_shortcut": self.default_shortcut,
            "selected_counter": self.selected_counter,
            "select_on_creation": self.select_on_creation,
            "counters": self.counters,
        }
        with open(self.config_file, "w") as f:
            json.dump(config_data, f, indent=4)

    def validate_version(self):
        if self.default_application == self.config_application:
            if self.config_version is None:
                print("Error: config file has no version")
                exit(1)
            elif self.default_version < self.config_version:
                print(
                    f"Warning: config file was made for newer version '{self.config_version}'"
                )
            elif self.config_version == 0.1:
                print(
                    f"Warning: config file was made for older version '{self.config_version}'"
                )
                self.counters = {}
                self.backup_config()
                print("Deleting old counter data")
                self.save_config()
            elif self.default_version > self.config_version:
                print(
                    f"Warning: config file was made for older version '{self.config_version}'"
                )
        else:
            print(
                f"Error: config file was made for application '{self.config_application}'"
            )
            exit(1)

    def create_counter(self, name=None, prefix=None, value=None, suffix=None):
        if prefix is None:
            prefix = self.default_prefix
        if value is None:
            value = self.default_value
        if suffix is None:
            suffix = self.default_suffix
        if name is not None:
            if name not in self.counters:
                data = {"prefix": prefix, "value": value, "suffix": suffix}
                self.counters[name] = data
                print(f"Counter '{name}' was created and is '{prefix}{value}{suffix}'")
                if self.select_on_creation or self.selected_counter is None:
                    self.selected_counter = name
                    print(f"Selected counter '{name}'")
                self.save_config()
                self.save_stream_counter(name)
            else:
                print(f"Warning: counter '{name}' already exists, skipping creation")

    def rename_counter(self, name=None, new_name=None):
        if name is None:
            name = self.selected_counter
        if new_name is not None and name is not None and name != new_name:
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
                print(
                    f"Warning: can't rename '{name}' to '{new_name}', counter '{new_name}' already exists"
                )
        else:
            print("Warning: old/new counter names are missing or are the same")

    def remove_counter(self, name=None):
        if name is None:
            name = self.selected_counter
        if name in self.counters:
            self.delete_stream_counter(name)
            names = list(self.counters)
            names_before = names.index(name)
            self.counters.pop(name)
            print(f"Removed counter '{name}'")
            if self.selected_counter == name:
                if len(names) > 1:
                    idx = 0 if names_before + 1 >= len(names) else names_before + 1
                    self.selected_counter = names[idx]
                    print(f"Selected counter '{names[idx]}'")
                else:
                    self.selected_counter = None
                    print("Deselected counter")
            self.save_config()
        else:
            print(f"Warning: counter '{name}' does not exist, skipping removal")

    def prefix_counter(self, name=None, prefix=None):
        if name is None:
            name = self.selected_counter
        if prefix is None:
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
            print(f"Warning: counter '{name}' does not exist, skipping prefix change")

    def suffix_counter(self, name=None, suffix=None):
        if name is None:
            name = self.selected_counter
        if suffix is None:
            suffix = self.default_suffix
        if name in self.counters:
            self.counters[name]["suffix"] = suffix
            print(f"Set suffix of '{name}' to '{suffix}'")
            if self.selected_counter != name:
                self.selected_counter = name
                print(f"Selected counter '{name}'")
            self.save_config()
            self.save_stream_counter(name)
        else:
            print(f"Warning: counter '{name}' does not exist, skipping suffix change")

    def select_counter(self, name=None):
        if name != self.selected_counter and name in self.counters:
            self.selected_counter = name
            print(f"Selected counter '{name}'")
            self.save_config()
        elif name == self.selected_counter:
            print(f"Warning: counter '{name}' is already selected")
        else:
            print(f"Warning: counter '{name}' does not exist, skipping selection")

    def get_selected_counter(self):
        name = self.selected_counter
        if name in self.counters:
            data = self.counters[name]
            print(
                f"Selected counter '{name}': prefix='{data['prefix']}', value={data['value']}, suffix='{data['suffix']}'"
            )
        else:
            print("No counter selected")

    def set_counter(self, name=None, value=None):
        if name is None:
            name = self.selected_counter
        if value is None:
            value = self.default_value
        if name in self.counters:
            self.counters[name]["value"] = value
            print(f"Set counter '{name}' to '{value}'")
            self.selected_counter = name
            self.save_config()
            self.save_stream_counter(name)
        else:
            print(f"Warning: counter '{name}' does not exist, skipping set")

    def change_conter(self, name=None, change=None):
        if name is None:
            name = self.selected_counter
        if name in self.counters:
            self.counters[name]["value"] += change
            print(
                f"Changed counter '{name}' by '{change}', now it's '{self.counters[name]['value']}'"
            )
            if self.selected_counter != name:
                self.selected_counter = name
                print(f"Selected counter '{name}'")
            self.save_config()
            self.save_stream_counter(name)
        else:
            print(f"Warning: counter '{name}' does not exist, skipping change")

    def list_counters(self):
        for name, data in self.counters.items():
            sel = " **" if name == self.selected_counter else ""
            print(
                f"Counter '{name}': prefix='{data['prefix']}', value={data['value']}, suffix='{data['suffix']}'{sel}"
            )
        if not self.counters:
            print("Warning: no counters defined")

    def save_stream_counter(self, name=None):
        if name is None:
            name = self.selected_counter
        if name in self.counters:
            data = self.counters[name]
            self.save_file(
                name + ".txt", data["prefix"] + str(data["value"]) + data["suffix"]
            )
        else:
            print(f"Warning: counter '{name}' does not exist, skipping stream save")

    def delete_stream_counter(self, name=None):
        if name is None:
            name = self.selected_counter
        if name in self.counters:
            try:
                os.remove(os.path.join(self.savedir, name + ".txt"))
            except OSError:
                pass
        else:
            print(
                f"Warning: counter '{name}' does not exist, skipping stream file deletion"
            )

    def create_shortcuts(self, name=None):
        if name is None:
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
                print(
                    "Warning: unsupported operating system for shortcuts, skipping creation"
                )
                return
            script = self.fullscript
            folder = self.savedir
            self.save_file(
                name + " add" + ext,
                fcont.format(
                    C="add 1 to " + name,
                    E="python '" + script + "' -t '" + name + "' -a 1",
                    N=name + " add",
                    P=folder,
                ),
            )
            self.save_file(
                name + " sub" + ext,
                fcont.format(
                    C="sub 1 to " + name,
                    E="python '" + script + "' -t '" + name + "' -a -1",
                    N=name + " sub",
                    P=folder,
                ),
            )
            self.save_file(
                name + " res" + ext,
                fcont.format(
                    C="set " + name + " to 0",
                    E="python '" + script + "' -t '" + name + "' -e 0",
                    N=name + " res",
                    P=folder,
                ),
            )
        else:
            print(
                f"Warning: counter '{name}' does not exist, skipping shortcut creation"
            )

    def delete_shortcuts(self, name=None):
        if name is None:
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
            print(
                f"Warning: counter '{name}' does not exist, skipping shortcut deletion"
            )

    def delete_file(self, filename=None):
        if filename is not None:
            try:
                os.remove(os.path.join(self.savedir, filename))
            except OSError:
                pass

    def save_file(self, filename, savedata):
        with open(os.path.join(self.savedir, filename), "w") as f:
            f.write(savedata)

    def interactive_mode(self):
        while True:
            print("\n=== Interactive Counter Manager ===")
            if self.selected_counter and self.selected_counter in self.counters:
                data = self.counters[self.selected_counter]
                print(
                    f"  Selected: '{self.selected_counter}': prefix='{data['prefix']}', value={data['value']}, suffix='{data['suffix']}'"
                )
            else:
                print("  Selected: None")
            print(
                f"  Defaults: prefix='{self.default_prefix}' value={self.default_value} suffix='{self.default_suffix}' select_on_creation={self.select_on_creation} default_shortcut={self.default_shortcut}"
            )
            print()
            print("  1) List counters")
            print("  2) Show selected counter")
            print("  3) Select counter")
            print("  4) Create counter")
            print("  5) Rename counter")
            print("  6) Remove counter")
            print("  7) Set counter value")
            print("  8) Change counter (+/-)")
            print("  9) Set prefix")
            print(" 10) Set suffix")
            print(" 11) Set default prefix")
            print(" 12) Set default suffix")
            print(" 13) Set default value")
            print(" 14) Toggle select on creation")
            print(" 15) Toggle default shortcut")
            print(" 16) Create shortcuts")
            print(" 17) Delete shortcuts")
            print("  q) Quit")
            choice = input("\nChoose an option: ").strip().lower()

            if choice == "q":
                print("Exiting interactive mode.")
                break
            elif choice == "1":
                self.list_counters()
            elif choice == "2":
                self.get_selected_counter()
            elif choice == "3":
                name = input("Counter name: ").strip()
                if name:
                    self.select_counter(name)
                else:
                    print("No name entered.")
            elif choice == "4":
                name = input("Counter name: ").strip()
                if not name:
                    print("No name entered.")
                    continue
                prefix = (
                    input(f"Prefix (default '{self.default_prefix}'): ").strip() or None
                )
                value_str = input(f"Value (default {self.default_value}): ").strip()
                value = int(value_str) if value_str else None
                suffix = (
                    input(f"Suffix (default '{self.default_suffix}'): ").strip() or None
                )
                self.create_counter(name, prefix, value, suffix)
                if self.default_shortcut:
                    self.create_shortcuts(name)
            elif choice == "5":
                name = (
                    input("Counter name to rename (default selected): ").strip() or None
                )
                new_name = input("New name: ").strip()
                if new_name:
                    self.rename_counter(name, new_name)
                else:
                    print("No new name entered.")
            elif choice == "6":
                name = (
                    input("Counter name to remove (default selected): ").strip() or None
                )
                self.remove_counter(name)
            elif choice == "7":
                name = input("Counter name (default selected): ").strip() or None
                value_str = input("Value: ").strip()
                if value_str:
                    self.set_counter(name, int(value_str))
                else:
                    print("No value entered.")
            elif choice == "8":
                name = input("Counter name (default selected): ").strip() or None
                change_str = input("Change by (+/-): ").strip()
                if change_str:
                    self.change_conter(name, int(change_str))
                else:
                    print("No change entered.")
            elif choice == "9":
                name = input("Counter name (default selected): ").strip() or None
                prefix = input("Prefix: ").strip()
                if prefix:
                    self.prefix_counter(name, prefix)
                else:
                    print("No prefix entered.")
            elif choice == "10":
                name = input("Counter name (default selected): ").strip() or None
                suffix = input("Suffix: ").strip()
                if suffix:
                    self.suffix_counter(name, suffix)
                else:
                    print("No suffix entered.")
            elif choice == "11":
                val = input("New default prefix: ").strip()
                if val:
                    self.default_prefix = val
                    self.save_config()
                    print(f"Default prefix set to '{val}'")
                else:
                    print("No value entered.")
            elif choice == "12":
                val = input("New default suffix: ").strip()
                if val:
                    self.default_suffix = val
                    self.save_config()
                    print(f"Default suffix set to '{val}'")
                else:
                    print("No value entered.")
            elif choice == "13":
                val_str = input("New default value: ").strip()
                if val_str:
                    self.default_value = int(val_str)
                    self.save_config()
                    print(f"Default value set to {val_str}")
                else:
                    print("No value entered.")
            elif choice == "14":
                self.select_on_creation = not self.select_on_creation
                self.save_config()
                print(f"Select on creation set to {self.select_on_creation}")
            elif choice == "15":
                self.default_shortcut = not self.default_shortcut
                self.save_config()
                print(f"Default shortcut set to {self.default_shortcut}")
            elif choice == "16":
                name = input("Counter name (default selected): ").strip() or None
                self.create_shortcuts(name)
            elif choice == "17":
                name = input("Counter name (default selected): ").strip() or None
                self.delete_shortcuts(name)
            else:
                print("Invalid option. Please try again.")


def main():
    parser = argparse.ArgumentParser(
        prog="AdCliCounter.py", description="A counter manager", epilog=""
    )
    parser.add_argument(
        "-j", "--json", help="where is your conter config (default 'counters.json')"
    )
    parser.add_argument(
        "-o",
        "--selectcreation",
        action="count",
        default=0,
        help="auto select counter on creation, add twice to disable",
    )
    parser.add_argument(
        "-c", "--create", help="create a new counter with a custom name"
    )
    parser.add_argument("-t", "--select", help="select a counter to use")
    parser.add_argument(
        "-i", "--pointer", action="store_true", help="print the selected counter"
    )
    parser.add_argument(
        "-r", "--remove", action="store_true", help="remove the selected counter"
    )
    parser.add_argument("-n", "--rename", help="rename the selected counter")
    parser.add_argument(
        "-x", "--defaultprefix", help="set default prefix for when creating counters"
    )
    parser.add_argument(
        "-p", "--prefix", help="set prefix for created or selected counter"
    )
    parser.add_argument(
        "-y", "--defaultsuffix", help="set sufix for for when creating counters"
    )
    parser.add_argument(
        "-s", "--suffix", help="set sufix for created or selected counter"
    )
    parser.add_argument(
        "-u", "--defaultvalue", help="set default value for when creating counters"
    )
    parser.add_argument(
        "-v", "--value", type=int, help="set value for when creating counters"
    )
    parser.add_argument(
        "-e", "--set", type=int, help="set the selected counter to any number"
    )
    # parser.add_argument('-b', '--defaultchange', help='set default change for when adding counters') #not needed
    parser.add_argument("-a", "--add", type=int, help="change the counter by +/-x")
    parser.add_argument(
        "-w",
        "--defaultshortcut",
        action="count",
        default=0,
        help="create shortcuts on counter creation, add twice to disable",
    )
    parser.add_argument(
        "-d",
        "--createshortcut",
        action="count",
        default=0,
        help="make shortcuts for selected counter, add twice to delete shortcuts",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="list available counters"
    )
    parser.add_argument(
        "-m",
        "--interactivemode",
        action="store_true",
        help="start interactive menu mode",
    )

    args = parser.parse_args()
    counter_manager = CounterManager(args.json)

    if args.interactivemode:
        counter_manager.interactive_mode()
        return

    if args.selectcreation == 1:  # select_on_creation
        counter_manager.select_on_creation = True
        counter_manager.save_config()
    elif args.selectcreation > 1:
        counter_manager.select_on_creation = False
        counter_manager.save_config()

    if args.create:  # create_counter
        counter_manager.create_counter(
            args.create, args.prefix, args.value, args.suffix
        )
        args.prefix = None
        args.suffix = None
    if args.select:  # select_counter
        counter_manager.select_counter(name=args.select)
    if args.pointer:
        counter_manager.get_selected_counter()

    if args.remove:  # remove_counter
        counter_manager.remove_counter()
    if args.rename:  # rename_counter
        counter_manager.rename_counter(new_name=args.rename)

    if args.defaultprefix:  # default_prefix
        counter_manager.default_prefix = args.defaultprefix
        counter_manager.save_config()
    if args.prefix:  # prefix_counter
        counter_manager.prefix_counter(prefix=args.prefix)

    if args.defaultsuffix:  # default_suffix
        counter_manager.default_suffix = args.defaultsuffix
        counter_manager.save_config()
    if args.suffix:  # suffix_counter
        counter_manager.suffix_counter(suffix=args.suffix)

    if args.defaultvalue:  # default_value
        counter_manager.default_value = args.defaultvalue
        counter_manager.save_config()
    if args.set is not None:  # set_counter
        counter_manager.set_counter(value=args.set)

    if args.add is not None:  # change_counter
        counter_manager.change_conter(change=args.add)

    if args.defaultshortcut == 1:  # default_shortcut
        counter_manager.default_shortcut = True
        counter_manager.save_config()
    elif args.defaultshortcut > 1:
        counter_manager.default_shortcut = False
        counter_manager.save_config()
    if args.createshortcut == 1:  # create_shortcuts
        counter_manager.create_shortcuts()
    if args.createshortcut > 1:
        counter_manager.delete_shortcuts()

    if args.list:  # list_counters
        counter_manager.list_counters()


if __name__ == "__main__":
    main()

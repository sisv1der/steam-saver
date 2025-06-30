#!/usr/bin/python3

import subprocess
import os
import sys
import datetime

args = sys.argv[1:]

def print_help_page():
    HELP_TEXT = """
    Usage:
        steam-saver [-h|--help] [TARGET]

    Exports Steam saves from Proton prefix into TARGET folder and pushes them to your git repo.

    Options:
        -h, --help     Show this help page

    Arguments:
        TARGET         Target folder path (required)
    """
    print(HELP_TEXT)

if len(args) == 0:
    print_help_page()
    sys.exit("Error: TARGET path not specified.")

if ('-h' in args or '--help' in args):
    print_help_page()
    sys.exit(0)

if not os.path.isdir(args[0]):
    print("Error: Target directory does not exist.")
    sys.exit(1)

def get_steam_path():
    FLATPAK_PATH    = os.path.expanduser('~/.var/app/com.valvesoftware.Steam/.local/share/Steam/')
    LOCAL_PATH      = os.path.expanduser('~/.local/share/Steam/')
    HOME_PATH       = os.path.expanduser('~/.steam/steam/')

    if (os.path.isdir(FLATPAK_PATH)):
        return FLATPAK_PATH
    elif (os.path.isdir(LOCAL_PATH)):
        return LOCAL_PATH
    elif (os.path.isdir(HOME_PATH)):
        return HOME_PATH
    else:
        raise Exception('Steam directory doesn\'t exist')

def extract_save_data(compatdata_path, game_id, steam_user_path, save_data_path, target):
    src = os.path.join(compatdata_path, game_id, steam_user_path, save_data_path)
    subprocess.run(['rsync', '-a', '--exclude=Microsoft/','--exclude=EasyAntiCheat/', f'{src}/', target], check=True)

def backup_git():
    commit_msg = f'Backup {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'
    try:
        subprocess.run(['git', '-C', args[0], 'pull', '--rebase'], check=True)
        subprocess.run(['git', '-C', args[0], 'add', '.'], check=True)
        try:
            subprocess.run(['git', '-C', args[0], 'commit', '-S', '-m', commit_msg], check=True)
        except subprocess.CalledProcessError as e:
            # commit may fail if there are no changes; ignore in that case
            pass
        subprocess.run(['git', '-C', args[0], 'push'], check=True)
    except subprocess.CalledProcessError as e:
        if ('nothing to commit' in str(e)):
            sys.exit('exiting: there is nothing to commit')
            # if there is nothing to commit it is not an error
        else:
            raise e

COMPATDATA_PATH     = f'{get_steam_path()}steamapps/compatdata/'
STEAM_USER_PATH     = f'pfx/drive_c/users/steamuser/'
SAVED_GAMES_PATH    = 'Saved Games/'
ROAMING_PATH        = 'AppData/Roaming/'
GAME_IDS            = [name for name in os.listdir(COMPATDATA_PATH) if os.path.isdir(os.path.join(COMPATDATA_PATH, name))]

paths = [SAVED_GAMES_PATH, ROAMING_PATH]

def main():
    for game_id in GAME_IDS:
        for path in paths:
            extract_save_data(COMPATDATA_PATH, game_id, STEAM_USER_PATH, path, target=args[0])

    backup_git()

if __name__ == '__main__':
    main()
#!/usr/bin/python3

import subprocess
import os
import sys
import datetime

args = sys.argv[1:]

def print_help_page():
    print('steam-saver: steam-saver: [-h] [target]\n')
    print('\tExports steam saves from proton into target folder and pushes saves to your git repo.\n')
    print('\n\tIf TARGET is specified exports into TARGET path,\notherwise does nothing\n')
    print('\tIf TARGET folder is not empty, steam-saver will pull diff from repo before ')

    print('\n\tOptions:\n')
    print('\t\t-h\n')
    print('\t\t--help\toutput this page\n')
    
    print('\n\tArguments:\n')
    print('\t\tTARGET\ttarget folder path')

if ('-h' in args or '--help' in args):
    print_help_page()
    sys.exit(0)

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
            # too stupid. stderr is none so i can't catch the error
            pass
        subprocess.run(['git', '-C', args[0], 'push'], check=True)
    except subprocess.CalledProcessError as e:
        if ('nothing to commit' in str(e)):
            sys.exit(0)
            # if there is nothing to commit it is not an error
        else:
            raise e

COMPATDATA_PATH     = f'{get_steam_path()}steamapps/compatdata/'
STEAM_USER_PATH     = f'pfx/drive_c/users/steamuser/'
SAVED_GAMES_PATH    = 'Saved Games/'
ROAMING_PATH        = 'AppData/Roaming/'
GAME_IDS            = [name for name in os.listdir(COMPATDATA_PATH) if os.path.isdir(os.path.join(COMPATDATA_PATH, name))]

def main():
    for i in range(len(GAME_IDS)):
        extract_save_data(COMPATDATA_PATH, GAME_IDS[i], STEAM_USER_PATH, SAVED_GAMES_PATH, target=args[0])
        extract_save_data(COMPATDATA_PATH, GAME_IDS[i], STEAM_USER_PATH, ROAMING_PATH, target=args[0])    
    backup_git()

if __name__ == '__main__':
    main()
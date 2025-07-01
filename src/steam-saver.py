#!/usr/bin/python3

import subprocess
import os
import sys
import datetime


ARGS = sys.argv[1:]

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


if len(ARGS) == 0:
    print_help_page()
    sys.exit("Error: TARGET path not specified.")

if ('-h' in ARGS or '--help' in ARGS):
    print_help_page()
    sys.exit(0)

REPO_PATH = ARGS[0]

if not os.path.isdir(REPO_PATH):
    print("Error: Target directory does not exist.")
    sys.exit(1)

if not os.path.isdir(os.path.join(REPO_PATH, '.git')):
    sys.exit("Error: Target directory is not a Git repository.")

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


COMPATDATA_PATH     = f'{get_steam_path()}steamapps/compatdata/'
STEAM_USER_PATH     = f'pfx/drive_c/users/steamuser/'
SAVED_GAMES_PATH    = 'Saved Games/'
ROAMING_PATH        = 'AppData/Roaming/'
GAME_IDS            = [name for name in os.listdir(COMPATDATA_PATH) if os.path.isdir(os.path.join(COMPATDATA_PATH, name))]
DATETIME_NOW        = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
COMMIT_MSG          = f'Backup {DATETIME_NOW}'
SAVES_PATHS         = [
    SAVED_GAMES_PATH,
    ROAMING_PATH
]
EXCLUDE_DIRS        = [
    'Microsoft',
    'EasyAntiCheat'
]

def get_exclude_args():
    exclude_args = []
    for dir in EXCLUDE_DIRS:
        exclude_args.append(f'--exclude={dir}/')
    return exclude_args


def extract_save_data(compatdata_path, game_id, steam_user_path, save_data_path, target):
    src = os.path.join(compatdata_path, game_id, steam_user_path, save_data_path)
    rsync_command = ['rsync', '-a'] + get_exclude_args() + [f'{src}/', target]
    subprocess.run(rsync_command, check=True)


def sync_saves():
    for game_id in GAME_IDS:
        for path in SAVES_PATHS:
            extract_save_data(COMPATDATA_PATH, game_id, STEAM_USER_PATH, path, target=REPO_PATH)


def git_commit():
    subprocess.run(['git', '-C', REPO_PATH, 'add', '.'], check=True)
    try:
        subprocess.run(['git', '-C', REPO_PATH, 'commit', '-S', '-m', COMMIT_MSG], check=True)
    except subprocess.CalledProcessError as e:
        # commit may fail if there are no changes; ignore in that case
        pass


def git_pull():
    try:
        subprocess.run(['git', '-C', REPO_PATH, 'pull', '--rebase'], check=True)
    except:
        git_commit()
    finally:
        subprocess.run(['git', '-C', REPO_PATH, 'pull', '--rebase'], check=True)


def git_push():
    try:
        subprocess.run(['git', '-C', REPO_PATH, 'push'], check=True)
    except subprocess.CalledProcessError as e:
        if ('nothing to commit' in str(e)):
            sys.exit('exiting: there is nothing to commit')
            # if there is nothing to commit it is not an error
        else:
            raise e


def git_backup():
    git_commit()
    git_push()


def main():
    git_pull()

    sync_saves()

    git_backup()


if __name__ == '__main__':
    main()
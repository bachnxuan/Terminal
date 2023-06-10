import os
import sys
import time
import ctypes
import shutil
import keyboard
import platform
import subprocess
from pytube import YouTube
from src.utils import get_project_root

# Check admin privileges and restart with admin privileges if required
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()
        
# Prepare the project
root = get_project_root()
os.chdir(root)
cwd = os.getcwd()
user = os.getlogin()

if platform.system() == "Windows":
    os.system("cls")
    print(f"Python Terminal [Version 1.0.0] \nRunning in {user}'s computer")
else:
    print(f"This code only runs on Windows, not supported on {platform.uname().system}")
    print("Press space to exit...")
    keyboard.wait("space")
    sys.exit()
    
def is_youtubedl_installed():
    try:
        subprocess.run(['youtube-dl', '--version'], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

# Main
while True:
    # User input
    try:
        cmds = input(f"PT {cwd}> ").lower().split()
        cmd1 = cmds[0] if len(cmds) > 0 else ""
        cmd2 = cmds[1] if len(cmds) > 1 else ""
        cmd3 = cmds[2] if len(cmds) > 2 else ""
        cmd4 = cmds[3] if len(cmds) > 3 else ""
        cmd5 = cmds[4] if len(cmds) > 4 else ""

        # Command
        if cmd1 == 'exit' and cmd2 == cmd3 == cmd4 == cmd5 == '':
            break

        elif cmd1 == 'cd':
            if len(cmds) == 1 and cmd3 == cmd4 == cmd5 == '':
                print("Usage: cd <directory>")
            elif len(cmd2) > 0:
                try:
                    os.chdir(cmd2)
                    cwd = os.getcwd()  # Update the current working directory
                except FileNotFoundError:
                    print("Directory not found")
            else:
                print(cwd)

        elif cmd1 == 'crtuser':
            if len(cmd2) == 0:
                print("Usage: crtuser [nopass/pass] [admin] <user> <password>")
                continue
            
            elif len(cmd2) > 0:
                if cmd2 == 'nopass':
                    os.system(f"net user /add {cmd3}")
                    if cmd5 == 'admin':
                        os.system(f"net localgroup administrators {cmd3} /add")
                elif cmd2 == 'pass':
                    os.system(f"net user /add {cmd3} {cmd4}")
                    if cmd5 == 'admin':
                        os.system(f"net localgroup administrators {cmd3} /add")
            else:
                print("Invalid option for crtuser command")

        elif cmd1 == 'deluser':
            if len(cmd2) == 0:
                print("deluser <user>")
                continue
            
            elif len(cmd2) > 0:
                print(f"Do you want to delete {cmd2}?")
                q = input("(y/n): ").lower()
                if q == "y":
                    try:
                        os.system(f"net user {cmd2} /delete")
                        os.system(f"net localgroup administrators {cmd2} /delete")
                        print(f"{cmd2} has been deleted")
                    except:
                        print(f"{cmd2} does not exist or failed to be deleted")
                elif q == "n":
                    print("Command aborted")
                else:
                    print("Invalid option for deluser command")

        elif cmd1 == 'help':
            print("""
            cls
            dir, ls
            cd <directory>
            timer(Countdown timer) <second>
            rmfile <file>
            mkdir <directory>
            rmdir <directory>
            crtuser [nopass/pass] [admin] <user> <password>
            deluser <user>
            exit
            """)
            
        elif cmd1 == 'cls':
            os.system("cls")
            
        elif cmd1 == 'mkdir':
            if len(cmd2) == 0:
                print("Usage: mkdir <directory>")
            elif len(cmd2) > 0:
                try:
                    os.mkdir(cmd2)
                    print(f"Directory {cmd2} has been created")
                except FileExistsError:
                    print(f"Directory {cmd2} already exists")
            else:
                print("Invalid option for mkdir command")
                
        elif cmd1 == 'rmdir':
            if len(cmd2) == 0:
                print("Usage: rmdir <directory>")
            elif len(cmd2) > 0:
                try:
                    shutil.rmtree(cmd2)
                    print(f"Directory {cmd2} has been deleted")
                except FileNotFoundError:
                    print(f"Directory {cmd2} does not exist")
            else:
                print("Invalid option for rmdir command")
        
        elif cmd1 == 'rmfile':
            if len(cmd2) == 0:
                print("Usage: rmfile <file>")
            elif len(cmd2) > 0:
                q = input(f"Do you want to delete {cmd2}? (y/n): ").lower()
                if q == 'y':
                    try:
                        cmd2 = os.path.join(cwd, cmd2)
                        os.remove(cmd2)
                        print(f"File {cmd2} has been deleted")
                    except FileNotFoundError:
                        print(f"File {cmd2} does not exist")
                elif q == 'n':
                    print("Command aborted")
                else:
                    print("Invalid option for rmfile command")
                
        elif cmd2 == 'timer':
            if len(cmd3) == 0:
                print("Syntax error")
            if len(cmd3) > 0:
                try:
                    while cmd3:
                        mins, secs = divmod(cmd3, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        cmd3 -= 1
                    print("Completed")
                except:
                    print("Failed")
                         
        elif cmd1 in ['dir', 'ls'] and cmd2 == cmd3 == cmd4 == cmd5 == '':
            files = os.listdir(cwd)
            print("  ".join(files))

        else:
            print("Incorrect command")

    except IndexError:
        pass
    except KeyboardInterrupt:
        print("\nProgram Interrupt")
        break
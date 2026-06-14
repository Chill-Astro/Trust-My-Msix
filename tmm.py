import requests, subprocess, os, sys, ctypes, argparse
from colorama import init, Fore, Style

verUrl = "https://gist.githubusercontent.com/Chill-Astro/7e0d5246d48b0684ac303df756586c38/raw/TMM_V.txt" # Gist URL.

ver = "3.15.1.5" # I FEEL THE COLOURS

init(convert=True)

# Msix is GREAT! Very much better than typing 'Yes' a 100 times. Only thing..... you need to buy a certificate to sign the app. Soooooo, I made this to Support Hobbyists and Students who JUST WANT TO INSTALL A FOSS PROJECT. ( Ah Lamina ✦ !)

def logo():
    print(Fore.CYAN + r""" 
 _____ ___  _   _  ___ _____   __  __ __   __  __  __  ___  ___ __  __  _ 
|_   _| _ \| | | |/ __|_   _| |  \/  |\ \ / / |  \/  |/ __||_ _|\ \/ / | |
  | | |   /| |_| |\__ \ | |   | |\/| | \ V /  | |\/| |\__ \ | |  >  <  |_|
  |_| |_|_\ \___/ |___/ |_|   |_|  |_|  |_|   |_|  |_||___/|___|/_/\_\ (_)
          
(C) Chill-Astro | 2026""" + Fore.RESET)
    
def freedom(): # For the Freedom Fighters who Liberated Mother India! 
    S = Fore.LIGHTYELLOW_EX + Style.BRIGHT
    W = Fore.WHITE + Style.BRIGHT
    G = Fore.GREEN + Style.BRIGHT
    R = Style.RESET_ALL
    
    print(f"""
{S}Sarfaroshi ki tamanna ab hamare dil mein hai,
{S}Dekhna hai zor kitna baazu-e-qaatil mein hai.

{W}Waqt aane de bata denge tujhe ae aasmaan,
{W}Hum abhi se kya bataayein kya hamare dil mein hai.

{G}Khainch kar laayi hai sab ko qatl hone ki umeed,
{G}Aashiqon ka aaj jamghat koocha-e-qaatil mein hai.

{S}Hai liye hathiyaar dushman taak mein baitha udhar,
{W}Aur hum taiyaar hain seena liye apna idhar.
{G}Khoon se khelenge holi gar vatan mushkil mein hai,
{G}Sarfaroshi ki tamanna ab hamare dil mein hai.{R}
""")  

def help():      
    R = Style.RESET_ALL
    P = Fore.MAGENTA + Style.BRIGHT
    Y = Fore.YELLOW + Style.BRIGHT
    C = Fore.CYAN + Style.BRIGHT
    G = Fore.GREEN + Style.BRIGHT

    print(f"""             
Huh someone asked for help? Sure!

{P}Usage :{R} {C}tmm --i{R} {Y}<path_to_cert>{R}

{C}tmm --v{R} : {G}Show Version{R}
{C}tmm --h{R} : {G}Show Help{R}
{C}tmm --uc{R} : {G}Check for Updates{R}

{G}NOTE : You can also Drag & Drop the .cer file on the Execuatble or Enter the Path!{R}          
""")


def warning(): # Ay DO NUT IMPORT RANDOM CERTIFICATES FROM THE INTERNET!
    print(Fore.RED + "⚠️ WARNING! ⚠️\n\n" + Fore.YELLOW + "Importing Random Certificates is DANGEROUS!\nImport Certificates of only Open-Source Software downloaded from Trusted Sources or if Testing your own App!\n" + Fore.RESET)

def isAdmin(): # If no then Sorry :)
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def runAsAdmin(): # Just helping you if you forgot 'sudo tmm -i <path>' ! ( Btw that's a shortcut! ) 
    if "--elevated" in sys.argv:
        return True
    if not isAdmin():
        if getattr(sys, 'frozen', False):
            # Running as a compiled EXE
            target_exe = sys.executable
            args_list = sys.argv[1:]
        else:
            # Running as a Python script (.py)
            target_exe = sys.executable
            args_list = [sys.argv[0]] + sys.argv[1:]

        if "--elevated" not in args_list:
            args_list.append("--elevated")
        params = " ".join([f'"{arg}"' for arg in args_list])
        try:            
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", target_exe, params, None, 1
            )
            return False 
        except Exception as e:
            print(f"Elevation failed: {e}")
            return False
    return True   

def versionToTuple(v): # Coverts Version to a Tuple ( Wait I forgot what a Tuple is.... Oh an Immutable Array! Haha JAVA Brainrot! )
    parts = v.strip().split('.')
    return tuple(int(p) for p in parts if p.isdigit())

def importCert(certificatePath, storeLocation, storeName): # The Magic of this Tool ( Ay stop calling everything as an App this is Windows not MacOS! )
    if storeLocation.lower() == 'localmachine' and not isAdmin():
        print(Fore.RED + "Error : Administrator privileges required." + Fore.RESET)
        return
    try:
        subprocess.run(
            ['certutil', '-addstore', storeName, certificatePath],
            check=True,
            capture_output=True,
            text=True
        )
        print(Fore.GREEN + "Import Succeeded! ✅" + Fore.RESET)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error: {e.stderr}" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Fore.RESET)

def checkForUpdates(): # I hope you are connected to the internet for this!
    print(Fore.GREEN + f"\nv{ver}" + Fore.RESET + " | Status - ", end="")
    try:
        response = requests.get(verUrl, timeout=5)
        response.raise_for_status()
        latestVersionStr = response.text.strip()        
        latest_tup = versionToTuple(latestVersionStr)
        current_tup = versionToTuple(ver)
        if latest_tup > current_tup:            
            print(Fore.GREEN + f"Update Available : {latestVersionStr} 🎉\n" + Fore.RESET)
        elif latest_tup == current_tup:
            print(Fore.GREEN + "Up to Date 🎉\n" + Fore.RESET)
        else:
            print(Fore.YELLOW + "DEV. Build ⚠️\n" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Check failed ❌ ({e})\n" + Fore.RESET)

class CustomParser(argparse.ArgumentParser): # Thou shalt see me on Binbows
    def print_help(self):
        logo()
        help()

    def error(self, message):
        logo()
        sys.stderr.write(Fore.RED + f'Error: {message}\n' + Fore.RESET)
        self.print_help()
        sys.exit(2)

if __name__ == "__main__":    

    if os.name != 'nt':
        logo()
        print(Fore.RED + "Trust My Msix! is 🪟 Windows ONLY!\nThis is not for 🐧 Linux or 🍎 MacOS!" + Fore.RESET)
        input("\nPress Enter to Exit...")
        sys.exit(1)

    parser = CustomParser(
        usage="%(prog)s --i <path_to_cert>",
        add_help=False
    )
    parser.add_argument('dropped_path', type=str, nargs='?', help=argparse.SUPPRESS) # For Drag & Drop support
    parser.add_argument('--i', type=str, metavar='<path>', help="Path to the .cer file")
    parser.add_argument('--v', action='store_true', help="Show version")
    parser.add_argument('--h', action='store_true', help="Show help")
    parser.add_argument('--uc', action='store_true', help="Check updates")
    parser.add_argument('--elevated', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--vande-mataram', action='store_true', help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.h:
        parser.print_help()
        sys.exit(0)

    if args.v:
        logo()
        print(Fore.GREEN + f"\nVersion: {ver}\n" + Fore.RESET)
        sys.exit(0)

    if args.uc:
        logo()
        checkForUpdates()
        sys.exit(0)

    if args.vande_mataram:
        logo()
        freedom()
        sys.exit(0)

    if not runAsAdmin():
        sys.exit(0)
    
    logo()
    checkForUpdates()
    warning()

    targetStoreLocation = "LocalMachine"
    targetStoreName = "Root"
    certFilePath = None

    # Handle file path from either --i flag or direct drag-and-drop
    initialPath = args.i or args.dropped_path

    if initialPath:
        pathValue = initialPath.strip().strip('"')
        if os.path.exists(pathValue) and pathValue.lower().endswith('.cer'):
            certFilePath = pathValue
        else:
            print(Fore.RED + f"\nError : Invalid Path - {pathValue} ❌\n" + Fore.RESET)

    if certFilePath is None:
        while True:
            inputPath = input(Fore.BLUE + "Enter Full Path or Drop your .cer file : " + Fore.RESET).strip().strip('"')
            if not inputPath:
                continue
            if os.path.exists(inputPath) and inputPath.lower().endswith('.cer'):
                certFilePath = inputPath
                break
            if inputPath.strip("").upper() == "VANDE MATARAM" or inputPath.strip("").upper() == "108":
                freedom()
                continue
            if inputPath.strip("").upper() == "EXIT":
                print(Fore.GREEN + "\nSee you Soon!\n" + Fore.RESET)
                sys.exit(0)
            else:
                print(Fore.RED + "\nError : Invalid File. ❌\n" + Fore.RESET)

    print(Fore.GREEN + f"\nImporting to Trusted Root Certification Authorities ♪(´▽｀)\n" + Fore.RESET)
    importCert(certFilePath, targetStoreLocation, targetStoreName)

    if not args.i : input("\nPress Enter to Exit... ")      

sys.exit(0)

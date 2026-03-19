import requests, subprocess, os, sys, ctypes, argparse

verUrl = "https://gist.githubusercontent.com/Chill-Astro/7e0d5246d48b0684ac303df756586c38/raw/TMM_V.txt" # Gist URL.

ver = "3.14.1.2" # New Name + Argument Update

# Msix is GREAT! Very much better than typing 'Yes' a 100 times. Only thing..... you need to buy a certificate to sign the app. Soooooo, I made this to Support Hobbyists and Students who JUST WANT TO INSTALL A FOSS PROJECT. ( Ah Lamina ✦ !)

def logo():
    print(r"""
 _____ ___  _   _  ___ _____   __  __  __   __  __  __  ___  ___ __  __  _ 
|_   _| _ \| | | |/ __|_   _| |  \/  | \ \ / / |  \/  |/ __||_ _|\ \/ / | |
  | | |   /| |_| |\__ \ | |   | |\/| |  \ V /  | |\/| |\__ \ | |  >  <  |_|
  |_| |_|_\ \___/ |___/ |_|   |_|  |_|   |_|   |_|  |_||___/|___|/_/\_\ (_)

(C) Chill-Astro | 2026
          """)

def warning(): # Ay DO NUT IMPORT RANDOM CERTIFICATES FROM THE INTERNET!
    print("⚠️ WARNING! ⚠️\n\nImporting Random Certificates is DANGEROUS!\nImport Certificates of only Open-Source Software downloaded from Trusted Sources or if Testing your own App!\n")

def isAdmin(): # If no then Sorry :)
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def runAsAdmin(): # Just helping you if you forgot 'sudo tmm -i <path>' ! ( Btw that's a shortcut! )
    if "--elevated" in sys.argv:
        return True
    if not isAdmin():
        try:
            scriptPath = os.path.abspath(sys.argv[0])
            params = " ".join(sys.argv[1:] + ["--elevated"])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{scriptPath}" {params}', None, 1
            )
            return False
        except:
            return False
    else:
        return True

def versionToTuple(v): # Coverts Version to a Tuple ( Wait I forgot what a Tuple is.... Oh an Immutable Array! Haha JAVA Brainrot! )
    parts = v.strip().split('.')
    return tuple(int(p) for p in parts if p.isdigit())

def importCert(certificatePath, storeLocation, storeName): # The Magic of this Tool ( Ay stop calling everything as an App this is Windows not MacOS! )
    if storeLocation.lower() == 'localmachine' and not isAdmin():
        print("Error : Administrator privileges required.")
        return

    try:
        subprocess.run(
            ['certutil', '-addstore', storeName, certificatePath],
            check=True,
            capture_output=True,
            text=True
        )
        print("Import Succeeded! ✅\n")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
    except Exception as e:
        print(f"Error: {e}")

def checkForUpdates(): # I hope you are connected to the internet for this!
    print("Status - ", end="")
    try:
        response = requests.get(verUrl, timeout=5)
        response.raise_for_status()
        latestVersionStr = response.text.strip()

        if versionToTuple(latestVersionStr) > versionToTuple(ver):
            print(f"Update Available : {latestVersionStr} 🎉\n")
        elif latestVersionStr == ver:
            print("Up to Date 🎉\n")
        else:
            print("DEV. Build ⚠️\n")
    except Exception as e:
        print(f"Check failed ❌ ({e})\n")

class CustomParser(argparse.ArgumentParser): # Thou shalt see me on Binbows
    def print_help(self):
        logo()
        super().print_help()

    def error(self, message):
        logo()
        sys.stderr.write(f'Error: {message}\n')
        self.print_help()
        sys.exit(2)

if __name__ == "__main__":
    parser = CustomParser(
        usage="%(prog)s --i <path_to_cert>",
        add_help=False
    )
    parser.add_argument('--i', type=str, metavar='<path>', help="Path to the .cer file")
    parser.add_argument('--v', action='store_true', help="Show version")
    parser.add_argument('--h', action='store_true', help="Show help")
    parser.add_argument('--uc', action='store_true', help="Check updates")
    parser.add_argument('--elevated', action='store_true', help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.h:
        parser.print_help()
        sys.exit(0)

    if args.v:
        logo()
        print(f"Version: {ver}")
        sys.exit(0)

    if args.uc:
        logo()
        checkForUpdates()
        sys.exit(0)

    if not runAsAdmin():
        sys.exit(0)

    logo()
    checkForUpdates()
    warning()

    targetStoreLocation = "LocalMachine"
    targetStoreName = "Root"
    certFilePath = None

    if args.i:
        pathValue = args.i.strip().strip('"')
        if os.path.exists(pathValue) and pathValue.lower().endswith('.cer'):
            certFilePath = pathValue
        else:
            print(f"Error : Invalid Path - {pathValue} ❌\n")

    if certFilePath is None:
        while True:
            inputPath = input("Enter Full Path of your .cer file : ").strip().strip('"')
            if not inputPath:
                continue
            if os.path.exists(inputPath) and inputPath.lower().endswith('.cer'):
                certFilePath = inputPath
                break
            else:
                print("Error : Invalid File. ❌\n")

    print(f"\nImporting to Trusted Root Certification Authorities ♪(´▽｀)\n")
    importCert(certFilePath, targetStoreLocation, targetStoreName)

    input("Press Enter to Exit...")
    sys.exit(0)
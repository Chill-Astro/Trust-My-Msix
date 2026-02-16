import requests
import subprocess
import os
import sys
import ctypes
import argparse

UPDATE_VERSION_URL = "https://gist.githubusercontent.com/Chill-Astro/7e0d5246d48b0684ac303df756586c38/raw/MCIT_V.txt"
CURRENT_VERSION = "3.14.1.2"

def logo():
    print(r"""
 _____ ___  _   _ ___ _____   __  __  __    __ __  __  ___  ___ __  __  _ 
|_   _| _ \| | | / __|_   _| |  \/  | \ \ / / |  \/  |/ __||_ _|\ \/ / | |
  | | |   /| |_| \__ \ | |   | |\/| |  \ V /  | |\/| |\__ \ | |  >  <  |_|
  |_| |_|_\ \___/|___/ |_|   |_|  |_|   |_|   |_|  |_||___/|___//_/\_\ (_)

(C) Chill-Astro | 2026
          """)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        try:
            script = os.path.abspath(sys.argv[0])
            params = " ".join([f'"{arg}"' if ' ' in arg else arg for arg in sys.argv[1:]])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
            return True
        except:
            return False
    else:
        return True

def import_cert_logic(certificate_path, store_location, store_name):
    if store_location.lower() == 'localmachine' and not is_admin():
        print("Error: Administrator privileges required.")
        return 

    try:
        powershell_command = f"Import-Certificate -FilePath \"{certificate_path}\" -CertStoreLocation Cert:\\{store_location}\\{store_name}"
        subprocess.run(['powershell', '-Command', powershell_command], check=True, capture_output=True, text=True)
        print("\nImport Succeeded!\n") 
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
    except Exception as e:         
        print(f"Error: {e}")

def check_for_updates():    
    print("Status - ", end="")
    try:        
        response = requests.get(UPDATE_VERSION_URL, timeout=5)
        response.raise_for_status()
        latest_version_str = response.text.strip()

        def version_tuple(v):
            return tuple(map(int, v.split('.')))

        if version_tuple(latest_version_str) > version_tuple(CURRENT_VERSION):                        
            print(f"Update Available : {latest_version_str}")                                                               
        elif latest_version_str == CURRENT_VERSION:            
            print("Up to Date.\n")
        else:
            print("DEV. Build\n")
    except:        
        print("Check failed.\n")

class CustomParser(argparse.ArgumentParser):
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
        description="TMM Certificate Importer",
        usage="%(prog)s --path <path_to_cert>",
        add_help=False
    )
    
    parser.add_argument('--path', type=str, metavar='<path>', help="REQUIRED: Path to the .cer file")
    parser.add_argument('--version', action='store_true', help="Show program's version number and exit")
    parser.add_argument('--help', action='store_true', help="Show this help message and exit")
    
    args, unknown = parser.parse_known_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    if args.version:
        logo()
        print(f"Version: {CURRENT_VERSION}")
        sys.exit(0)

    if not is_admin():
        if run_as_admin():
            sys.exit(0)
        else:
            logo()
            print("Admin rights required.")
            input("Press Enter to exit...")
            sys.exit(1)

    logo()
    check_for_updates()

    target_store_location = "LocalMachine"
    target_store_name = "Root"
    cert_file_path = None

    if args.path:
        p = args.path.strip().strip('"')
        if os.path.exists(p) and p.lower().endswith('.cer'):
            cert_file_path = p
        else:
            print(f"Invalid path: {p}")

    if cert_file_path is None:
        while True:
            p_in = input("Enter Full Path of the .cer file: ").strip().strip('"')
            if not p_in:
                continue
            if os.path.exists(p_in) and p_in.lower().endswith('.cer'):
                cert_file_path = p_in
                break
            else:
                print("Invalid file. Ensure path is correct and ends in .cer.\n")

    print(f"\nImporting to Trusted Root Certification Authourities...")
    import_cert_logic(cert_file_path, target_store_location, target_store_name)

    input("Press Enter to exit...")
    sys.exit(0)
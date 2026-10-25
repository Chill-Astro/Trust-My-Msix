import requests
import subprocess
import os
import sys
import ctypes
import argparse
import re
import hashlib

from pathlib import Path
from urllib.parse import urlparse, unquote
from colorama import init, Fore, Style


repoUrl = "https://chill-astro.github.io/assets/data/repo-data.json"
repoKey = "trustMyMsix"

ver = "3.14.1.7"  # UPDATE CHECKER OVERHAUL

init(convert=True)

# Msix is GREAT! Very much better than typing 'Yes' a 100 times. Only thing..... you need to buy a certificate to sign the app. Soooooo, I made this to Support Hobbyists and Students who JUST WANT TO INSTALL A FOSS PROJECT. ( Ah Lamina ✦ !)


def logo():
    print(Style.BRIGHT + Fore.CYAN + r"""
 _____ ___  _   _  ___ _____   __  __ __   __  __  __  ___  ___ __  __  _
|_   _| _ \| | | |/ __|_   _| |  \/  |\ \ / / |  \/  |/ __||_ _|\ \/ / | |
  | | |   /| |_| |\__ \ | |   | |\/| | \ V /  | |\/| |\__ \ | |  >  <  |_|
  |_| |_|_\ \___/ |___/ |_|   |_|  |_|  |_|   |_|  |_||___/|___|/_/\_\ (_)

(C) Chill-Astro | 2026""" + Style.RESET_ALL)


def freedom():  # For the Freedom Fighters who Liberated Mother India!
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


def warning():  # Ay DO NUT IMPORT RANDOM CERTIFICATES FROM THE INTERNET!
    print(
        Style.BRIGHT + Fore.YELLOW +
        "⚠️ WARNING! ⚠️\n\n" +
        "Importing Random Certificates is DANGEROUS! Use at your OWN RISK!\n" +
        Style.RESET_ALL
    )


def isAdmin():  # If no then Sorry :)
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def runAsAdmin():  # Just helping you if you forgot 'sudo tmm -i <path>' ! ( Btw that's a shortcut! )
    if isAdmin():
        return True

    if "--elevated" in sys.argv:
        print(Fore.RED + "Administrator privileges were not granted.")
        return False

    if getattr(sys, "frozen", False):
        # Running as a compiled EXE
        target_exe = sys.executable
        args_list = sys.argv[1:]
    else:
        # Running as a Python script (.py)
        target_exe = sys.executable
        args_list = [os.path.abspath(sys.argv[0])] + sys.argv[1:]

    args_list.append("--elevated")
    params = subprocess.list2cmdline(args_list)

    try:
        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            target_exe,
            params,
            None,
            1
        )

        if result <= 32:
            print(
                Style.BRIGHT + Fore.RED +
                "Elevation failed or was cancelled." +
                Style.RESET_ALL
            )

        # Original process exits after handing over to elevated process.
        return False

    except Exception as e:
        print(
            Style.BRIGHT + Fore.RED +
            f"Elevation failed: {e}" +
            Style.RESET_ALL
        )
        return False


def versionToTuple(v):  # Coverts Version to a Tuple ( Wait I forgot what a Tuple is.... Oh an Immutable Array! Haha JAVA Brainrot! )
    cleaned = str(v).strip().lstrip("vV")

    if not re.fullmatch(r"\d+(?:\.\d+)*", cleaned):
        raise ValueError("Invalid release version")

    return tuple(int(part) for part in cleaned.split("."))


def askYesNo(message):  # Democracy! The User gets to Decide!
    while True:
        answer = input(
            Fore.CYAN + f"{message} [Y/N]: " + Style.RESET_ALL
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print(Fore.YELLOW + "Please enter Yes or No.")


def getDownloadsFolder():  # Windows, please tell me where you hid the Downloads Folder.
    from ctypes import wintypes
    from uuid import UUID

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", ctypes.c_ubyte * 8)
        ]

    raw = UUID("374DE290-123F-4565-9164-39C4925E467B")
    guid = GUID.from_buffer_copy(raw.bytes_le)

    path_ptr = ctypes.c_wchar_p()
    shell32 = ctypes.windll.shell32

    shell32.SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID),
        wintypes.DWORD,
        wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_wchar_p)
    ]

    shell32.SHGetKnownFolderPath.restype = ctypes.c_long

    result = shell32.SHGetKnownFolderPath(
        ctypes.byref(guid),
        0,
        None,
        ctypes.byref(path_ptr)
    )

    if result != 0:
        raise OSError("Could not locate the Downloads folder")

    try:
        return Path(path_ptr.value)
    finally:
        ctypes.windll.ole32.CoTaskMemFree(
            ctypes.cast(path_ptr, ctypes.c_void_p)
        )


def getReleaseInfo():  # GitHub Pages is now our Update HQ!
    response = requests.get(repoUrl, timeout=10)
    response.raise_for_status()

    data = response.json()
    release = data[repoKey]

    if "tag" not in release or "downloads" not in release:
        raise ValueError("Incomplete release metadata")

    return release


def downloadFile(url, expected_hash=None):  # Green ASCII Progress Bar! Because CLI Apps deserve Style too!
    downloads = getDownloadsFolder()
    downloads.mkdir(parents=True, exist_ok=True)

    filename = Path(unquote(urlparse(url).path)).name

    if not filename or filename in (".", ".."):
        raise ValueError("Invalid download filename")

    destination = downloads / filename
    temporary = downloads / (filename + ".part")

    print(
        Fore.GREEN + Style.BRIGHT +
        f"\nDownloading: {filename}\n"
        f"Destination: {destination}\n" +
        Style.RESET_ALL
    )

    downloaded = 0
    hasher = hashlib.sha256()

    try:
        with requests.get(
            url,
            stream=True,
            timeout=(10, 30),
            allow_redirects=True
        ) as response:

            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))

            with open(temporary, "wb") as file:
                for chunk in response.iter_content(chunk_size=65536):
                    if not chunk:
                        continue

                    file.write(chunk)
                    hasher.update(chunk)
                    downloaded += len(chunk)

                    if total:
                        progress = min(downloaded / total, 1.0)
                        filled = int(progress * 30)
                        bar = "#" * filled + "-" * (30 - filled)

                        print(
                            Fore.GREEN + Style.BRIGHT +
                            f"\r[{bar}] "
                            f"{progress * 100:5.1f}% | "
                            f"{downloaded / 1048576:.1f}/"
                            f"{total / 1048576:.1f} MB" +
                            Style.RESET_ALL,
                            end="",
                            flush=True
                        )
                    else:
                        print(
                            Fore.GREEN + Style.BRIGHT +
                            f"\rDownloaded: "
                            f"{downloaded / 1048576:.1f} MB" +
                            Style.RESET_ALL,
                            end="",
                            flush=True
                        )

        if total and downloaded != total:
            raise IOError("Incomplete download")

        if expected_hash:
            actual = hasher.hexdigest()
            if actual.lower() != expected_hash.lower():
                raise ValueError("SHA-256 verification failed")

        temporary.replace(destination)

    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    print(
        Fore.GREEN + Style.BRIGHT +
        f"\n\nDownload completed successfully!\n"
        f"Saved to: {destination}\n" +
        Style.RESET_ALL
    )

    return destination


def launchDownloadedFile(path):  # Time to hand over the Stage to the New Version!
    path = Path(path)

    if not askYesNo("Launch the downloaded file now?"):
        print(Fore.YELLOW + "\nAlrighty then!")        
        return False

    suffix = path.suffix.lower()

    if suffix == ".exe":
        os.startfile(str(path))

    elif suffix == ".py":
        if getattr(sys, "frozen", False):
            print(
                Fore.YELLOW +
                "Open the downloaded .py file with Python."
            )
            return False

        subprocess.Popen(
            [sys.executable, str(path)],
            cwd=str(path.parent)
        )

    else:
        print(Fore.RED + "Unsupported file type.")
        return False

    return True


def updateDownloader(release):  # Portable or Setup? Your PC, Your Rules!
    print(
        Style.BRIGHT + Fore.CYAN +
        "\n========== UPDATE DOWNLOADER ==========\n" +
        Style.RESET_ALL
    )

    print(f"Latest version: {release['tag']}\n")
    print("[1] Portable Python (.py)")
    print("[2] Portable Executable (.exe)")
    print("[3] Setup Installer (.exe)")
    print("[4] Cancel\n")

    options = {
        "1": "python",
        "2": "executable",
        "3": "setup"
    }

    while True:
        choice = input(
            Fore.CYAN + "Select an option [1-4]: " +
            Style.RESET_ALL
        ).strip()

        if choice == "4":
            print(Fore.YELLOW + "Download cancelled.")
            return False

        if choice in options:
            break

        print(Fore.RED + "Invalid selection.")

    selected = options[choice]
    downloads = release["downloads"]
    url = downloads.get(selected)

    if not url:
        print(Fore.RED + "Selected download is unavailable.")
        return False

    parsed = urlparse(url)

    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or not parsed.path.startswith(
            "/Chill-Astro/Trust-My-Msix/releases/download/"
        )
    ):
        print(Fore.RED + "Unexpected download URL. Cancelled.")
        return False

    expected_extension = ".py" if selected == "python" else ".exe"

    if not parsed.path.lower().endswith(expected_extension):
        print(Fore.RED + "Unexpected download file type.")
        return False

    hashes = release.get("sha256", {})
    expected_hash = hashes.get(selected)

    if expected_hash and not re.fullmatch(
        r"[0-9a-fA-F]{64}", expected_hash
    ):
        print(Fore.RED + "Invalid SHA-256 metadata.")
        return False

    if not expected_hash:
        print(
            Fore.YELLOW +
            "Note: No SHA-256 checksum was provided for this release."
        )

    try:
        downloaded = downloadFile(url, expected_hash)

        if launchDownloadedFile(downloaded):
            sys.exit(0)

        return False

    except requests.RequestException as e:
        print(Fore.RED + f"\nDownload failed: {e}")

    except (OSError, ValueError) as e:
        print(Fore.RED + f"\nError: {e}")

    return False


def checkForUpdates():  # I hope you are connected to the internet for this!
    print(
        Style.BRIGHT + Fore.CYAN +
        f"\nv{ver}" + Fore.RESET +
        " | Status - ",
        end="",
        flush=True
    )

    try:
        release = getReleaseInfo()

        latest = str(release["tag"]).lstrip("vV")
        latest_tup = versionToTuple(latest)
        current_tup = versionToTuple(ver)

        if latest_tup > current_tup:
            print(
                Style.BRIGHT + Fore.GREEN +
                f"Update Available: v{latest} 🎉\n" +
                Style.RESET_ALL
            )

            if askYesNo("Would you like to download the update?"):
                updateDownloader(release)

            print()

        elif latest_tup == current_tup:
            print(
                Style.BRIGHT + Fore.GREEN +
                "Up to Date 🎉\n" +
                Style.RESET_ALL
            )

        else:
            print(
                Style.BRIGHT + Fore.YELLOW +
                "DEV. Build ⚠️\n" +
                Style.RESET_ALL
            )

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError
    ):
        print(
            Style.BRIGHT + Fore.RED +
            "Check failed ❌\n" +
            Style.RESET_ALL
        )


def importCert(certificatePath, storeLocation, storeName):  # The Magic of this Tool ( Ay stop calling everything as an App this is Windows not MacOS! )
    if storeLocation.lower() == "localmachine" and not isAdmin():
        print(
            Style.BRIGHT + Fore.RED +
            "Error : Administrator privileges required." +
            Style.RESET_ALL
        )
        return

    try:
        subprocess.run(
            ["certutil", "-addstore", storeName, certificatePath],
            check=True,
            capture_output=True,
            text=True
        )

        print(
            Style.BRIGHT + Fore.GREEN +
            "Import Succeeded! ✅" +
            Style.RESET_ALL
        )

    except subprocess.CalledProcessError as e:
        print(
            Style.BRIGHT + Fore.RED +
            f"Error: {e.stderr}" +
            Style.RESET_ALL
        )

    except Exception as e:
        print(
            Style.BRIGHT + Fore.RED +
            f"Error: {e}" +
            Style.RESET_ALL
        )


class CustomParser(argparse.ArgumentParser):  # Thou shalt see me on Binbows
    def print_help(self):
        logo()
        help()

    def error(self, message):
        logo()
        sys.stderr.write(
            Style.BRIGHT + Fore.RED +
            f"Error: {message}\n" +
            Style.RESET_ALL
        )
        self.print_help()
        sys.exit(2)


def main():
    if os.name != "nt":
        logo()
        print(
            Style.BRIGHT + Fore.RED +
            "Trust My Msix! is 🪟 Windows ONLY!\n"
            "This is not for 🐧 Linux or 🍎 MacOS!" +
            Style.RESET_ALL
        )
        input("\nPress Enter to Exit. ")
        return 1

    parser = CustomParser(
        usage="%(prog)s --i <path_to_cert>",
        add_help=False
    )

    parser.add_argument(
        "dropped_path",
        type=str,
        nargs="?",
        help=argparse.SUPPRESS
    )  # For Drag & Drop support

    parser.add_argument(
        "--i",
        type=str,
        metavar="<path>",
        help="Path to the .cer file"
    )

    parser.add_argument("--v", action="store_true", help="Show version")
    parser.add_argument("--h", action="store_true", help="Show help")
    parser.add_argument("--uc", action="store_true", help="Check updates")

    parser.add_argument(
        "--elevated",
        action="store_true",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--vande-mataram",
        action="store_true",
        help=argparse.SUPPRESS
    )

    args = parser.parse_args()

    # These three commands NEVER require Administrator privileges.
    if args.h:
        parser.print_help()
        return 0

    if args.v:
        logo()
        print(
            Style.BRIGHT + Fore.GREEN +
            f"\nVersion: {ver}\n" +
            Style.RESET_ALL
        )
        return 0

    if args.uc:
        logo()
        checkForUpdates()
        return 0

    # Administrator First! Except for --v, --h and --uc.
    # No logo, update check, or certificate prompt before UAC.
    if not isAdmin():
        runAsAdmin()
        return 0

    if args.vande_mataram:
        logo()
        freedom()
        return 0

    # --i SHALL NOT TRIGGER THE UPDATE CHECKER!
    # Drag & Drop skips it too. No internet needed to import a certificate!
    skipUpdateCheck = bool(args.i or args.dropped_path)

    logo()

    # IMPORTANT: Do NOT check args.elevated here.
    # Normal launches must still check updates after UAC elevation.
    if not skipUpdateCheck:
        checkForUpdates()

    warning()

    targetStoreLocation = "LocalMachine"
    targetStoreName = "Root"
    certFilePath = None

    # Handle file path from either --i flag or direct drag-and-drop
    initialPath = args.i or args.dropped_path

    if initialPath:
        pathValue = initialPath.strip().strip('"')

        if (
            os.path.isfile(pathValue)
            and pathValue.lower().endswith(".cer")
        ):
            certFilePath = pathValue

        else:
            print(
                Style.BRIGHT + Fore.RED +
                f"\nError : Invalid Path - {pathValue} ❌\n" +
                Style.RESET_ALL
            )

    if certFilePath is None:
        while True:
            inputPath = input(
                "Enter Full Path : "
            ).strip().strip('"')

            if not inputPath:
                continue

            if (
                os.path.isfile(inputPath)
                and inputPath.lower().endswith(".cer")
            ):
                certFilePath = inputPath
                break

            if inputPath.upper() in ("VANDE MATARAM", "108"):
                freedom()
                continue

            if inputPath.upper() == "EXIT":
                print(
                    Fore.GREEN +
                    "\nSee you Soon!\n" +
                    Style.RESET_ALL
                )
                return 0

            print(
                Style.BRIGHT + Fore.RED +
                "\nError : Invalid File. ❌\n" +
                Style.RESET_ALL
            )

    print(
        Style.BRIGHT + Fore.GREEN +
        "\nImporting to Trusted Root Certification Authorities ♪(´▽｀)\n" +
        Style.RESET_ALL
    )

    importCert(
        certFilePath,
        targetStoreLocation,
        targetStoreName
    )

    if not args.i:
        input("\nPress Enter to Exit. ")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

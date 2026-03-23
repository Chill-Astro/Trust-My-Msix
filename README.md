<p align="center">
  <img src="https://github.com/Chill-Astro/MsixCertImportTool/blob/main/TMM.ico" width="128px" height="128px" alt="TMM Logo">
</p>
<h1 align="center">Trust My Msix!</h1>

<div align="center">
  
`Trust My Msix!` is a Simple Command-Line App designed to import `.cer` files to the `Trusted Root Certification Authourities Store` in Windows in a few keystrokes! This speeds up the process of certificate importing for `Self-Signed Msix Packages on Windows` and it is very helpful to non tech-savvy users. 

The `.msix` format is AWESOME and leaves far less traces and doesn't need pressing 'Yes' a 100 times. But an `.msix` is allowed to be installed if the `Certificate` is signed by a `Certificate Authourity`, and getting a Certificate from a CA costs Money 💵.

Normally Users have to go through the Import process of a Self-Signed Certificate which is TEDIOUS and CONFUSING, especially for Newbies. `This tool makes this process take 1 second`!
  
**Target OS :** **Windows** ONLY.  |  **Latest Stable Version :** `v3.14.1.2`

**Execution Alias :** `tmm.exe`

</div>

## ⚠️ WARNING! :

This is the original version of Trust My Msix! Don't trust Counterfeit Versions. Importing Random Certificates is DANGEROUS. Import Certificates of only Open-Source Software downloaded from Trusted Sources or if Testing your own App.

---

## Key Features :

- Extemely Lightweight ( It's Terminal-based ). ✅
- Update Checking Support. ✅
- Extremely Quick and Reliable. ✅
- Zero Instructions Needed for Novice Users. ✅
- Supports Arguments for Easy Importing. ✅

---

## Installing Trust My Msix! from Winget :

    winget install Chill-Astro.TMM    

---

## How it Works? 

Transparency is the key Trust and you can't Trust `Trust My Msix!` if it wasn't Transparent!

- This app uses `certutil` on Windows to import `.cer` files.
- This tool uses the following command :
  
      certutil -addstore Root <path>

- Of course making it easier for Newbies is better :

      tmm -i <path>

- This command just saves developer hassle and encourages more hobbyists to make FOSS Apps.

---    

## Building :

STEP 1 : Install Python 

    winget install python

STEP 2 : Clone this Repository :

    git clone https://github.com/Chill-Astro/Trust-My-Msix.git
    cd Trust-My-Msix

STEP 3 : Install Dependencies 

    pip install -r Reqs.txt

STEP 4 : Build

    pyinstaller -F -i TMM.ico TMM.py

STEP 5 : Run

    tmm --i <path> 
    # Use pyhton tmm.py - i <path> if not Building

---

## Usage :

- Trust My Msix! can be easily used by just running the Portable `.exe`
- Trust My Msix!'s entire CLI can be bypassed by using the argument '--i' :
      
      tmm --i <path>
      # python tmm.py --i <path> if using Python File.
  
- Help, Version and Update Check can be accessed as follows :
      
      tmm --h
      # python tmm.py --h if using Python File.
      tmm --v
      # python tmm.py --v if using Python File.
      tmm --uc
      # python tmm.py --uc if using Python File.

---

## Preview :

<kbd>
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9404a45d-7de3-4653-83ec-c96d40168fff" />
</kbd>

---

## Wallpaper Credit :

- [@Lisa on Pexels for Pink Flowers Photograph](https://www.pexels.com/photo/pink-flowers-photograph-1083822/)

---

## ⚠️ IMPORTANT NOTICE ⚠️

Please be aware: There are fraudulent repositories on GitHub that are cloning this project's name and using AI-generated readmes, but they contain **completely random and unrelated files in each release**. These are NOT official versions of this project.

**ALWAYS ensure you are downloading or cloning this project ONLY from its official and legitimate source:**
`https://github.com/Chill-Astro/Trust-My-Msix`

I am trying my best to report these people.

---

## HALL OF FAME 👍 : 

// Will add Forked Repos which are genuinely good. 🤩 I will list everything Good about them.

---

## HALL OF NEUTRALITY 😐 :

// Will add Inactive Forks. Uh yeah that's it atleast it's Forking not Cloning! 😅

---

## HALL OF SHAME 👎 :

// Includes Clones who are working against the MIT Licence and Distributing Malware. All Flaws are mentioned. 😑

- Trust My Msix! previously MsixCertImportTool has undergone Malware Attacks.

---


## ⚠️ Smoking Gun for Danger :

> [!CAUTION]
> **MALWARE ALERT:** If your downloaded folder looks like the images below, **DO NOT OPEN** any files. Format the drive or delete the folder immediately. Official releases are ONLY `.msix` files or an Inno Setup `.exe`.

<details>
<summary><b>View Details</b></summary>
  
* **Suspicious Windows Executables:** Files ending in `.exe`, `.bat`, or `.dll` (e.g., `luau.exe`, `StartApp.bat`).
* **Compressed Archives:** This project is distributed as an **MSIX**, never as a `.zip` or `.7z` containing Windows binaries.
* **Hidden Scripts:** Text files like `asm.txt` used to execute malicious code on your PC.
* The Following Folder Structure is used by Malware (Shown in a VM) :

![Screenshot_2026-03-01-18-52-39-337_com clone android dual space](https://github.com/user-attachments/assets/be691c9f-7def-4e8b-982c-c7ca2e9a067d)

![Screenshot_2026-03-01-18-53-09-759_com clone android dual space](https://github.com/user-attachments/assets/1c75031d-95be-4716-9347-b762e3dad5b8)

</details>

---

## Note from Developer :

Appreciate my effort? Why not leave a Star ⭐ ! Also if forked, please credit me for my effort and thanks if you do! :)

---


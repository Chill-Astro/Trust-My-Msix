<p align="center">
  <img src="https://github.com/Chill-Astro/MsixCertImportTool/blob/main/tmm.ico" width="200px" alt="TMM Logo">
</p>
<h1 align="center">Trust My Msix!</h1>

<div align="center">
  
`Trust My Msix!` is a **Simple CLI App** to **Import** `.cer` files to the `Trusted Root Certification Authorities Store` in Windows in a few keystrokes! 

This *SPEEDS UP* the Process of Certificate Importing for `Self-Signed Msix Packages` that Refuse to Pay Money 💵 to a *Certificate Authority*! 
  
**Target OS :** **Windows** ONLY.  |  **Latest Stable Version :** `v3.14.1.7`

**Execution Alias :** `tmm.exe`

**Codename** : `TMM`

</div>

---

## Key Features :

- **Extremely Lightweight** & **CLI-Based**! ✅
- **Built-In Self-Updater ( With Consent )** !✅
- **Zero Instructions Needed** for NOOBS! ✅
- **Supports Arguments** for ADVANCED People. ✅
- **Supports Drag & Drop** for `cer` Files! ✅

---

## Usage :

- Trust My Msix! can be easily used by just running the Portable `.exe`
- Trust My Msix!'s entire CLI can be bypassed by using the argument '--i' :
      
      tmm --i <path>
      # python tmm.py --i <path> if using Python File.
      # .\tmm --i <path> if using Powershell on Portable exe.
  
- Help, Version and Update Check can be accessed as follows :
      
      tmm --h
      # python tmm.py --h if using Python File.
      # .\tmm --h if using Powershell on Portable exe.
      tmm --v
      # python tmm.py --v if using Python File.
      # .\tmm --v if using Powershell on Portable exe.
      tmm --uc
      # python tmm.py --uc if using Python File.
      # .\tmm --uc if using Powershell on Portable exe.
---

## Preview :

<kbd>
  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7ab6920b-1bf7-4914-a529-b03450a262d9" />
</kbd>

---

## Version Structure :

<div align="center">

<H2>

v`3.14`.`1.7`

</H2>

</div>

- `3.14` -> Python Version ( NOT a Strict Requirement. *BUT I AM CUTTING EDGE!* )
- `1.7` -> App Version ( Incremented by `0.1` Every Release )

---

## Installing from Winget :

    winget install Chill-Astro.TMM    

---

## How she Works? 

Transparency is the key Trust and you can't Trust `Trust My Msix!` if she wasn't Transparent!

- She uses `certutil` on Windows to import `.cer` files.
- The following command is used :
  
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

    pip install -r reqs.txt

STEP 4 : Build

    pyinstaller -F -i tmm.ico tmm.py

STEP 5 : Run

    tmm --i <path> 
    # Use pyhton tmm.py - i <path> if not Building

---

## Note from Developer :

A Star ⭐ will be Appreciated to Support this Project! :)

---


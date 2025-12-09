# xiaomi.eu-roms-checker

A small tool for monitoring new **xiaomi.eu ROM releases** from SourceForge.  
Originally designed for Weekly ROMs, now updated to work with the new **Stable / HyperOS** structure.

---

## ✨ Features

### **1. SourceForge Folder Scanner**
Automatically crawls the xiaomi.eu SourceForge project and:
- discovers all device folders (with recursive folder parsing)
- detects newly added folders or versions
- returns the **newest** or **last modified** ROM folder  
- prints or sends the result

### **2. Thread & Changelog Fetching (deprecated for Weekly)**
Previously supported checking the newest thread from the *xiaomi.eu Weekly section*.  
This function remains available but Weekly ROMs are no longer released.

### **3. Telegram Notifications**
Send results directly to:
- your **Telegram account**, or
- your **Telegram channel**

Fully optional—if not configured, results print to console.

---

## 🆕 New Functionality
The tool now includes:
- **Recursive scraping** of SourceForge folders  
- **Extraction of device-specific ROM files**  
- Parsing and caching to minimize requests  
- Compatibility with the new **Stable / HyperOS** folder layout  
- Future support for table-based device lists (from image/JSON sources)

---

## 📁 Files

- `sourceforge_new_folder_checker.py`  
  Finds the newest available ROM folder (or last modified) from the xiaomi.eu SourceForge tree.

- `xiaomi_eu_new_thread_checker.py`  
  Checks the last stable thread from the xiaomi.eu forum and prepares telegram message with the title, downloads link and changelog.
  Now, because of the deprecation of weekly roms this function is no longer usable.

- `get_all_folders.py` *(new)*  
  Recursively scans all device folders and builds a full ROM index.

- `telegram_sender.py` *(optional)*  
  Send messages to Telegram (user or channel).

---

## 🖼 Screenshots

SourceForge check result:
![Image](rom_checker_from_sourceforge.png)

xiaomi.eu thread parsing (legacy Weekly mode):
![Image](rom_checker_from_xiaomi.eu.png)

---

## ▶️ Usage

Run folder checker:
```bash
python sourceforge_new_folder_checker.py

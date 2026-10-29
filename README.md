# dtech-win

This repository hosts a PowerShell wrapper that mimics the behaviour of:

```
irm https://christitus.com/win | iex
```

but points to our own script hosted at:

```
https://dattantruongdx-bdss.github.io/dtech-win/win
```

Running the command below will download the script and execute it, which in turn fetches the original **WinUtil** project from ChrisTitusTech, extracts it, and launches its GUI.

```powershell
irm https://dattantruongdx-bdss.github.io/dtech-win/win | iex
```

Feel free to fork, edit, or contribute.

---

## DTechCom Tool (Python GUI)

The repository also contains a full‑featured Python utility `dtechcom_tool.py` built with **CustomTkinter**. It provides system cleanup, disk conversion, performance tweaks, printer fixes, LAN share setup, and backup utilities.

### Run the tool

A convenient batch wrapper `run-dtechcom.bat` is provided. Double‑click it to:
1. Verify Python is in the PATH.
2. Upgrade `pip` and install required packages (`customtkinter`, `psutil`).
3. Launch the GUI.

```bat
run-dtechcom.bat
```

You can also run the script directly:

```powershell
python dtechcom_tool.py
```

---

## Usage summary

- **PowerShell wrapper**: `irm https://dattantruongdx-bdss.github.io/dtech-win/win | iex`
- **Python GUI**: `run-dtechcom.bat` (or `python dtechcom_tool.py`)

---

## Contributing

Feel free to open issues or pull requests to improve either the PowerShell wrapper or the Python tool.

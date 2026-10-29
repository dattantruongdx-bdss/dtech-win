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

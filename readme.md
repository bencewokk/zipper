# Zipper

_Advanced directory zipper with rich visual feedback._

## Overview

Zipper is a Python-based command-line tool that compresses a directory into a ZIP archive with a progress indication and statistics summary. It supports custom file exclusion, timestamped file names, and works on multiple platforms (via a batch script on Windows).

## Features

- Text-based progress bar during compression
- Spinning cursor animation while discovering files
- Displays compression statistics such as file count, original size, compressed size, ratio, and processing time
- Excludes common directories/files by default
- Allows custom exclusion via command-line arguments

## Usage

### Windows

Run the provided batch script (`zipper.bat`) to launch the utility:

```bat
[zipper.bat](http://_vscodecontentref_/0) --source "C:\Your\Directory" --output "C:\Output\Directory"
```

### Add Zipper to Your PATH

If you want to run Zipper from any CMD window without providing full paths, you can use the provided batch script:

1. Open a CMD window as a normal user.
2. Run the following command:
   ```bat
   c:\zipper\add_to_path.bat
   ```
3. Close and reopen CMD for the changes to apply.
4. Now you can run `zipper` from any directory.
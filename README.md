# pdref

Whether it's books, papers, articles, recipes, or website printouts, pdref is a tool intended to help you keep track of notes you've taken while reading PDFs.

pdref extracts comments, highlights, and images from PDFs, and it saves them in an organized plain-text format (based on Markdown). It runs on your own computer, and all of your data stays with you. And because it uses plain text, you can use whatever you like to search or display the notes and images.

# Usage

Using pdref is easy:

1. Select a parent directory containing all of the PDFs you want to index. (They can be nested in subfolders.) If you've used pdref before, you _can_ select your previous notes folder
1. Select an output directory for your notes. If you've used pdref before, you'll probably want to use your previous notes folder
1. Set the date according to your preferences. If running for the first time, set a long-ago date or clear the date field to screen all PDFs in the refs folder
1. Hit "Run", and you're done

## Behind the scenes

pdref looks through the main folder and all subfolders to identify PDF files. When a PDF is found, pdref will go through a series of checks:
1. The name of the PDF will be converted to a more compatible one
1. pdref will check if a folder with that same name already exists in the output folder. If not, it will be made automatically
1. pdref will check if a copy of the PDF exists in that folder. If not, it will be copied automatically
1. pdref will go through the _original_ PDF and do the following:
    1. Extract metadata from the PDF like title and authors
    1. Extract all of the images in the PDF and reference them in an `_index.md` file
    1. Extract annotations and highlights from the PDF and list them page-by-page in a timestamped file. The file will be saved under a `notes` subfolder
        - For highlights, pdref attempts to extract the highlighted words
1. Every time you run pdref again, it will repeat the process of extracting the annotations/highlights and saving them to the named folder

## What it doesn't do

1. Extract ink/handwriting
1. Optical character recognition (OCR)


## Tips

### General
- Have descriptive names for all of your PDFs. At least make sure they're unique. Files that share the same name can create complications for saving notes

### PDF Notes
- If you want to add a note in an editor that doesn't allow comments, just highlight a single word and include a comment on it
- If you want to copy over new annotations to the PDF in your notes, you can delete the PDF in the output folder (or move it somewhere else, like a subfolder)

### Images
- If you want to re-extract the images, you can delete `_index.md` in the output folder (or move it somewhere else, like a subfolder)
- Extra images are extracted. You can delete them and the references to them in `_index.md`
- Images are broken up. You can manually screenshot, save, and reference them in `_index.md`

# Installation

You can use `pdref` with or without Python on your computer. If you're familiar with Python, you can run `pdref` yourself from this source. Otherwise, you can install a pre-built executable file.

## Running from source
1. Fork/clone/download this repository
1. Create the environment from the `environment.yml` file
1. Run `gui.py` to get started

### Building with `pyinstaller`
_You may need to (re)install `pyinstaller` for this to work appropriately._

Change into `/pdref/` and execute the following:

```
pyinstaller gui.py --name="pdref" --windowed --icon=res/icon.ico --add-data="res/icon.ico;res"
```

## Running from a pre-built executable

1. Download the appropriate compressed archive for your OS
1. Extract the files and locate the executable file for `pdref`
    - This is a little bit messy. All of the dependency files have been intentionally included in this distribution. You can see exactly what this program requires
1. Run the executable file or create a shortcut and move it somewhere for easy access



# Notes

- This project was initially influenced by the project [`pdfannots`](https://github.com/0xabu/pdfannots) around November 2020. If you want to make notes just once, for a single PDF, that might be a better option.
- There's no clear-cut rule for size-based filtering images in a PDF, since resolution and image size may vary from one source to another. As a result, you might end up with watermarks or other images you don't want. You can simply delete those images from the notes folder, and everything else should work fine. Alternatively, if you find that some images _aren't_ included, you can always manually save them to the notes folder and reference them in _index.md or wherever else you'd like.
- When processing highlights, you might get more than what you asked for. This can be deleted in the output.
- This program uses an older version of PyMuPDF, and some methods may be outdated.

# Possible future features

- [x] Don't indicate "No annotations"
- [x] Process only references modified after specified date (GUI input)
- [x] ~~Keep track of dates and update notes only if source PDF has an altered timestamp more recent than the last run of pdref~~  
    Instead sets default date to one week earlier
- [x] Extract text box annotations
- [ ] Take images from within specified bounds (e.g. don't take images from outer 1" margins)
- [ ] Option to filter images by size (GUI input)
- [ ] Option to compare images to reference directory for exclusion
- [ ] Option to force image extraction (GUI checkbox)
- [ ] Option to print image debugging output (GUI checkbox)
- [ ] Save source and destination folder locations (GUI)
- [ ] Save notes author name (GUI input)
- [ ] Update PyMuPDF usage

# Issues
PyMuPDF 1296 (from an earlier version; running macOS Sierra 10.12.6)
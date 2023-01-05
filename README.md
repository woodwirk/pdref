# pdref

Whether it's books, papers, articles, recipes, or website printouts, pdref is a tool intended to help you keep track of notes you've taken while reading PDFs.

pdref extracts comments, highlights, and images from PDFs, and it saves them in an organized plain-text format (based on Markdown). It runs on your own computer, and all of your data stays with you. And because it uses plain text, you can use whatever you like to search or display the notes and images.

# Usage

Using pdref is just a few clicks:

1. Select a parent directory containing all of the PDFs you want to index. (They can be nested in subfolders.) If you've used pdref before, you _can_ select your previous notes folder
1. Select an output directory for your notes. If you've used pdref before, you'll probably want to use your previous notes folder
1. Set the date according to your preferences. If running for the first time, set a long-ago date or clear the date field to screen all PDFs in the refs folder
1. Hit "Run", and you're done

See more at [`usage.md](notes/usage.md)

# Installation

## Running from source
1. Fork/clone/download this repository
1. Change into the `pdref` folder and create the environment from the `environment.yml` file with
        ```
        conda env create -f environment.yml
        ```
1. Run `gui.py` to get started

## Building with `pyinstaller`
_You may need to (re)install `pyinstaller` for this to work appropriately._

Change into `/pdref/` and execute the following:

Windows
```
pyinstaller gui.py --name="pdref" --windowed --icon=res/icon.ico --add-data="res/icon.ico;res"
```

Mac  
Note: on Mac, you must have XCode command line installed (From terminal: `xcode-select --install`). This may take up 15 GB of space. macOS also requires a different type of icon format. This process has not been confirmed.


# Notes

- This project was initially influenced by the project [`pdfannots`](https://github.com/0xabu/pdfannots) around November 2020. If you want to make notes just once, for a single PDF, that might be a better option.
- There's no clear-cut rule for size-based filtering images in a PDF, since resolution and image size may vary from one source to another. As a result, you might end up with watermarks or other images you don't want. You can simply delete those images from the notes folder, and everything else should work fine. Alternatively, if you find that some images _aren't_ included, you can always manually save them to the notes folder and reference them in _index.md or wherever else you'd like.
- When processing highlights, you might get more than what you asked for. This can be deleted in the output.
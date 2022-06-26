# pdref

Whether it's books, papers, articles, recipes, or website printouts, pdref is a tool intended to help you keep track of notes you've taken while reading PDFs.

pdref extracts comments, highlights, and images from PDFs and saves them in an organized plain text format (based on Markdown). It runs on your own computer, and all of your data stays with you. And because it uses plain text, you can use whatever you like to search or display the notes and images.

# Usage

Using pdref is easy:

1. Select a parent directory containing all of the PDFs you want to index. (They can be nested in subfolders.)
1. Select an output directory for your notes. If you've used pdref before, you'll probably want to use the same folder
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

1. Extract text box comments/annotations
1. Extract ink/handwriting
1. OCR


## Tips

- Have descriptive names for all of your PDFs. At least make sure they're unique. Files that share the same name can create complications for saving notes
- If you want to add a note, just highlight a single word and include a comment on it (for now)
- If you want to copy over new annotations, you can delete the PDF in the output folder (or move it somewhere else, like a subfolder)
- If you want to re-extract the images, you can delete `_index.md` in the output folder (or move it somewhere else, like a subfolder)

# Installation

Right now, you can only run pdref from source. You can create a conda environment based on `environment.yml` and run `gui.py` to get started.

# Notes

- This project was initially influenced by the project [`pdfannots`](https://github.com/0xabu/pdfannots) around November 2020. If you want to make notes just once, for a single PDF, that might be a better option.
- There's no clear-cut rule for size-based filtering images in a PDF, since resolution and image size may vary from one source to another. As a result, you might end up with watermarks or other images you don't want. You can simply delete those images from the notes folder, and everything else should work fine. Alternatively, if you find that some images _aren't_ included, you can always manually save them to the notes folder and reference them in _index.md or wherever else you'd like.
- When processing highlights, you might get more than what you bargained for. This can be deleted in the output.

# Future features

- [] Extract text box annotations
- [] Keep track of dates and update notes only if source PDF has an altered timestamp more recent than the last run of pdref
- [] Option to filter images by size (GUI input)
- [] Option to force image extraction (GUI input)
- [] Save source and destination folder locations (GUI)
- [] Save notes author name (GUI input)
- [] Don't indicate "No annotations"
- [] Update PyMuPDF usage
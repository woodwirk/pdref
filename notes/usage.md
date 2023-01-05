# Usage

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
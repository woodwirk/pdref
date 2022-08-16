import os
import shutil
from datetime import datetime
import text_utils
from parse import process_pdf

def prepare_pdf(path_to_pdf, slugified_title, preferences):
    notes_path = preferences.notes_path
    image_size = preferences.image_size
    debug = preferences.debug

    print(path_to_pdf)
    path_to_notes = os.path.join(notes_path, slugified_title)
    if (not os.path.exists(path_to_notes)):
        os.mkdir(path_to_notes)

    path_to_pdf_copy = os.path.join(path_to_notes, f"{slugified_title}.pdf")
    if (not os.path.exists(path_to_pdf_copy)):
        shutil.copy(path_to_pdf, path_to_pdf_copy)
    
    process_pdf(path_to_pdf=path_to_pdf, path_to_pdf_copy = path_to_pdf_copy, path_to_notes = path_to_notes, image_size = image_size, debug = debug)

def crawl(preferences):
    # Both paths should exist before proceeding
    notes_path = preferences.notes_path
    pdfs_path = preferences.pdfs_path
    earliest_modified_date = preferences.earliest_modified_date

    if (not os.path.exists(notes_path)):
        os.mkdir(notes_path)

    if (not os.path.exists(pdfs_path)):
        print("The PDFs directory does not exist")
    else:
        try:
            earliest_modified_date = datetime.fromisoformat(earliest_modified_date)
        except:
            earliest_modified_date = None

        for dirpath, dirnames, filenames in os.walk(pdfs_path):
            for file in filenames:
                ext = os.path.splitext(file)
                if ext[-1] == '.pdf':
                    path_to_pdf = os.path.abspath(os.path.join(dirpath, file))
                    slugified_title = text_utils.slugify(ext[0])

                    if earliest_modified_date is not None:
                        if datetime.fromtimestamp(os.stat(path_to_pdf).st_mtime) > earliest_modified_date:
                            prepare_pdf(path_to_pdf, slugified_title, preferences)
                    else:
                        prepare_pdf(path_to_pdf, slugified_title, preferences)
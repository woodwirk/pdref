import os
import shutil
import text_utils
from parse import process_pdf

def crawl(pdfs_path, notes_path, image_size = None):
    # Both paths should exist before proceeding
    if (not os.path.exists(notes_path)):
        os.mkdir(notes_path)

    if (not os.path.exists(pdfs_path)):
        print("The PDFs directory does not exist")
    else:
        for dirpath, dirnames, filenames in os.walk(pdfs_path):
            for file in filenames:
                ext = os.path.splitext(file)
                if ext[-1] == '.pdf':
                    path_to_pdf = os.path.abspath(os.path.join(dirpath, file))
                    print(path_to_pdf)

                    slugified_title = text_utils.slugify(ext[0])

                    path_to_notes = os.path.join(notes_path, slugified_title)
                    if (not os.path.exists(path_to_notes)):
                        os.mkdir(path_to_notes)

                    path_to_pdf_copy = os.path.join(path_to_notes, f"{slugified_title}.pdf")
                    if (not os.path.exists(path_to_pdf_copy)):
                        shutil.copy(path_to_pdf, path_to_pdf_copy)
                    
                    process_pdf(path_to_pdf=path_to_pdf, path_to_pdf_copy = path_to_pdf_copy, path_to_notes = path_to_notes, image_size = image_size)
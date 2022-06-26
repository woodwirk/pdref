from operator import itemgetter
from itertools import groupby
import os
import re
from datetime import datetime
import fitz
from bisect import bisect_left, bisect_right
import text_utils


class SortedCollection(object):
    '''Sequence sorted by a key function.

    SortedCollection() is much easier to work with than using bisect() directly.
    It supports key functions like those use in sorted(), min(), and max().
    The result of the key function call is saved so that keys can be searched
    efficiently.

    Instead of returning an insertion-point which can be hard to interpret, the
    five find-methods return a specific item in the sequence. They can scan for
    exact matches, the last item less-than-or-equal to a key, or the first item
    greater-than-or-equal to a key.

    Once found, an item's ordinal position can be located with the index() method.
    New items can be added with the insert() and insert_right() methods.
    Old items can be deleted with the remove() method.

    The usual sequence methods are provided to support indexing, slicing,
    length lookup, clearing, copying, forward and reverse iteration, contains
    checking, item counts, item removal, and a nice looking repr.

    Finding and indexing are O(log n) operations while iteration and insertion
    are O(n).  The initial sort is O(n log n).

    The key function is stored in the 'key' attibute for easy introspection or
    so that you can assign a new key function (triggering an automatic re-sort).

    In short, the class was designed to handle all of the common use cases for
    bisect but with a simpler API and support for key functions.

    >>> from pprint import pprint
    >>> from operator import itemgetter

    >>> s = SortedCollection(key=itemgetter(2))
    >>> for record in [
    ...         ('roger', 'young', 30),
    ...         ('angela', 'jones', 28),
    ...         ('bill', 'smith', 22),
    ...         ('david', 'thomas', 32)]:
    ...     s.insert(record)

    >>> pprint(list(s))         # show records sorted by age
    [('bill', 'smith', 22),
     ('angela', 'jones', 28),
     ('roger', 'young', 30),
     ('david', 'thomas', 32)]

    >>> s.find_le(29)           # find oldest person aged 29 or younger
    ('angela', 'jones', 28)
    >>> s.find_lt(28)           # find oldest person under 28
    ('bill', 'smith', 22)
    >>> s.find_gt(28)           # find youngest person over 28
    ('roger', 'young', 30)

    >>> r = s.find_ge(32)       # find youngest person aged 32 or older
    >>> s.index(r)              # get the index of their record
    3
    >>> s[3]                    # fetch the record at that index
    ('david', 'thomas', 32)

    >>> s.key = itemgetter(0)   # now sort by first name
    >>> pprint(list(s))
    [('angela', 'jones', 28),
     ('bill', 'smith', 22),
     ('david', 'thomas', 32),
     ('roger', 'young', 30)]

    '''

    def __init__(self, iterable=(), key=None):
        self._given_key = key
        key = (lambda x: x) if key is None else key
        decorated = sorted((key(item), item) for item in iterable)
        self._keys = [k for k, item in decorated]
        self._items = [item for k, item in decorated]
        self._key = key

    def _getkey(self):
        return self._key

    def _setkey(self, key):
        if key is not self._key:
            self.__init__(self._items, key=key)

    def _delkey(self):
        self._setkey(None)

    key = property(_getkey, _setkey, _delkey, 'key function')

    def clear(self):
        self.__init__([], self._key)

    def copy(self):
        return self.__class__(self, self._key)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __repr__(self):
        return '%s(%r, key=%s)' % (
            self.__class__.__name__,
            self._items,
            getattr(self._given_key, '__name__', repr(self._given_key))
        )

    def __reduce__(self):
        return self.__class__, (self._items, self._given_key)

    def __contains__(self, item):
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return item in self._items[i:j]

    def index(self, item):
        'Find the position of an item.  Raise ValueError if not found.'
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return self._items[i:j].index(item) + i

    def count(self, item):
        'Return number of occurrences of item'
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return self._items[i:j].count(item)

    def insert(self, item):
        'Insert a new item.  If equal keys are found, add to the left'
        k = self._key(item)
        i = bisect_left(self._keys, k)
        self._keys.insert(i, k)
        self._items.insert(i, item)

    def insert_right(self, item):
        'Insert a new item.  If equal keys are found, add to the right'
        k = self._key(item)
        i = bisect_right(self._keys, k)
        self._keys.insert(i, k)
        self._items.insert(i, item)

    def remove(self, item):
        'Remove first occurence of item.  Raise ValueError if not found'
        i = self.index(item)
        del self._keys[i]
        del self._items[i]

    def find(self, k):
        'Return first item with a key == k.  Raise ValueError if not found.'
        i = bisect_left(self._keys, k)
        if i != len(self) and self._keys[i] == k:
            return self._items[i]
        raise ValueError('No item found with key equal to: %r' % (k,))

    def find_le(self, k):
        'Return last item with a key <= k.  Raise ValueError if not found.'
        i = bisect_right(self._keys, k)
        if i:
            return self._items[i-1]
        raise ValueError('No item found with key at or below: %r' % (k,))

    def find_lt(self, k):
        'Return last item with a key < k.  Raise ValueError if not found.'
        i = bisect_left(self._keys, k)
        if i:
            return self._items[i-1]
        raise ValueError('No item found with key below: %r' % (k,))

    def find_ge(self, k):
        'Return first item with a key >= equal to k.  Raise ValueError if not found'
        i = bisect_left(self._keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError('No item found with key at or above: %r' % (k,))

    def find_gt(self, k):
        'Return first item with a key > k.  Raise ValueError if not found'
        i = bisect_right(self._keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError('No item found with key above: %r' % (k,))

def make_text(words):
    """Return textstring output of getText("words").
    Word items are sorted for reading sequence left to right,
    top to bottom.
    """
    line_dict = {}  # key: vertical coordinate, value: list of words
    words.sort(key=lambda w: w[0])  # sort by horizontal coordinate
    for w in words:  # fill the line dictionary
        y1 = round(w[3], 1)  # bottom of a word: don't be too picky!
        word = w[4]  # the text of the word
        line = line_dict.get(y1, [])  # read current line content
        line.append(word)  # append new word
        line_dict[y1] = line  # write back to dict
    lines = list(line_dict.items())
    lines.sort()  # sort vertically
    return " ".join([" ".join(line[1]) for line in lines])


def process_pdf(path_to_pdf, path_to_pdf_copy, path_to_notes, image_size = None):
    doc = fitz.open(path_to_pdf)
    # if not image_size:
    #     image_size = 500*500

    # Check whether this ref has been processed previously
    time = datetime.now().strftime("%Y%m%d-%H%M%S")
    notes_name_formatted = f"_index.md"
    branch_index_path = os.path.join(path_to_notes, notes_name_formatted)

    if not os.path.exists(branch_index_path):
        metadata_title = doc.metadata['title'][0:20]

        file = os.path.basename(path_to_pdf_copy)
        ext = os.path.splitext(file)
        pdf_slug = text_utils.slugify(ext[0])

        if not metadata_title:
            notes_name_title = pdf_slug
        else:
            notes_name_title = text_utils.slugify(metadata_title)

        with open(branch_index_path, "w", encoding='utf-8') as f:
            title = doc.metadata['title']
            notes_frontmatter = text_utils.make_frontmatter(
                title = title if title else notes_name_title,
                author=doc.metadata['author'],
                keys=doc.metadata['keywords'].split(','),
                top_level = "true"
            )
            f.writelines(notes_frontmatter)
            f.writelines(f"\n\n[PDF]({os.path.basename(path_to_pdf_copy)})\n")

            pages = [ doc[ i ] for i in range( doc.pageCount ) ]

            for index, page in enumerate(pages, start=1):

                # Indicate page number
                f.write("\n## Page {}\n".format(index))

                # Save and reference images
                for img in doc.getPageImageList(index-1):
                    try:
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        f.writelines(text_utils.debug_image_text(pix))
                        # if (pix.size < image_size):
                        #     # The image is too small to be considered a figure
                        #     f.writelines(["\n", "**Skip**", "\n"])
                        #     # continue

                        image_name = f"{pdf_slug}-p{index:03d}-{xref}.png"
                        image_path = os.path.join(path_to_notes, image_name)
                        markdown_reference = "/".join([image_name])
                        if pix.colorspace.name in [fitz.csRGB.name, fitz.csGRAY.name]:       # this is GRAY or RGB
                            pix.writePNG(image_path)
                        elif pix.colorspace.name in [fitz.csCMYK.name]:               # CMYK: convert to RGB first
                            pix1 = fitz.Pixmap(fitz.csRGB, pix)
                            pix1.writePNG(image_path)
                            pix1 = None
                        pix = None
                        f.writelines(["\n", "[![](", markdown_reference, ")](",markdown_reference,")" "\n"])
                    except:
                        print(f"There was a problem saving an image")

    # Check for notes directory
    path_to_notes_dir = os.path.join(path_to_notes, "notes")
    if (not os.path.exists(path_to_notes_dir)):
        os.mkdir(path_to_notes_dir)

    notes_path = os.path.join(path_to_notes_dir, f"{time}.md")

    with open(notes_path, "a", encoding='utf-8') as f:
        metadata_title = doc.metadata['title'][0:20]

        if not metadata_title:
            file = os.path.basename(path_to_pdf_copy)
            ext = os.path.splitext(file)
            notes_name_title = text_utils.slugify(ext[0])
        else:
            notes_name_title = text_utils.slugify(metadata_title)

        notes_frontmatter = text_utils.make_frontmatter(
            title = f"Notes - {time}",
            author = doc.metadata['author']
        )
        f.writelines(notes_frontmatter)
        

    with open(notes_path, "a", encoding='utf-8') as f:
        f.writelines(["\n\n", "# ", datetime.now().strftime("%Y%m%d %H:%M:%S"), "\n\n"])

        pages = [ doc[ i ] for i in range( doc.pageCount ) ]

        for index, page in enumerate(pages, start=1):

            # Indicate page number
            f.write("\n## Page {}\n".format(index))

            text_words = page.getTextWords()
        #   print(text_words)

            # The words should be ordered by y1 and x0
            sorted_words = SortedCollection( key = itemgetter( 3, 0 ) )

            for word in text_words:
                sorted_words.insert( word )

            # At this point you already have an ordered list. If you need to 
            # group the content by lines, use groupby with y1 as a key
            lines = groupby( sorted_words, key = itemgetter( 3 ) )

            # Get annotations
            annot = page.firstAnnot

            # Skip if there are no anntations
            if not annot:
                f.write("\n- No annotations on this page\n")
                

            while annot:
                # Debug annotation type
                # f.write(''.join(["\ntype: ", str(annot.type[0])]))
                
                # Text annotation
                if annot.type[0] == 0:
                    text = "\n- %s" % (annot.info['content'])
                    f.write(text)

                # Highlight, Underline, Strikethrough, etc
                f.write("\n")
                if annot.type[0] in (8, 9, 10, 11): # one of the 4 types above
                    if (annot.info['content'] == ''):
                        text = "\n- %s" % ("Highlighted text: ")
                        f.write(text)
                    else:
                        text = "\n- %s" % (annot.info['content'])
                        f.write(text)
                    rect = annot.rect # this is the rectangle the annot covers

                    # Intersecting bounds - full word
                    mywords = [w for w in text_words if fitz.Rect(w[:4]).intersects(rect)]
                    try:
                        f.write("\n\n    > ")
                        f.write(make_text(mywords))
                        f.write("\n")
                    except UnicodeEncodeError:
                        print("Error writing annotation")

                annot = annot.next # None returned after last annot

        f.writelines(["\n\n", "---"])
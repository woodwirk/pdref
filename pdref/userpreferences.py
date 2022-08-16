class UserPreferences:
    def __init__(self, pdfs_path = None, notes_path = None, earliest_modified_date = None):
        self.pdfs_path = pdfs_path
        self.notes_path = notes_path
        self.earliest_modified_date = earliest_modified_date
        self.debug = False
        self.image_size = None
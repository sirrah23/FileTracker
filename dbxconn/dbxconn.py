import dropbox


class DBXRepo:
    """
    Connect to Dropbox and interact with the files there
    """

    def __init__(self, token):
        self.token = token

    def get_file_metadata(f):
        dbx = dropbox.Dropbox(self.token)
        if not f.startswith('/'):
            f = '/' + f
        try:
            return dbx.files_get_metadata(f)
        except dropbox.exceptions.ApiError:
            return None

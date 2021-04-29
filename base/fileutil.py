import string
import os
from os import path

VALID_CHARS_4_FILENAME="-_.() {}{}".format( string.ascii_letters, string.digits )


class GhFileUtil:

    @staticmethod
    def normalizeFileName(input):
        return ''.join(c for c in input if c in VALID_CHARS_4_FILENAME)

    @staticmethod
    def fileExist(file):
        return path.exists(file)
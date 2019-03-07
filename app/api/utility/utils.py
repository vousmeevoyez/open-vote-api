""" 
    Utility
"""
from uuid import UUID
import traceback
import base64
import binascii
import os
import time
import random

from flask import current_app

from werkzeug.utils import secure_filename

from app.config import config

from app.api.error.http import *

ERROR = config.Config.ERROR
ALLOWED_EXTENSIONS = config.Config.ALLOWED_EXTENSIONS

class DecodeError(Exception):
    """ raised when failed decode uuid """

def string_to_uuid(string):
    """ convert uuid bytes to base64 url safe string"""
    try:
        uuid_obj = UUID(string)
    except:
        raise BadRequest(ERROR["DECODE"]["TITLE"], ERROR["DECODE"]["MESSAGE"])
    return uuid_obj

def allowed_file(filename):
    """ check file extension and make sure only allowed file ext can be
    processed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_file_name(filename):
    filename, extension = os.path.splitext(filename)

    prefix = str(random.randint(1, 1000000))
    return prefix + "_"  + str(int(time.time())) + extension


def upload(files):
    if files.filename == "":
        raise BadRequest("NO_FILE_ATTACHED", "No file attached")

    if files and allowed_file(files.filename):
        filename = secure_filename(files.filename)
        random_name = generate_file_name(filename)

        files.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                random_name))
    return random_name

def remove(filename):
    """ utility to remove a file """
    result = True
    fullpath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                            filename)
    if os.path.isfile(fullpath):
        os.remove(fullpath)
    else:
        result = False

    return result
#end def

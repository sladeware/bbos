#!/usr/bin/env python

from hashlib import md5

def md5sum(filename, buf_size=8192):
    m = md5()
    # the with statement makes sure the file will be closed
    with open(filename) as f:
        # read the file in small chunk until EOF
        data = f.read(buf_size)
        while data:
            # we had data to the md5 hash
            m.update(data)
            data = f.read(buf_size)
    # return the md5 hash in hexadecimal format
    return m.hexdigest()

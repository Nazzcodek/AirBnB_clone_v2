#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive 
from the contents of the web_static
"""
from fabric import *
from datetime import datetime as dt
import os


def do_pack():
    """this is a do pack fabric method"""
    dt = dt.utcnow()
    date =[dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second]
    file_path = ("versions/web_static_{}{}{}{}{}{}.tgz".format(*date))

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local(f"tar -cvzf {filw_path} web_static").failed is True:
        return None
    return file_path

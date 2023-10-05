#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from the web_static folder"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Creates a .tgz archive from web_static folder"""
    try:
        # Create the "versions" folder if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Create the archive filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_filename = "versions/web_static_{}.tgz".format(timestamp)

        # Compress web_static into the archive
        local("tar -cvzf {} web_static".format(archive_filename))

        return archive_filename
    except Exception:
        return None


if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        print("web_static packed: {}".format(archive_path))
    else:
        print("Packing failed.")

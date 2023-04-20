#!/usr/bin/python3
"""Generate a .tgz archive from web_static folder."""
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Generate a .tgz archive from contents of web_static folder
    """
    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Generate timestamp for the archive name
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')

        # Create archive using tar
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))

        # Return the archive path if archive has been
        # generated correctly
        return archive_path

    except:
        # Return None if archive could not be generated
        return None

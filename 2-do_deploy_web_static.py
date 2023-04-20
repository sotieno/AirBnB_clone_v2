#!/usr/bin/python3
"""Script to distribute archive to your web servers"""
from datetime import datetime
from fabric.api import *
import os

env.hosts = ["52.91.146.214", "54.160.76.161"]
env.user = "ubuntu"


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


def do_deploy(archive_path):
    """
    Distribute .tgz archive
    """
    # Check if archive file exists
    if not os.path.isfile(archive_path):
        return False

    # Get the filename of the archive without the .tgz extension
    filename = os.path.basename(archive_path).split('.')[0]

    try:
        # Upload archive to /tmp/ directory on web server
        put(archive_path, "/tmp/")

        # Create directory where code will be deployed
        run("sudo mkdir -p /data/web_static/releases/{}/".format(filename))

        # Uncompress the archive to the web server
        run("sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(filename, filename))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}.tgz".format(filename))

        # Move the code to the correct directory
        run("sudo mv /data/web_static/releases/{}/web_static/*\
             /data/web_static/releases/{}/".format(filename, filename))

        # Delete the empty directory
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(filename))

        # Delete the symbolic link
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("sudo ln -s /data/web_static/releases/{}/\
             /data/web_static/current".format(filename))

        print("New version deployed!")
        return True
    except:
        return False

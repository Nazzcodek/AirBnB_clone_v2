#!/usr/bin/python3
"""
Fabric scripts that distribute an archive to web servers
"""
import os
from fabric.api import run, task, env, put, local, runs_once
from datetime import datetime

env.hosts = ['52.3.245.154', '54.157.143.250']
env.user = 'ubuntu'


@task
def do_deploy(archive_path):
    """ deploying archive function """
    if not os.path.exists(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Upload the archive to /tmp
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    # Remove existing release directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Create a new release directory
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Extract the contents of the archive to the new release directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed:
        return False

    # Remove the uploaded archive
    if run("rm /tmp/{}".format(file)).failed:
        return False

    # Move contents to the proper location
    if run("mv /data/web_static/releases/{}/web_static/* \
           /data/web_static/releases/{}/".
           format(name, name)).failed:
        return False

    # Remove the old web_static directory
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed:
        return False

    # Remove the current symbolic link
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create a symbolic link to the new release
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed:
        return False

    return True


@runs_once
def do_pack():
    """this is a do pack fabric method"""
    dt = datetime.now()
    date = dt.strftime("%Y%m%d%H%M%S")
    file_path = ("versions/web_static_{}.tgz".format(date))

    if os.path.exists("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file_path)).failed is True:
        return None
    return file_path


@task
def deploy():
    """Deploy archive to web server."""
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)


@runs_once
def clean_local(number):
    """Remove unnecessary archives locally."""
    local("ls -dt versions/* | tail -n +{} | sudo xargs rm -fr".format(number))


@task
def do_clean(number=0):
    """ Delete arvhive """
    try:
        number = int(number)
    except ValueError:
        return

    if number == 0:
        number = 1

    keep = number + 1

    clean_local(keep)

    releases_path = "/data/web_static/releases"
    run("ls -dt {} | tail -n +{} | xargs rm -rf".format(releases_path, keep))

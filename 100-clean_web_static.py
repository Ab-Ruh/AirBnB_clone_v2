#!/usr/bin/python3
"""
removes archives which are out of date
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.24.74.170', '18.234.80.72']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    local("mkdir -p versions")

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    archive_name = "web_static_{}.tgz".format(timestamp)

    result = local("tar -czvf versions/{} web_static".format(archive_name))

    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to a web server
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name.split('.')[0]
        target_path = "/data/web_static/releases/" + archive_no_ext

        put(archive_path, '/tmp', use_sudo=True)
        run('sudo mkdir -p {}'.format(target_path))
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_name, target_path))
        run('sudo rm /tmp/{}'.format(archive_name))
        run('sudo mv {}/web_static/* {}/'.format(target_path, target_path))
        run('sudo rm -rf {}/web_static'.format(target_path))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(target_path))
        return True
    except Exception as e:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)


def do_clean(number=0):
    """
    removes archives
    """
    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    releases_path = '/data/web_static/releases'
    run('cd {}; ls -t | tail -n +{} | xargs rm -rf'
        .format(releases_path, number))

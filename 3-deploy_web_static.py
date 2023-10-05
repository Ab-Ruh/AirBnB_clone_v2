#!/usr/bin/python3
"""
Fabric script to create and distribute an archive and deploy it to web servers
"""

from fabric.api import local, env, run
from os.path import exists
from datetime import datetime
from os import path
from shutil import copyfile

env.hosts = ['your_web_server_ip1', 'your_web_server_ip2']
env.user = 'your_ssh_user'
env.key_filename = ['path/to/your/ssh/key']


def do_pack():
    """Create a .tgz archive from the web_static folder"""
    try:
        if not path.exists("versions"):
            local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_filename = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_filename))
        return archive_filename
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute and deploy an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_ext = archive_filename.split('.')[0]
        release_path = '/data/web_static/releases/{}/'.format(archive_no_ext)

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))
        run('rm /tmp/{}'.format(archive_filename))
        run('mv {}web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive and deploy it to web servers"""
    archive_path = do_pack()
    if archive_path:
        result = do_deploy(archive_path)
        return result
    return False


if __name__ == '__main__':
    result = deploy()
    if result:
        print('New version deployed!')
    else:
        print('Deployment failed.')

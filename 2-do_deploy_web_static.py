#!/usr/bin/python3
"""
Fabric script to distribute and deploy an archive to web servers
"""

from fabric.api import local, put, run, env
from os.path import exists
from datetime import datetime

env.hosts = ['your_web_server_ip1', 'your_web_server_ip2']
env.user = 'your_ssh_user'
env.key_filename = ['path/to/your/ssh/key']


def do_deploy(archive_path):
    """
    Distributes and deploys an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive filename
        # without extension>/
        archive_filename = archive_path.split('/')[-1]
        release_path = '/data/web_static/releases/{}'.format(
            archive_filename[:-4]
        )
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Delete the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted archive to the release folder
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the web_static folder
        run('rm -rf {}/web_static'.format(release_path))

        # Remove the old symbolic link if it exists
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('ln -s {} /data/web_static/current'.format(release_path))

        print('New version deployed!')
        return True

    except Exception as e:
        return False


if __name__ == '__main__':
    archive_path = 'versions/web_static_{}.tgz'.format(
        datetime.now().strftime('%Y%m%d%H%M%S')
    )
    result = do_deploy(archive_path)
    if result is False:
        print('Deployment failed.')

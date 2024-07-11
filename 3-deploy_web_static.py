#!/usr/bin/python3
"""
Distributes an archive to your web servers,
using the function do_deploy
"""

from datetime import datetime
from fabric.api import put, run, env, local
from os.path import exists
env.hosts = ['54.160.119.223', '18.235.243.61']


def do_pack():
    """
    create an archive from web_static dir
    """
    time = datetime.now()
    archive_name = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')

    result = local('tar -cvzf versions/{} web_static'.format(archive_name))
    if result is not None:
        return archive_name
    else:
        return None

def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        path = "/data/web_static/releases/"
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False

def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)

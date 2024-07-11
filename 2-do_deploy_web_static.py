#!/usr/bin/python3
"""
Distributes an archive to your web servers
"""

from fabric.api import env, run, put
import os

env.hosts = ['54.160.119.223', '18.235.243.61']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        no_ext = archive_name.split('.')[0]
        remote_path = f"/tmp/{archive_name}"
        put(archive_path, remote_path)

        release_path = f"/data/web_static/releases/{no_ext}"
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf /tmp/{archive_name} -C {release_path}")
        run(f"rm /tmp/{archive_name}")

        run(f"mv {release_path}/web_static/* {release_path}/")
        run(f"rm -rf {release_path}/web_static")

        run("rm -rf /data/web_static/current")

        run(f"ln -s {release_path} /data/web_static/current")

        return True
    except:
        return False

#!/usr/bin/python3
"""
Generates a .tgz archive from the contents of the web_static
"""

from datetime import datetime
from fabric.api import local


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

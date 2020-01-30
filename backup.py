#!/usr/bin/env python3

import os
import datetime
import time

from sh import rsync
from sh import ssh


backupdir = "/backups/"
host_list = []
now = datetime.datetime.now()
date_time_string = now.strftime("_%Y_%m_%d")
directory_list = []


# Functions
def loop_hosts_and_save_to_list():
    with open("%shosts" % backupdir) as hosts:
        for line in hosts:
            host_list.append(str(line.rstrip()))


def create_dirs_and_save_to_list():
    for host in host_list:
        directory = "%s%s%s" % (backupdir, str(host), date_time_string)
        os.mkdir(directory)
        directory_list.append(directory)


def loop_hosts_and_backup():
    for host in host_list:
        host_file = backupdir+host
        index = directory_list.index(host_file + date_time_string)
        with open(host_file) as host_directories:
            for line in host_directories:
                ssh("root@%s" % str(host), "tar -czvf /tmp/%s.tar.gz %s" % (str(host + date_time_string), line.rstrip()))
                time.sleep(1)
                rsync("-av", "--delete", "-e ssh", "root@%s:/tmp/%s" % (str(host), str(host) + date_time_string + ".tar.gz"), "%s" % str(directory_list[index]))


loop_hosts_and_save_to_list()
create_dirs_and_save_to_list()
loop_hosts_and_backup()

import os

from decouple import config

server_ip = config('SERVER_IP')
allowed_hosts_target = 'facebot.104.236.104.21.xip.io'
# os.system('ssh dokku@104.236.104.21  config facebot')
to_server = ''
with open('.env') as file:
    for line in file:
        if not line[:1] == '#':
            line = line[:-1].split('=')
            if line[0] == 'ALLOWED_HOSTS':
                line = [line[0], server_ip]
                os.system("echo '{}'".format(line))
            elif line[0] == 'SERVER_IP':
                os.system("echo '{}'".format(line))
            else:
                os.system("echo '{}'".format(line))
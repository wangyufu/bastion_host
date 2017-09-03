#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import os
import socket
import sys
import traceback

import paramiko

try:
    import interactive
except ImportError:
    from web.libs import interactive


def manual_auth(t, username, hostname, pw):
    # default_auth = 'p'
    # auth = input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)
    # if len(auth) == 0:
    #     auth = default_auth
    #
    # if auth == 'r':
    #     default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
    #     path = input('RSA key [%s]: ' % default_path)
    #     if len(path) == 0:
    #         path = default_path
    #     try:
    #         key = paramiko.RSAKey.from_private_key_file(path)
    #     except paramiko.PasswordRequiredException:
    #         password = getpass.getpass('RSA key password: ')
    #         key = paramiko.RSAKey.from_private_key_file(path, password)
    #     t.auth_publickey(username, key)
    # elif auth == 'd':
    #     default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_dsa')
    #     path = input('DSS key [%s]: ' % default_path)
    #     if len(path) == 0:
    #         path = default_path
    #     try:
    #         key = paramiko.DSSKey.from_private_key_file(path)
    #     except paramiko.PasswordRequiredException:
    #         password = getpass.getpass('DSS key password: ')
    #         key = paramiko.DSSKey.from_private_key_file(path, password)
    #     t.auth_publickey(username, key)
    # else:
    #     pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
    t.auth_password(username, pw)


# setup logging
def ssh_channel(self, bind_host_user_obj, models):
    hostname = bind_host_user_obj.host.ip_addr
    port = bind_host_user_obj.host.port
    username = bind_host_user_obj.host_user.username
    password = bind_host_user_obj.host_user.password

    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception as e:
        print('*** Connect failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print('*** Unable to open host keys file')
                keys = {}

        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if hostname not in keys:
            print('*** WARNING: Unknown host key!')
        elif key.get_name() not in keys[hostname]:
            print('*** WARNING: Unknown host key!')
        elif keys[hostname][key.get_name()] != key:
            print('*** WARNING: Host key has changed!!!')
            sys.exit(1)
        else:
            print('*** Host key OK.')

        if not t.is_authenticated():
            manual_auth(t, username, hostname, password)
        if not t.is_authenticated():
            print('*** Authentication failed. :(')
            t.close()
            sys.exit(1)

        chan = t.open_session()
        chan.get_pty()
        chan.invoke_shell()
        print('*** Here we go!\n')
        # 连接上，创建一条session信息
        session_obj = models.SessionLog.objects.create(account=self.user, bind_host_user=bind_host_user_obj)
        interactive.interactive_shell(chan, models, session_obj)
        chan.close()
        t.close()

    except Exception as e:
        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)



#!/usr/bin/env python
from django.contrib.auth import authenticate

from web import models
from web.libs import demo


class UserInteractive(object):
    """用户的shell 界面"""

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
        self.user = None

    def auth(self):
        token = input("Input your token,if don't have ,press Enter:").strip()
        if token:
            token_objs = models.Token.objects.filter(val=token)
            token_obj = None
            if len(token_objs) == 0:
                print("invalid token...")
            elif len(token_objs) > 1:   # 重复的token取最后一个
                token_obj = token_objs.latest()
            else:
                token_obj = token_objs[0]
                self.user = token_obj.account
            if token_obj:
                return token_obj, 'token'
        count = 0
        while count < 3:
            username = input('Username:').strip()
            password = input('Password:').strip()
            # authenticate 验证admin的用户
            user = authenticate(username=username, password=password)
            if user:
                self.user = user
                return True
            else:
                print('Wrong username or password!')
                count += 1
        else:
            exit('Too many attempts!')

    def welcome_msg(self):
        msg = """Welcome logon Luffy JumpServer terminal""".center(80, '-')
        print(msg)

    def start(self):
        """ 登录交互入口"""
        if self.auth():
            self.welcome_msg()

            while True:
                host_groups = self.user.host_groups.all()

                for index, group in enumerate(host_groups):
                    print(index, group)
                print(len(host_groups), '未分组主机')

                choice = input('select group>>:').strip()
                if choice.isdigit():
                    choice = int(choice)
                    # groups list
                    if len(host_groups) > choice >= 0:
                        selected_group = host_groups[choice]
                        bind_host_user_list = selected_group.bind_host_users.all()
                    # 为分组的机器
                    if choice == len(host_groups):
                        bind_host_user_list = self.user.bind_host_users.all()

                    while True:
                        for index, host in enumerate(bind_host_user_list):
                            print("\t", index, host)
                        choice = input("select host >>:").strip()
                        if choice.isdigit():
                            choice = int(choice)
                            if len(bind_host_user_list) > choice >= 0:
                                selected_host = bind_host_user_list[choice]  # 选中的主机
                                # start login
                                demo.ssh_channel(self, selected_host, models)
                        elif choice == 'b':
                            break
                        elif choice == 'exit':
                            exit("bye.")

                elif choice == 'exit':
                    exit("bye.")

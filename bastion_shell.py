#!/usr/bin/env python

import os
import sys

if __name__ == '__main__':
    # 配置默认环境变量django,之后才能导入django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bastion_host.settings")
    import django
    # 加载
    django.setup()
    from web.libs import user_interface

    obj = user_interface.UserInteractive(sys.argv)
    obj.start()
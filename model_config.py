# -*- coding: utf-8 -*-

"""
    读取配置文件
"""

import ConfigParser


class Config():
    """
        配置类
    """
    config = ConfigParser.SafeConfigParser()
    config.read('model.conf')

    @classmethod
    def getconfig(cls, key, section='database'):
        """
            返回配置信息
        """
        return cls.config.get(section, key)

if __name__ == '__main__':
    # dbname = Config()
    print Config.getconfig('db_user')

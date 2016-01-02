# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月31日
#

'''
    启动Tornado服务器的入口
'''

import tornado.ioloop
import tornado.autoreload
import model_application
import logging
import datetime
import traceback
# import email_sender
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    model_application.application.listen(options.port)
    server_instance = tornado.ioloop.IOLoop.instance()
    # tornado.autoreload.add_reload_hook(database.release)
    try:
        server_instance.start()
    except KeyboardInterrupt:
        logging.error("Existing")
        exit_error = '按键Cc退出'
    except Exception, e:
        logging.exception(e)
        exit_error = traceback.format_exec()
    finally:
        server_instance.add_callback(server_instance.stop)
        exit_error = str(datetime.datetime.now()) + '\n' + exit_error

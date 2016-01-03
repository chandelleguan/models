# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月31日
#
'''
    加载服务器设置的application文件
'''

import tornado.web
import model_handler
from model_settings import settings

application = tornado.web.Application([
    (r"/models", model_handler.ModelsHandler),
    (r"/model/(\S+)", model_handler.ModelHandler),
    (r"/experiment/(\S+)", model_handler.ExperimentHandler),
    (r"/paper/(\S+)", model_handler.PaperHandler),
    (r".*", model_handler.BaseHandler),
], **settings)

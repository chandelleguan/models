# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月20日
#
'''
    业务处理逻辑
'''

import tornado.web
import model_db
import email_sender
import traceback


class BaseHandler(tornado.web.RequestHandler):
    '''
        基础handler
    '''
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        try:
            message = \
                '\n'.join(traceback.format_exception(*kwargs['exc_info']))
        except KeyError:
            message = str(status_code)
        email_sender.async_send(title="服务器错误", message=message)
        self.render('404.html', page_title="404")


class ModelsHandler(BaseHandler):
    '''
        模型列表页面handler
    '''


class ModelHandler(BaseHandler):
    '''
        模型展示页handler
    '''


class ExperimentHandler(BaseHandler):
    '''
        模型实验效果展示页handler
    '''

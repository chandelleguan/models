# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月30日
#
'''
    包含前端模块定义的文件
'''
import tornado.web


class ModelListItemModule(tornado.web.UIModule):
    '''
        模型列表页列表项模块
    '''
    def render(self, model):
        return self.render_string('module\modelItem.html', model=model)

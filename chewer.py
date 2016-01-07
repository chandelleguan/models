# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月20日
#
'''
    其他处理程序
'''
# import model_db


def static_image(image, suffix='jpeg'):
    '''
        处理image 转化为伪静态地址
    '''
    if image is None:
        return None

    return ''.join(('img/', str(image), '.', suffix))

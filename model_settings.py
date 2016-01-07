# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月31日
#
import os.path

import model_modules

settings = {
    'debug': True,
    'autoescape': None,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'template_path': os.path.join(os.path.dirname(__file__), "template"),
    'ui_modules': {
        'ModelItem': model_modules.ModelListItemModule,
    }
}

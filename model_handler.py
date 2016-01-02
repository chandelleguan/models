# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月20日
#
'''
    业务处理逻辑
'''
import os.path

import tornado.web
import model_db
# import email_sender
import traceback

import model_modules
import database


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
        # email_sender.async_send(title="服务器错误", message=message)
        print message  # 暂时代替上一行
        self.render('404.html', page_title="404")


class ModelsHandler(BaseHandler):
    '''
        模型列表页面handler
    '''

    def get(self):
        models = model_db.Model.query()
        if models:
            models = [model_db.Model.chew(model) for model in models]
        self.render(
            "models.html",
            page_title="ModelList",
            models=models,
        )

    def post(self):
        query_num = self.get_argument('query_num', None)

        if query_num is None:
            self.write('failed')
            return None

        models = model_db.Model.query(int(query_num))

        write_str =\
            ''.join(
                (
                    self.render_string(
                        'module/modelItem.html',
                        model=model_db.Model.chew(model),
                    ) for model in models
                )
            )

        load_more = '-1' if len(models) < 10 else str(int(query_num) + 1)

        self.write({'write_str': write_str, 'load_more': load_more})


class ModelHandler(BaseHandler):
    '''
        模型展示页handler
    '''
    def get(self, model_id):

        model = model_db.Model.get_in_model_id(model_id)
        model = model_db.Model.chew(model)

        paper = database.Paper.get(model.refer)
        paper = database.Paper.chew(paper)

        process = model_db.Model.get_in_proc_id(model.model_proc)
        process = model_db.Model.chew(process)

        self.render(
            "model.html",
            page_title=model.name,
            model=model,
            paper=paper,
            process=process,
        )


class ExperimentHandler(BaseHandler):
    '''
        模型实验效果展示页handler
    '''


def main():
    # parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', ModelsHandler)],
        # 'static_path': config.Config.get_local_position('static'),
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        ui_modules={'ModelItem': model_modules.ModelListItemModule}
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

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
# import email_sender
import traceback

# import database


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
        self.render("404.html", page_title="404")


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

        paper = model_db.Paper.get(model.refer)
        paper = model_db.Paper.chew(paper)

        process = model_db.Process.get_in_proc_id(model.proc)
        process = model_db.Process.chew(process)

        experiments = model_db.Experiment.query(model_id)
        if experiments:
            experiments = (
                [model_db.Experiment.chew(experiment)
                    for experiment in experiments]
            )

        self.render(
            "model.html",
            page_title=model.name,
            model=model,
            paper=paper,
            process=process,
            experiments=experiments,
        )


class ExperimentHandler(BaseHandler):
    '''
        单个模型实验效果展示页handler
    '''
    def get(self, exp_id):

        model_id = self.get_argument("model_id", 0)

        experiment = model_db.Experiment.get_in_exp_id(exp_id)
        experiment = model_db.Experiment.chew(experiment)

        datasets = model_db.Dataset.query_in_model_id(model_id)
        if not datasets:  # 若按照model_id取出来记录为空，则说明用exp_id标注
            datasets = model_db.Dataset.query_in_exp_id(exp_id)
        if datasets:
            datasets = (
                [model_db.Dataset.chew(dataset)
                    for dataset in datasets]
            )

        evaluations = model_db.Evaluation.query(exp_id)
        if evaluations:
            evaluations = (
                [model_db.Evaluation.chew(evaluation)
                    for evaluation in evaluations]
            )

        baselines = model_db.Baseline.query(exp_id)
        if baselines:
            baselines = (
                [model_db.Baseline.chew(baseline)
                    for baseline in baselines]
            )

        results = model_db.Result.query(exp_id)
        if results:
            results = (
                [model_db.Result.chew(result)
                    for result in results]
            )

        self.render(
            "experiment.html",
            page_title=experiment.exp_name,
            experiment=experiment,
            datasets=datasets,
            evaluations=evaluations,
            baselines=baselines,
            results=results,
        )

    def post(self):
        '''
            接收客户请求做出相应显示
        '''


class PaperHandler(BaseHandler):

    def get(self, paper_id):

        paper = model_db.Paper.get(paper_id)
        paper = model_db.Paper.chew(paper)

        self.render(
            "paper.html",
            page_title=paper.title,
            paper=paper,
        )

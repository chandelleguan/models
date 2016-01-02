# -*- coding: utf-8 -*-
#
# Author: Chenyu Guan
#
# Created Time: 2015年12月20日
#
'''
    数据持久化操作
'''

import torndb
import logging

import model_config


conf = model_config


def get_connection(function):
    '''装饰器，连接数据库'''
    def wrapper(cls, *args, **kwargs):

        try:
            connection = torndb.Connection(
                conf.Config.getconfig('db_host'),
                cls.db,
                conf.Config.getconfig('db_user'),
                conf.Config.getconfig('db_passwd')
            )
        except AttributeError:
            logging.error(
                (
                    'Mysql Connection Error: '
                    'class {cls} db not assigned'
                ).format(
                    cls=cls.__name__
                )
            )
            # 如果函数名含有query返回list[]，否则返回None
            return None if 'query' not in function.__name__ else []
        return function(cls, connection, *args, **kwargs)
    return wrapper


class Model(object):
    '''
        model表持久化
    '''
    db = 'model_db'

    @classmethod
    @get_connection
    def get_in_model_id(cls, connection, model_id):
        '''
            按model_id取单条记录
        '''
        sql = \
            (
                'SELECT * FROM model WHERE model_id = %s'
            )
        return connection.get(sql, model_id)

    @classmethod
    @get_connection
    def get_in_refer(cls, connection, refer):
        '''
            按所属论文id取单条记录（一一对应）
        '''
        sql = \
            (
                'SELECT * FROM model WHERE refer = %s'
            )
        return connection.get(sql, refer)

    @classmethod
    @get_connection
    def query(cls, connection, query_num=1):
        '''
            直接返回全部model记录
            query_num表示显示次数，即第几次显示
        '''
        entry_number = 10  # 每次显示的记录数目
        query_num = query_num if query_num >= 1 else 1

        sql = (
            'SELECT * FROM model LIMIT {start}, {end}'
        ).format(
            start=(query_num - 1) * entry_number,
            end=query_num * entry_number,
        )

        return connection.query(sql)

    @classmethod
    @get_connection
    def query_in_time_order(cls, connection):
        '''
            按照所属论文的发表时间进行排序返回记录集
        '''
        sql = (
            'SELECT * '
            'FROM homepage.article '
            'NATURAL JOIN homepage.paper '
            'NATURAL JOIN model '
            'ORDER BY publish_year DESC'
        )
        return connection.query(sql)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''
        application = Application.get_in_app_id(model.app)
        if application:
            model.app = application.app_type
        else:
            model.app = 'Not Classified Yet'

        return model


class Application(object):
    '''
        模型所属类别 application表持久化
    '''
    db = 'model_db'
    # APPLICATION_TYPE = ['', '', '']

    @classmethod
    @get_connection
    def get_in_app_id(cls, connection, app_id):
        '''
            按app_id取类别记录
        '''
        sql = 'SELECT * FROM application WHERE app_id = %s'
        return connection.get(sql, app_id)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''


class Baseline(object):
    '''
        baseline表持久化
    '''
    db = 'model_db'

    @classmethod
    @get_connection
    def get_in_base_id(cls, connection, base_id):
        '''
            按base_id获取单条记录
        '''
        sql = 'SELECT * FROM baseline WHERE base_id = %s'
        return connection.get(sql, base_id)

    @classmethod
    @get_connection
    def query(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的baseline记录
        '''
        sql = 'SELECT * FROM baseline WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''


class Dataset(object):
    '''
        dataset表持久化
    '''
    db = 'model_db'

    @classmethod
    @get_connection
    def get_in_data_id(cls, connection, data_id):
        '''
            按data_id取单条记录
        '''
        sql = 'SELECT * FROM dataset WHERE data_id = %s'
        return connection.get(sql, data_id)

    @classmethod
    @get_connection
    def query(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的dataset记录
        '''
        sql = 'SELECT * FROM dataset WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''


class Evaluation(object):
    '''
        评估信息evaluation表持久化
    '''
    db = 'model_db'

    @classmethod
    @get_connection
    def get_in_evl_id(cls, connection, evl_id):
        '''
            按evl_id取单条记录
        '''
        sql = 'SELECT * FROM evaluation WHERE evl_id = %s'
        return connection.get(sql, evl_id)

    @classmethod
    @get_connection
    def query(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的evaluation记录
        '''
        sql = 'SELECT * FROM evaluation WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''


class Result(object):
    '''
        实验结果信息result表持久化
    '''
    db = 'model_db'

    @classmethod
    @get_connection
    def get_in_result_id(cls, connection, result_id):
        '''
            按evl_id取单条记录
        '''
        sql = 'SELECT * FROM result WHERE result_id = %s'
        return connection.get(sql, result_id)

    @classmethod
    @get_connection
    def query(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的result记录
        '''
        sql = 'SELECT * FROM result WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''


class Experiment(object):
    '''
        experiment表持久化
    '''
    db = 'model_db'

    @classmethod
    @get_connection
    def get_in_exp_id(cls, connection, exp_id):
        '''
            按exp_id取单条记录
        '''
        sql = 'SELECT * FROM experiment WHERE exp_id = %s'
        return connection.get(sql, exp_id)

    @classmethod
    @get_connection
    def query(cls, connection, model_id):
        '''
            按model_id所属模型获取属于该模型的实验记录
        '''
        sql = 'SELECT * FROM experiment WHERE model_id = %s'
        return connection.query(sql, model_id)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''


class Process(object):
    '''
        模型详细信息process表持久化
    '''
    db = 'model_db'

    @classmethod
    @get_connection
    def get_in_proc_id(cls, connection, proc_id):
        '''
            按proc_id取单条记录
        '''
        sql = 'SELECT * FROM process WHERE proc_id = %s'
        return connection.get(sql, proc_id)

    @classmethod
    def chew(cls, process):
        '''
            process 处理函数
        '''

        return process

# -*- coding: utf-8 -*-

import model_db

connection = ''


SET = ['model_id', 'name', 'refer', 'app', 'goal', 'proc']
'''
# 多条返回记录测试
results = model_db.Model.query()
# print results
print [results[num][key] for num in range(len(results)) for key in SET]
# print [results[num] for num in range(len(results))]
'''

# 多条返回记录测试
model_id = 1
result = model_db.Model.get_in_model_id(model_id)
print result  # dict{}
print [result[key] for key in SET]  # list[]

# 无记录返回出错测试
record = model_db.Baseline.query(2)
print record

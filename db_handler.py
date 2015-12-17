# -*- coding: utf-8 -*-

import torndb


class MysqlHandler(object):
    """Dealing with database for data exchanging."""
    def __init__(self):
        db = torndb.Connection("localhost", "model_db", "root", "50136")
        return db

    def getone(self, tname, tid):
        """Get one record in table "tname" with a given primary_key value."""
        db = torndb.Connection("localhost", "model_db", "root", "50136")
        skey = 'SELECT k.column_name \
            FROM information_schema.table_constraints t \
            JOIN information_schema.key_column_usage k \
            USING (constraint_name,table_schema,table_name) \
            WHERE t.constraint_type = "PRIMARY KEY" \
            AND t.table_schema = "model_db" \
            AND t.table_name = "' + tname + '";'
        results = db.query(skey)
        key = results[0]['column_name']   # get primary_key name
        sql = 'select * from ' + tname + ' where result_id = ' + key + ';'
        record = torndb.get(sql)
        return record

    def getmany(self, tname):
        """Get all records in table "tname" ."""
        sql = 'select * from ' + tname + ' ;'
        records = torndb.query(sql)
        return records

import sqlite3
import unittest

import prql


class TestSqlGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.base_path = 'employee_examples'
        db_path = f'./{self.base_path}/employee.db'
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()

    def run_query(self, text, expected=None):
        print(text.replace('\n\n', '\n'))
        print('-' * 40)
        sql = prql.to_sql(text)
        print(sql)
        rows = self.cur.execute(sql)
        columns = [d[0] for d in rows.description]
        print(f'Columns: {columns}')
        rows = rows.fetchall()
        if expected is not None:
            assert (len(rows) == expected)

    def test_select_all(self):
        q = '''
        from table
        '''
        res = prql.to_sql(q)
        self.assertTrue(res.startswith('SELECT * FROM `table`'))
        self.run_query(q)

    def test_limit(self):
        q = 'from table | take 10'
        res = prql.to_sql(q)
        self.assertTrue(res.index('LIMIT 10') != -1)
        self.run_query(q, 10)

    def test_order_by(self):
        q = 'from table | sort country | take 7'
        res = prql.to_sql(q)
        self.assertTrue(res.index('ORDER BY country') != -1)
        self.run_query(q, 7)

    def test_join_syntax(self):
        q = '''
        from table
        join table2 [id=id]
        '''
        res = prql.to_sql(q)
        self.assertTrue(res.index('JOIN table2 table2_t ON table_t.id = table2_t.id') != -1)
        self.run_query(q, 6)

    def test_join_syntax_2(self):
        q = '''
        from table
        join table2 [table.id=table2.id]
        '''
        res = prql.to_sql(q)
        print(res)
        self.assertTrue(res.index('JOIN table2 table2_t ON table_t.id = table2_t.id') != -1)
        self.run_query(q, 6)

    def test_group_by_single_item_array(self):
        q = '''
        from table
        select [ foo, bar ]
        aggregate by:[code] [
            sum price 
        ] 
        '''
        res = prql.to_sql(q)

        self.assertTrue(res.index('sum(price) as sum_price') != -1)
        self.assertTrue(res.index('GROUP BY code') != -1)
        self.run_query(q, 3)

    def test_group_by_double_item_array(self):
        q = '''
        from table
        select [ foo, bar ]
        aggregate by:[code,country] [
            sum price 
        ] 
        '''
        res = prql.to_sql(q)

        self.assertTrue(res.index('sum(price) as sum_price') != -1)
        self.assertTrue(res.index('GROUP BY code,country') != -1)
        self.run_query(q, 5)

    def test_groupby_single_argument(self):
        q = '''
        from table
        select [ foo, bar ]
        aggregate by:code [
            sum price 
        ] 
        '''
        res = prql.to_sql(q)

        self.assertTrue(res.index('sum(price) as sum_price') != -1)
        self.assertTrue(res.index('GROUP BY code') != -1)
        self.run_query(q, 3)

    def test_named_aggs(self):
        q = '''
        from table
        select [ foo, bar ]
        aggregate by:code [
            all_costs: sum price 
        ] 
        '''
        res = prql.to_sql(q)

        self.assertTrue(res.index('sum(price) as all_costs') != -1)
        self.assertTrue(res.index('GROUP BY code') != -1)
        self.run_query(q, 3)

    def test_derive_syntax(self):
        q = '''
        from table
        derive [
         foo_bar: foo + bar
        ]
        '''
        res = prql.to_sql(q)
        self.assertTrue(res.index('foo + bar as foo_bar') != -1)
        self.run_query(q, 12)
        print(res)
import sqlite3

from prql import parse, read_file, script_path, SQLGenerator

if __name__ == '__main__':
    base_path = '/factbook_examples'
    file_names = [
        f'/{base_path}/q1.prql',
        f'/{base_path}/q2.prql',
        f'/{base_path}/q3.prql',
        f'/{base_path}/q3b.prql',
        f'/{base_path}/q4.prql',
        f'/{base_path}/q5.prql',
        f'/{base_path}/q6.prql'

    ]

    expected_results = {
        f'/{base_path}/q1.prql': 1,
        f'/{base_path}/q2.prql': 2,
        f'/{base_path}/q3.prql': 3,
        f'/{base_path}/q3b.prql': 4,
        f'/{base_path}/q4.prql': 4,
        f'/{base_path}/q5.prql': 5,
        f'/{base_path}/q6.prql': 6
    }

    db_path = script_path + f'{base_path}/factbook.db'

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for file_name in file_names:
        text = read_file(file_name)

        print( '\n' + '-' * 80 + f'\nParsing {file_name}\n' + '-' * 80 + '\n' + text + '\n' + '-' * 80)
        if text:
            tree = parse(text)
            sql_generator = SQLGenerator(tree)
            try:
                sql = sql_generator.generate(verbose=False)
                print(f'Result: \n{sql}\n' + '~' * 80 + '\n')

                rows = cur.execute(sql)
                columns = [d[0] for d in rows.description]
                rows = rows.fetchall()

                for row in rows:
                    print(row)

            except Exception as e:
                print(f'\n\nError: {e}\n\n')
                #raise e
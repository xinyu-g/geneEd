import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

'''dependent on the drug central database'''

def get_data(geneSym):
    '''
    retrieve data from database

    return data in data frame
    '''
    user = 'postgres'
    password = 971023
    host = 'localhost'
    port = 5432
    database = 'drugs'
    
    conn_str = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(conn_str)

    query = '''
            SELECT DISTINCT ON (T1.product_name) T1.product_name, T1.target_name, T1.gene, T1.generic_name, T1.route, T2.descr 
            FROM (SELECT * 
            FROM act_table_full acf LEFT JOIN active_ingredient ai USING (struct_id) LEFT JOIN product p USING (ndc_product_code)
            WHERE UPPER(acf.gene) = '{}') T1 JOIN (SELECT *
            FROM tdkey2tc t1 JOIN target_component t2 ON t1.component_id=t2.id 
            JOIN target_keyword t3 ON t1.tdkey_id=t3.id) T2 USING(accession)
            '''

    data = pd.read_sql_query(query.format(geneSym), engine, index_col='product_name')
    # print(len(data))
    engine.dispose()
    return data



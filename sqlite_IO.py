import os
import sqlite3
import pandas as pd
import re


class SQLite:
    def __init__(self, dbName):
        self.dbName = dbName
        self.tbName = ''
        self.data_path = ''
        if not self.dbName.endswith('.db'):
            self.dbName = self.dbName + '.db'

    def sqlite(self):
        if not os.path.exists(self.dbName):
            if_creat = input('数据库不存在是否创建并导入数据？(y/[n])：').strip()
            if if_creat == 'Y' or if_creat == 'y':
                self.tbName = input('请输入表名称：').strip()
                if re.findall(r'(.*?)\.db', self.dbName)[0] == self.tbName:
                    print('表名称不能与数据库重名！')
                    input('按回车键退出......')
                    exit(0)
                return self.creatDB(), self.tbName
            else:
                exit(0)
        else:
            self.tbName = input('请输入表名称：').strip()
            conn = self.connDB()
            if_exist_sql = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{self.tbName}'"
            if_exist = conn.execute(if_exist_sql).fetchall()[0][0]
            if if_exist == 0:
                print(f'数据库中不存在名称为[{self.tbName}]的表!')
                input('按回车键退出......')
                exit(0)

            return conn, self.tbName

    def rd_type(self):
        if self.data_path.endswith('.csv'):
            return pd.read_csv
        elif self.data_path.endswith('.xlsx'):
            return pd.read_excel
        else:
            print('后缀必须是“.csv”或".xlsx"的文件！')
            input('按回车键退出......')
            exit(0)

    def creatDB(self):
        self.data_path = input('要导入的数据文件完整路径(*.csv|*.xlsx)：').strip()
        print('正在创建数据库，请稍后......')
        pd_rd = self.rd_type()
        conn = self.connDB()
        datas = pd_rd(self.data_path)
        datas.to_sql(self.tbName, con=conn, index=False)
        # datas.to_sql(self.tbName, con=conn, if_exists='replace', index=False)
        print('创建成功！')

        return conn

    def connDB(self):
        conn = sqlite3.connect(self.dbName)  # 数据库不存在则创建，存在则连接
        # conn.row_factory = sqlite3.Row  # 可以用字典形式（键值对）获取数据

        return conn


if __name__ == '__main__':
    path = input('请输入要访问的数据库路径名称(*.db)：').strip()  # 'Fake_info.db'

    sqlite = SQLite(dbName=path)
    cnn, table_name = sqlite.sqlite()
    cur = cnn.cursor()
    sql = f'SELECT * FROM {table_name}'
    results = cur.execute(sql).fetchall()
    for result in results[:10]:
        print(f"{result[0]},{result[1]},{result[2]}")
        # print(f"{result['Name']},{result['Telephone']},{result['Birth']}")  # 对应conn.row_factory = sqlite3.Row

    print("###### 以下是pandas读取的数据 ######")
    df = pd.read_sql(sql, con=cnn)  # pandas.read_sql内置游标，可以直接使用
    print(df)

    cnn.close()

'''
关于sqlite3游标问题，可以直接使用conn(隐式游标)，也可以定义显式游标c=conn.cursor()
区别在于显式游标是大多数据库执行的标准操作，移植性强。隐式游标是sqlite3内置的游标(快捷方式)，可以直接使用。
'''

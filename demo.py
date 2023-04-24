import pandas as pd
import numpy as np
import streamlit as st


class Application:
    def __init__(self):
        st.set_page_config(page_title="Detail of A-Share", layout="wide")

        self.df = pd.read_csv(
            "https://gitee.com/youngyuan1971/my_projects/raw/master/stock.csv")

        # 两种方法：
        # 1. 遍历所有列数据，将含有“-”的对应行删除
        # for col in self.df:
        #     self.df.drop(self.df[self.df[col] == '-'].index, inplace=True)
        # 2. 替换所有含“-”的数据为缺失值Nan，然后删除缺失值所在的行
        self.df.replace('-', value=np.nan, inplace=True)
        # 考虑到Nan数据不影响数据类型转换，可以不删除(本案中缺失值有用途)
        # self.df.dropna(inplace=True)

        self.df['代码'] = self.df['代码'].apply(lambda x: str(x).zfill(6))
        col_list = self.df.columns.to_list()
        self.df[col_list[2:]] = self.df[col_list[2:]].astype('float64')

    def stock_detail(self):
        option_list = ["All", "Limit up", "Limit down",
                       "Trade suspension", "Special treatment", "Delisting arrangement"]
        st.write(
            '''
                <h4 style="text-align:center">Daily market of A-Share</h4><br>
            ''', 
            unsafe_allow_html=True)
            
        userSelect = st.sidebar.selectbox("Please select:", option_list)

        if userSelect == option_list[1]:
            detail = self.df.loc[self.df.涨跌幅 >= 9.95]
        elif userSelect == option_list[2]:
            detail = self.df.loc[self.df.涨跌幅 <= -9.95]
        elif userSelect == option_list[3]:
            detail = self.df.loc[self.df.最新价.isna()]
        elif userSelect == option_list[4]:
            detail = self.df.loc[self.df.名称.str.contains("ST")]
        elif userSelect == option_list[5]:
            detail = self.df.loc[self.df.名称.str.contains("退")]
        else:
            detail = self.df

        detail.reset_index(drop=True, inplace=True)
        detail.index = detail.index+1
        st.download_button("Download data to CSV",
                           data=detail.to_csv(), file_name=f"{userSelect}.csv")

        st.write(detail)

    def stock_query(self):
        st.write("**Stock query**")
        userInput = st.sidebar.text_input(
            "Please enter the stock code or name:").strip()
        if userInput == "":
            result = self.df.loc[self.df.代码 == "000001"]
        else:
            result = self.df.loc[(self.df.代码 == userInput) | (
                self.df.名称.str.contains(userInput))]

        if result.empty:
            st.write("*The data cannot be found, please try again ......*")
        else:
            st.write(result)

    def run(self):
        self.stock_detail()
        self.stock_query()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()

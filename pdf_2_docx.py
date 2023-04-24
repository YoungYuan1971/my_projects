# -*- encoding: utf-8 -*-
'''
@File    :   pdf_2_docx.py
@Time    :   2022/08/30 16:01:59
@Author  :   YoungYuan 
@Contact :   young_yuan@hotmail.com
@License :   (C)Copyright 2022-2031, YoungYuan
'''


from pdf2docx import Converter


class PDF2DOCX:
    def __init__(self, pdf_file: str):
        self.pdf_file = pdf_file

    def pdf2docx(self):
        file_name = self.pdf_file.split(".")[0]
        docx_file = f"{file_name}.docx"
        cv = Converter(pdf_file=self.pdf_file)
        cv.convert(docx_filename=docx_file)
        cv.close()
        print(f"转换成功！文件位置： {file_name}.docx ")


if __name__ == "__main__":
    pdf_file = input("请输入PDF文件完整路径：").strip()
    app = PDF2DOCX(pdf_file)
    app.pdf2docx()

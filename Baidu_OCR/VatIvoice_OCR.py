# -*- coding: UTF-8 -*-
# @time: 2022/7/7 18:31
# @file: VatIvoice_OCR.py
# @Author: YoungYuan

import time
from aip import AipOcr
from SecretData import BAIDU_OCR
import BaiduOCR_IO


class OCR(AipOcr):
    def __init__(self, imgs):
        BAIDU = BAIDU_OCR()
        super(OCR, self).__init__(appId=BAIDU.APP_ID,
                                  apiKey=BAIDU.API_KEY, secretKey=BAIDU.SECRET_KEY)
        self.imgs = imgs

    def BaiduOcr(self):
        results = []
        for pic in self.imgs:
            print(f'正在识别{pic}......')
            try:
                with open(pic, 'rb') as fp:
                    res = self.vatInvoice(fp.read())[
                        'words_result']  # 增值税发票识别  500次/天/免费
                    # print(res)
                    results.append(self.paser_data(res))
                    time.sleep(1)
            except:
                pass

        BaiduOCR_IO.save_file('VatInvoice', results)
        print('识别完成，数据写入[VatInvoice.xlsx]文件中！')

    def paser_data(self, datas):
        CommodityName = ''
        for Commodity in datas['CommodityName']:
            CommodityName += Commodity['word']

        data_info = {
            # 发票基本信息
            '发票类型': datas['InvoiceType'],
            '发票代码': datas['InvoiceCode'],
            '发票号码': datas['InvoiceNum'],
            '开票日期': datas['InvoiceDate'],
            '校验码': datas['CheckCode'],
            '密码区': datas['Password'],
            # 价税金额
            '金额合计': datas['TotalAmount'],
            '税额合计': datas['TotalTax'],
            '价税合计(小写)': datas['AmountInFiguers'],
            '价税合计(大写)': datas['AmountInWords'],
            # 销售方信息
            '销售方名称': datas['SellerName'],
            '销售方纳税人识别号': datas['SellerRegisterNum'],
            '销售方地址电话': datas['SellerAddress'],
            '销售方开户行及账号': datas['SellerBank'],
            '收款人': datas['Payee'],
            '复核': datas['Checker'],
            '开票人': datas['Checker'],
            # 购买方信息
            '购买方名称': datas['PurchaserName'],
            '货物服务名称': CommodityName,
        }

        return data_info


def main():
    base_path = 'invoice'
    imgs = BaiduOCR_IO.find_all_img(base_path)
    app = OCR(imgs)
    app.BaiduOcr()


if __name__ == '__main__':
    main()

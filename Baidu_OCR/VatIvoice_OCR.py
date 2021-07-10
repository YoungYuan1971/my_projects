import os
from aip import AipOcr
from SecretData import BAIDU_OCR
import pandas as pd


APP_ID = BAIDU_OCR['APP_ID']
API_KEY = BAIDU_OCR['API_KEY']
SECRET_KEY = BAIDU_OCR['SECRET_KEY']
CLIENT = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def find_all_img():
    base_path = './Invoice/'
    for root, _, fs in os.walk(base_path):
        for f in fs:
            if f.endswith(('.jpeg', '.jpg', '.png')):
                yield root + f


def get_data(img):
    datas = CLIENT.vatInvoice(img)  # 增值税发票识别  500次/天/免费
    datas = datas['words_result']

    return datas


def parser_data(datas):
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
    imgs = find_all_img()
    results = []
    try:
        for img in imgs:
            with open(img, 'rb') as fp:
                print(f'正在识别{img}......')
                datas = get_data(fp.read())
                # print(datas)
                result = parser_data(datas)
                results.append(result)

        df = pd.DataFrame(results)
        df.to_excel('VatInvoice.xlsx', 'VatInvoice', index=False)
        print('识别完成，数据写入[VatInvoice.xlsx]文件中！')

    except:
        pass

    


if __name__ == '__main__':
    main()

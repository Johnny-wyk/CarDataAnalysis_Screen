# --coding:utf-8--
import requests
from lxml import etree
import csv
import os
import time
import json
import pandas as pd
import re
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','车辆大屏可视化.settings')
django.setup()
from myApp.models import carInfo

# 爬取懂车帝数据做可视化大屏
class spider(object):
    def __init__(self):
        # 定义要爬的网站地址
        # self.spiderUrl = 'https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name=%E5%B9%BF%E5%B7%9E&count=10&month=&new_energy_type=&rank_data_type=11&brand_id=&price=&manufacturer=&series_type=&nation=0'
        self.spiderUrl = pe = 'https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name=%E5%B9%BF%E5%B7%9E&count=10&month=1000&new_energy_type=&rank_data_type=11&brand_id=&price=&manufacturer=&series_type=&nation=0'
        # 应对浏览器反爬
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'

        }

    def init(self):
        # 调用os库创建csv文件，存放爬虫获取的车辆数据信息
        if not os.path.exists('./data.csv'):
            with open('./data.csv','a',newline='',encoding='utf-8') as wf:
                write = csv.writer(wf)
                write.writerow(["brand","carName","carImg","saleVolume","price",
                                "manufacturer","rank","carModel","energyType","marketTime","insure"])

    def get_page(self):
        with open('./spiderPage.txt','r') as r_f:
            return r_f.readlines()[-1].strip()

    def setPage(self,newPage):
        with open('./spiderPage.txt','a') as a_f:
            a_f.write('\n'+str(newPage))

    def main(self):
        # 主函数，获取数据
        count = self.get_page()
        parms = {
            'offset': int(count)
        }
        print("数据从{}开始爬取".format(int(count) + 1))
        pageJson = requests.get(self.spiderUrl, headers=self.headers, params=parms).json()
        pageJson = pageJson["data"]["list"]

        try:
            for index, car in enumerate(pageJson):
                carData = []
                print("正在爬取第%d" % (index + 1) + "数据")
                # 品牌名
                carData.append(car["brand_name"])
                # 车名
                carData.append(car["series_name"])
                # 图片链接
                carData.append(car["image"])
                # 销量
                carData.append(car["count"])
                # 价格
                price = []
                price.append(car["min_price"])
                price.append(car["max_price"])
                carData.append(price)
                # print((carData))
                # 厂商
                carData.append(car["sub_brand_name"])
                # 排名
                carData.append(car["rank"])
                # 车型
                carNumber = car["series_id"]
                # 因为车型不在第一个url里，获取到第二次请求的url地址
                infoHTML = requests.get("https://www.dongchedi.com/auto/params-carIds-x-%s" % carNumber,
                                        headers=self.headers)
                infoHTMLpath = etree.HTML(infoHTML.text)
                # 获取到车型那一行的div
                carModel = infoHTMLpath.xpath("//div[@data-row-anchor='jb']/div[2]/div/text()")[0]
                carData.append(carModel)
                # 能源类型
                energyType = infoHTMLpath.xpath("//div[@data-row-anchor='fuel_form']/div[2]/div/text()")[0]
                carData.append(energyType)
                # 上市时间
                marketTime = infoHTMLpath.xpath("//div[@data-row-anchor='market_time']/div[2]/div/text()")[0]
                carData.append(marketTime)
                # 保修期限
                insure = infoHTMLpath.xpath("//div[@data-row-anchor='period']/div[2]/div/text()")[0]
                carData.append(insure)
                print(carData)
                self.save_to_csv(carData)
        except:
            pass

        # print(pageJson)
        self.setPage(int(count)+10)
        self.main()

    def save_to_csv(self, resultData):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(resultData)

    def clear_csv(self):
        df = pd.read_csv('./temp.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        print("总数量为%d" % df.shape[0])
        return df.values

    def save_to_sql(self):
        data=self.clear_csv()
        for car in data:
            carInfo.objects.create(
                brand = car[0],
                carName = car[1],
                carImg=car[2],
                saleVolume=car[3],
                price=car[4],
                manufacturer=car[5],
                rank=car[6],
                carModel=car[7],
                energyType=car[8],
                marketTime=car[9],
                insure=car[10],
            )

if __name__ == '__main__':
    spiderObj = spider()
    # spiderObj.init()
    # spiderObj.main()
    spiderObj.save_to_sql()
from pymongo import MongoClient
import tushare
import json
import requests
from fake_useragent import UserAgent
import datetime

class IwencaiNewHigh:

    def __init__(self):
        self.db=MongoClient()['wencai']

    def get_trade_date(self):
        # tushare.set_token('8b8f77e8abc8396a88d99ee51fd76a602fbe8fb3c0eae86c6561e3d7')
        # pro = tushare.pro_api()
        # df = pro.trade_cal(exchange='', start_date='20200727', end_date='20200907', is_open='1')
        # date = df['cal_date'].to_list()
        day = datetime.datetime.now()
        date = [day.strftime('%Y%m%d')]
        return date

    def get_data(self, question):
        self.headers = {
            'Host': 'www.iwencai.com',
            'Origin': 'http://www.iwencai.com',
            'Referer': 'http://www.iwencai.com/unifiedwap/result?w=%s&querytype=&issugs' % question,
            'User-Agent': UserAgent(path='D://fake_useragent.json').random,
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'zh - CN, zh;q = 0.9, ja;q = 0.8, ko;q = 0.7'
        }
        self.post_url = 'http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick'
        self.data_temp = {
            'question': question,
            'secondary_intent': 'stock',
            'perpage': 4000,
            'page': 1, }
        self.cookies = {'chat_bot_session_id': '469324f4d5b911bf9c05def3ee800dab',
                        ' PHPSESSID': 'b50a91cc70dc14f137a78b8f2db9282d',
                        ' cid': 'b50a91cc70dc14f137a78b8f2db9282d1582445631',
                        ' ComputerID': 'b50a91cc70dc14f137a78b8f2db9282d1582445631', ' guideState': '1',
                        ' other_uid': 'Ths_iwencai_Xuangu_087b043c9b7bf78a61804a7bd7b5b912',
                        ' user': 'MDptb18yMTEzMTY4NzI6Ok5vbmU6NTAwOjIyMTMxNjg3Mjo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6MjQ6OjoyMTEzMTY4NzI6MTU4Mjg3Mzc2Mjo6OjE0MjAxNjk1MjA6ODY0MDA6MDoxYjE0ZWNiNjg1ZmNkODMzZWFhNGFmOGZlYTc1NDE1NjI6ZGVmYXVsdF80OjE%3D',
                        ' userid': '211316872', ' u_name': 'mo_211316872', ' escapename': 'mo_211316872',
                        ' ticket': '595ce825965bcf62ce6b927820fe9aae',
                        ' v': 'Ap7K_6bJTJHijJj1t6SQFYZh6T_gX2La9CAW-EgnCiDdZzHlsO-y6cSzZsQb'}
        response = requests.post(self.post_url, data=self.data_temp, headers=self.headers, cookies=self.cookies)
        resp = response.content.decode(encoding="utf-8", errors="replace")
        return json.loads(resp)

    def save_to_mongo(self, data_list, date,collection):
        item={'新高数量':data_list['analyze_data']['code_count']}
        item['trade_date']=date
        item['新高个股']=data_list['data']
        collection.insert_one(item)


    def run(self):
        period=input('输入查询60日新高或者新低(新高/新低)：')
        col_name='high' if period=='新高' else 'low'
        collection=self.db['new{}60'.format(col_name)]
        trade_date = self.get_trade_date()
        for i in trade_date:
            i_format = '%s年%s月%s日' % (i[0:4], i[4:6], i[6:8])
            question_str = i_format + '收盘价创60日{}'.format(period)
            print(question_str)
            question = question_str.encode('utf-8')
            block_data = self.get_data(question)['data']
            self.save_to_mongo(block_data, i,collection)
            print('{}的数据已写入数据库'.format(i))


if __name__ == '__main__':
    newhigh=IwencaiNewHigh()
    newhigh.run()

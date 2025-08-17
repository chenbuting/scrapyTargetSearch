import requests
from datetime import datetime

class EbidSinochemitcCrawler:
    def __init__(self, keyword="电缆", days=3):
        self.keyword = keyword
        self.days = days
        self.source = "中华商务电子招标平台"
        self.api_url = "https://ebid.sinochemitc.com/api/truelore-business-support/noauth/trans/trade/pageEs"
        self.systimeapi_url = "https://ebid.sinochemitc.com/api/truelore-business-support/noauth/time/systemTime"
    
    def fetch(self):
        headers = {
            'access-control-allow-origin':'https://ebid.sinochemitc.com',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Origin': 'https://ebid.sinochemitc.com',
            'Referer': 'https://ebid.sinochemitc.com/web-portal/'
        }

        # 获取当前时间api
        systemtime_response = requests.get(self.systimeapi_url, headers=headers)
        systemtimeJson = systemtime_response.json()

        if systemtimeJson['success']:
            systemtime = systemtimeJson['data']  # 获取系统时间

            # 将系统时间作为 releaseEndTime 和 releaseStartTime
            release_end_time = systemtime
            release_start_time = systemtime - 86400000 * self.days  # 假设是过去 `days` 天的时间

            form_data = {
                "businessName": self.keyword,
                "noticeType": 1,
                "pageNum": 1,
                "pageSize": 12,
                "purchaseMode": "1184173458458267648,1184173458655399936",
                "purchasePatternId": "",
                "purchaseProjectType": "",
                "releaseEndTime": release_end_time,
                "releaseStartTime": release_start_time,
                "tradePattern": "1184173458290495489",
            }

            try:
                print("开始请求API...")

                # 发送请求
                response = requests.post(self.api_url, json=form_data, headers=headers)
                # print("响应内容:", response.text)
                response.raise_for_status()  # 检查请求是否成功
                json_data = response.json()  # 获取JSON数据
                # print('----------', json_data)  # 打印完整返回数据以便调试

                results = []
                if 'data' in json_data and 'list' in json_data['data']:
                    for item in json_data['data']['list']:
                        # 解析时间并转换为日期格式
                        pub_date = datetime.utcfromtimestamp(item['releaseTime'] / 1000)
                        bid_end_date = datetime.utcfromtimestamp(item['bidEndTime'] / 1000)

                        # 收集数据
                        results.append({
                            "标题": item['businessName'],
                            "发布日期": pub_date.strftime("%Y-%m-%d %H:%M:%S"),
                            # "投标截止日期": bid_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                            "地区": "",
                            "采购单位": item['tendererName'],
                            "URL": f"https://www.cdt-ec.com/notice/moreController/xjdhtml?id={item['id']}",
                            "来源": self.source
                        })
                return results
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")  # 请求错误
                return []
            except ValueError as e:
                print(f"解析JSON时出错: {e}")  # JSON解析错误
                return []
        else:
            print(f"获取系统时间失败: {systemtimeJson['errMessage']}")
            return []

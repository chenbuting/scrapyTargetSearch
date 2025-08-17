import requests
from datetime import datetime

class ecChngCrawler:
    def __init__(self, keyword="电缆", days=3):
        self.keyword = keyword
        self.days = days
        self.source = "中国华能新版"
        self.api_url = "https://ec.chng.com.cn/scm-uiaoauth-web/s/business/uiaouth/queryAnnouncementByTitle?kbfJdf1e=JQFYxalqEqmhR4xtcp.F2wO3vq5.Qg.bZRNmaAQXRQQ5TWSIGs7BEoYx1aDlOBl5QA_em8ORUYwRsbBsBro98karqhQ6ggCC"
        self.session = requests.Session()  # 使用 Session 来保存 Cookie 和会话信息


    def fetch(self):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Origin': 'https://ec.chng.com.cn',
            'host':'ec.chng.com.cn'
        }

        # 获取当前时间api
        # systemtime_response = requests.get(self.systimeapi_url, headers=headers)
        # systemtimeJson = systemtime_response.json()


        # 将系统时间作为 releaseEndTime 和 releaseStartTime
        # release_end_time = systemtime
        # release_start_time = systemtime - 86400000 * self.days  # 假设是过去 `days` 天的时间

        cookies = {
            'cookie': 'S6J51OuUjLieO=50.E5g8LIjSx7ApRPoOsLDL7svUk0bgaYXf2MKzhMN7cXWqUM4bLTzpH7rnPaERvLCGLbl8XDZufJRGf32L6Oxa; S6J51OuUjLieP=AzDOk8MsfTgQSNmS7UIX2z5VSSmv6NJpuJcSvWsI2TN19Q7qbxDxQPfgLsE4B0_uMEXspTL9vcx90V1fwTJqaUMZiT5nxZn5P1qw981omo4qLFwkLjOI7SBKVQnfpinDTIdxz8RddAwLJi5wCIvCfLCxd.WC820rf35wvk8io1rFiP_aCrIsCEbb8NRnotEZB9vzDNbqy_46S.SDz5xID8ehD8Ki26NQOkpX4jH2HOS2bt9.kf0IDKiAV4335lyCB6QdB.O3T5ZfdoD6elJ5rGsYbsnXN7c4i9YtNtORVzvzHLhdhBNzbe81UaRcpZerHi2qDyntn0JyQnCUxdz5gMMyhz8SlMa74_iqUdiv31gBWi_zoYVsC3bHsgvDxMb3AlhUcxHCK5y2IFYo1PlrlwobTp84n.uNJu4r9GGcy8E',
        }

        form_data = {
            "search": self.keyword,
            "ifend": "in",
            "type": "107",
        }

        try:
            print("开始请求API...")

            # 发送请求
            response = self.session.post(self.api_url, json=form_data, headers=headers)
            print("响应内容:", response.text)
            response.raise_for_status()  # 检查请求是否成功
            json_data = response.json()  # 获取JSON数据
            print('----------', json_data)  # 打印完整返回数据以便调试

            results = []
            if 'data' in json_data and 'list' in json_data['root']:
                for item in json_data['root']:
                    # 解析时间并转换为日期格式
                    pub_date = datetime.utcfromtimestamp(item['createtime'] / 1000)
                    print("pub_date",pub_date)
                    bid_end_date = datetime.utcfromtimestamp(item['activetime'] / 1000)
                    print("bid_end_date",bid_end_date)
                    # 收集数据
                    results.append({
                        "标题": item['announcementTitle'],
                        "发布日期": pub_date.strftime("%Y-%m-%d %H:%M:%S"),
                        # "投标截止日期": bid_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "地区": "",
                        "采购单位": "",
                        "URL": f"https://ec.chng.com.cn/channel/home/#/detail?id={item['announcementId']}",
                        "来源": self.source
                    })
            print(results)
            return results
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")  # 请求错误
            return []
        except ValueError as e:
            print(f"解析JSON时出错: {e}")  # JSON解析错误
            return []

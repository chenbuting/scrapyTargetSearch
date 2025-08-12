import requests
from datetime import datetime, timedelta

class CdtEcCrawler:
    def __init__(self, keyword="电缆", days=3):
        self.keyword = keyword
        self.days = days
        self.source = "中国大唐集团有限公司"
        self.api_url = "https://www.cdt-ec.com/notice/moreController/getList"
        self.session = requests.Session()  # 使用 Session 来保存 Cookie 和会话信息

    def fetch(self):
        today = datetime.now()
        start_date = today - timedelta(days=self.days)
        date_format = "%Y-%m-%d %H:%M:%S"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Origin': 'https://chinasalt.china-tender.com.cn',
            'Referer': 'https://chinasalt.china-tender.com.cn/zbcg/moreinfo.html'
        }

        cookies = {
            'cookie': 'JSESSIONID=CE4A1A171AE94A2E594738A2C12661BB; acw_tc=1a0c651517549668009893808e48bfd15d0331e71dd6f88d0b61f55e880fa4; acw_sc__v2=689aab11d4e9e6b129449afc8f4beb06d2727c11; ssxmod_itna=eqx=qIxRrNYjh4Cq7jbh4eLFDzxUqAjQGgDYq7=GFDmx0PeyxD7QMKmDfEix0IzDBQq2j+y8CqDsqRcxGzDiTPGhDBW5aPezLvmOg7t7odo3KCmcjpuett50m3RhYE8crbXU=/Mu3QLqNDB3DbqDyiGpDMDGGf4GwDGoD34DiDDPDbRiDAdeD7qDFfCTNVlbDm4GWfeDmDGA3seDgCDDBG+i3YERzY4uODDX+335u7hcHoC9iAGTezpG3x0tbDBLCjzI36ZSjvOnHhIDaTSrDzMCDtMuiYci3Cxubxact7EGm0XqDOxAMT44iGe72t/w4Sv4YRi3q4/540TNKixlaTtq4UxVSDDGSKuBQ3BzDSDZAqAk16M12LqVT4ST=gYoUeiqmPZBdxEQx4iB75/A5QDY=BQKu5PGGgiroWDD; ssxmod_itna2=eqx=qIxRrNYjh4Cq7jbh4eLFDzxUqAjQGgDYq7=GFDmx0PeyxD7QMKmDfEix0IzDBQq2j+y8nxDWy7EATXCYDj40Cum+GYLODBLaNFb5mTfaFVlzI8N2P72=hWan0+DzBx750ahW9OhTf0Ro5UU3Qe9dXLRr4UI8tj3DU4mkQjS+PGmu=ZBfGPmL5oU4vzWGbg9QrqPTjTsjraLmIuIOXgIhjLiB6gRfQjlpW2I+YX3i42WKiaiG6xF1ba9WPR76PginUEB=uEfjHU7oXayT9dPvUL3DYXtakIdjp9pTxz2aulAtXIOov0Gv9cqBAGEQD=oYWcdAoejWY4eIGl076QQ2pzW3NxXgC=4/NdhAQ2ojGf0A+0ZIT9NyP54YQBiIBYUxxuYp5zltj7TS7QshiHoUFjYopIfhY5c+Tz=yp=z=NYhTCBP40IYgKXmp=2LIKhLeEwhRZPUEPILi3moPzgdu4uXtY4/caOvZZb2ZcVlIX9XB8o2QhFPoGBtpO=xpwA=tFWB4C=aUPgB73rWcceEn5eQoPjExeUupvlttYOQSF7G4YFDocGGFzWe65cn4zryS+gEOcz85W95WSoaYh/exsyEPuT9DOjP0WKA+LUdH5fFjdb=d9QH+O93i394twW1/SntkXjoegL31pzAMTUlzT1hFEzwqGlmtMe+jjAly/nwSVAlGwld4Sqn+tAxP02SqGYwzwHRDOKdMsIm4mCSwqiOFjeLxEiE04giSfWmGaxQFKyDQGwVde2+rW4m0LDYmD0OKFPb2oIh47Y3mkxYWGWutm2UYx8oGQ58oFOK7hoOKGrBi1DbFhDlr10i94BDYm0eBehwU7K/htBslRkAqU2ki5BhsGx92qAqIhcjqRx0CDeD',
        }

        form_data = {
            "page": 1,
            "limit": 10,
            "messagetype": 4,
            "pro_bidding_mothod": 0,
            "message_title": self.keyword,
            "purchase_unit": "",
            "purchase_unit_agent": "",
            "message_no": "",
            "purchase_code": "",
            "startDate": "",  # 起始日期
            "endDate": "",  # 截止日期
            "purchase_type": 0,
        }

        try:
            # 使用 Session 对象发送请求
            response = self.session.post(self.api_url, data=form_data, headers=headers,cookies=cookies)
            response.raise_for_status()  # 检查请求是否成功
            print("Response content:", response.text)
            json_data = response.json()  # 获取JSON数据

            results = []
            if 'data' in json_data:
                for item in json_data['data']:
                    # 解析时间并比较
                    pub_date = datetime.strptime(item['publish_time'], date_format)
                    if start_date <= pub_date <= today:  # 检查公告时间是否在日期范围内
                        results.append({
                            "标题": item['message_title'],
                            "发布日期": item['publish_time'],
                            "地区": "",
                            "采购单位": "",
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

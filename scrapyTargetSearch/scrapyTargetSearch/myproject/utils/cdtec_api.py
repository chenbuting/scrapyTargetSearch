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
            'cookie': 'JSESSIONID=CE4A1A171AE94A2E594738A2C12661BB; acw_tc=1a0c652317549686851692254e1b854e1eade380ebebf8493dec02fa60798a; acw_sc__v2=689ab26e999542eb121599520b40cb762e7ced17; ssxmod_itna=eqx=qIxRrNYjh4Cq7jbh4eLFDzxUqAjQGgDYq7=GFDmx0PeyxD7QMKmDfEix0IzDBQq2j+1WG70=Dl=YH5DSxD=aDK4GT1WaiB6zbIpugGIjmAiOeFu8tT7gCDHfY5+pjOLtXMl3FyUGOS0qDU4GnD0=e7O0tDYALDBYD74G+DDeDixGmieDS4xD9DGpdMeniueDEDYpdxDoDYSRYxit5DDtEQm4bUj5+nCKD0LA+Rx=FC=FqL=e3leh7oBbDjweD/35jvgbCuzMO3=FEoGcp+eGyb5Gu4=eTrm4HnlWrO6qF37oZMiiFDb/F44iGe72t4m4/5b3bxrbDT+sS2D3D0z+bRxwW+GDDWy7KEroLOiqA51i16M12kz1YGbGsjo5dgp4fGjA5hoYvOijY=SG5ZGxSDG3AqYu5P0GOnsgTx4D; ssxmod_itna2=eqx=qIxRrNYjh4Cq7jbh4eLFDzxUqAjQGgDYq7=GFDmx0PeyxD7QMKmDfEix0IzDBQq2j+1WG7i5Di1wp+tDdnq03ao9k5iGDBqrifPR=G8UOoR26cTffUiPx4coIcFxlxfO2f=OejnL=/BOtffk3URh3oGLDU7E34Gq0ZASUmbm3G8mdRBwYX7r2FIOTCKDYgWhKKkGfvWqhCiA2S/bXz3BczUe0FA8DPZhLf8gRlYTPKVdT1Otb8OIjppwjzaTrP2eQpHmPeClvMWKh=XDEtowIR3+LS/Z+D6craf8isoGNaQa4FAvpSjo02PGAXqDQWhDoWAqpIFidCG5cADcgNoUf4idr1jglvH2IBAIEDQDzr1lf=oxapQ8omQc6Brdae6zYR/WIaKoVnPo==1Qw5pw+hfgZYoQUGAYYxncjEaxvaIqvS5SgqGELQtv2gj8F5kxnx0vcPRYUQ5PvHgvln+mg5Iz3x1pUjKqf68tuhUQsEXAxnS0v2BPGOLPIm0Co5=bE4vn0I20BtZ36gdKhfoPAxCPDavY/QBAg5ZHxSAYf=g0w9e6UDm94Sw9Kvovzn3BDnCAYood+2gNxW2Q7YvG0WK3aKARPjzlMlEl04xzl0ttdd6Q3YFWOmBiCn3k69YDrh5RaamReMgALCMykbGTqjdu4R7dD10sPbByK6xnEKIU05kovMBVB4EL9B4Kr/SGz7DBhki1Iho7bFU1ATB6YYQ+ALqab5bR4NDKoLF5CiGSx2b43DYxiSoo7egqTm4cea3Q3PBi4z0=eY+247KMvHmYDjOik9+4i4FAnM5uIWQGQrOmNePCneo=RD52fOD0iGt7Knr1MQD4PBkmwbxj353jTmftxTfb5OKWEuQoNTmoxC5101DAtr3bvfxOlLsAqCU/lKSGTWo0h1057D10gG+ODdMDoAqRhkiDD',
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
            # print("Response content:", response.text)
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

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
            'cookie': 'JSESSIONID=A1C47A40057EC793194AB24B4CBC082F; yzw-auac-token=175e2fd5-452c-4c6a-9cba-c45ipudatang; acw_tc=1a0c639817554204839313197e14f67800c30e769d11db8a9596860690879a; acw_sc__v2=68a1974374cd0608bd22c32573480ac67dc1fc5d; ssxmod_itna=eqx=qIxRrNYjh4Cq7jbh4eLFDzxUqAjQGgDYq7=GFDmx0PeyxD7QMKmDfoVDD5m4Djhawtj7gODD/KmLqDZDGI3Dqx0Etf3nk96GbIpLgRxjmA70=PjI2CKHIq4+iE+Cnkyt4ky0yLsI4S4htDB3DbqDyiGptlDGGj4GwDGoD34DiDDPDb3rDAdeD7qDF0nuiPaTDm4GW0eDmDGYQpeDgCDDB+Si3YxugIOuODDXOttQn7gaONn9iABTempDQx0tbDBLCRFBCcIMOQa9EoAapmeGyb5Gue=mTTm4H9ecrkcA4W4EtS+pzQ+biD4mDdBhGWGVWD4tKxHYDr0z4RDe44Cb83u=SH5DDWy7KEEr1gDxEqfL1XdzuLqDW4ML=gioUCiPQYhoYZBQyY5De5MADjOd5Y41Y5QYYPAGgimKrx4D; ssxmod_itna2=eqx=qIxRrNYjh4Cq7jbh4eLFDzxUqAjQGgDYq7=GFDmx0PeyxD7QMKmDfoVDD5m4Djhawtj7gxDW1iDW++z1S2b4Ga8FB30sjD0v3exLtYv9XYfRf8xovLtMfHaqRIPhCF0MOUc/e2NqtFKBfx/4EnYlUX/dNDaodCBT6Z8SdL3qxqvM64V8XgjqxyGC6OS+0QZ+iooThUWd54MEGU44nxeqh97oY2IqALf1GzGq7PKkIlYdYKLfP/YMgkXScxWwpGuE510kXQuELjewG=TDte9o=OOe=eiX9gGdH/lTaKOp0q/jfMaEjYrDv=XOWdne3NxfxOK5c4ygpMlQEEo7OQm6AgYhXpIIAG0P34IET=54WPoAAroX2gtuhQLir8ljz20vpPUcPwEXzBjjmwI2EYlYL04VoxclN4Pmn=j2CpNbYBWDgWK0AL9Yxo7Q=40OQwzlT8YKPAATEEfemHI69DomaavzAwz2WbNPh5cGU=1mtOEQIKN=5cmFKaK5h2eQU4ii0IBmh6L1fP/N1ovChLZeeEtqRDdfxKEzFYR6vxmDKUVex4twcbN16EjAvaTcLoju7p/KIXAnv12Bp6I+2HVAM/AOVNhkQMiOiELW/LQ=Ho9XTxcflcU0DOKaqPFo9m20wBpDFPK8TbnADyxFBWI1if3rgCtOWo2ykdO/lqorgRNDVyjDKuY19=xOrYKMB+44wYxnxABKG6A8KiwxOHRxADaIpjRWiw3jqSGO0qxrRY30h1Yu3D8hDWDilq5Gk0qPD',
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

import requests
from datetime import datetime, timedelta

class ChinaSaltCrawler:
    def __init__(self, keyword="电缆", days=3):
        self.keyword = keyword
        self.days = days
        self.source = "中盐采购平台"
        self.api_url = "https://chinasalt.china-tender.com.cn/ewbfront-zs/rest/secaction/getSecInfoListYzm"

    def fetch(self):
        today = datetime.now()
        start_date = today - timedelta(days=self.days)
        date_format = "%Y-%m-%d"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0',
            'Origin': 'https://chinasalt.china-tender.com.cn',
            'Referer': 'https://chinasalt.china-tender.com.cn/zbcg/moreinfo.html'
        }

        form_data = {
            'pageSize': '10',
            'pageIndex': '0',
            'content': self.keyword,
            'siteGuid': '7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
            'categoryNum': '002',
            'endDate': '',
            'startdate': '',
            'status': 'YZM',
            'ImgGuid': ''
        }

        response = requests.post(self.api_url, data=form_data, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        results = []
        if 'custom' in json_data and 'infodata' in json_data['custom']:
            for item in json_data['custom']['infodata']:
                pub_date = datetime.strptime(item['infodate'], date_format)
                if start_date.date() <= pub_date.date() <= today.date():
                    results.append({
                        "标题": item['realtitle'],
                        "发布日期": item['infodate'],
                        "地区": "",
                        "采购单位": "",
                        "URL": f"https://chinasalt.china-tender.com.cn{item['infourl']}",
                        "来源": self.source
                    })
        return results

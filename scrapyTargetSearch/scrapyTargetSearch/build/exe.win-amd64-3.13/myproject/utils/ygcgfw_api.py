import requests
from datetime import datetime, timedelta

class YgcgfwApiCrawlerV2:
    def __init__(self, keyword="电缆", days=3):
        self.keyword = keyword
        self.days = days
        self.source = "阳光采购网"
        self.api_url = "http://www.ygcgfw.com/inteligentsearchnew/rest/esinteligentsearch/getFullTextDataNew"
        self.base_url = "http://www.ygcgfw.com"

    def fetch(self):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        today = datetime.now()
        cutoff = today - timedelta(days=self.days)

        payload = {
            "token": "",
            "pn": 0,
            "rn": 100,
            "wd": self.keyword,
            "fields": "title",
            "cnum": "004",
            "sort": "{\"webdate\":0}",
            "ssort": "title",
            "cl": 500,
            "condition": [
                {
                    "fieldName": "categorynum",
                    "equal": "001",
                    "isLike": True,
                    "likeType": "2"
                }
            ],
            "highlights": "title"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"[{self.source}] 请求失败: {e}")
            return []

        results = []
        records = data.get("records") or data.get("result", {}).get("records", [])

        for record in records:
            date_str = record.get("webdate", "")[:10]
            try:
                pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                if pub_date < cutoff:
                    continue
            except:
                continue

            title_raw = record.get("title", "").replace("<em style='color:red'>", "").replace("</em>", "")
            url_path = record.get("linkurl", "")
            full_url = self.base_url + url_path if url_path else ""

            results.append({
                "标题": title_raw.strip(),
                "发布日期": date_str,
                "地区": record.get("zhuanzai", ""),
                "采购单位": record.get("organizationname", ""),
                "URL": full_url,
                "来源": self.source
            })

        return results

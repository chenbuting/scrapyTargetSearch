from lxml import html
import requests
from urllib.parse import urljoin
from datetime import datetime, timedelta

class JingCaiZongHengCrawler:
    def __init__(self, keyword="电缆", days=3):
        self.keyword = keyword
        self.days = days
        self.source = "精彩纵横"
        base_url = "https://www.yingcaicheng.com/notice/search"
        params = {
            'searchWord': '电缆',
        }
        self.target_url = base_url + "?" + "&".join(f"{k}={v}" for k, v in params.items())

    def fetch_html(self):
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(self.target_url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        return response.text

    def parse(self, html_content):
        tree = html.fromstring(html_content)
        card_list = tree.xpath('//div[contains(@class, "project-card")]')
        today = datetime.now()
        valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))

        results = []
        for card in card_list:
            # 提取标题
            title_list = card.xpath('.//a[@title]/@title')
            # print(title_list)
            href_list = card.xpath('.//a[@title]/@href')
            pub_date_list = card.xpath('.//span[contains(text(), "发布日期")]/span/text()')
            # print(pub_date_list)
            region_list = card.xpath('.//span[contains(text(), "地区")]/span/text()')
            # print(region_list)
            agency_list = card.xpath('.//span[contains(text(), "代理机构")]/span/text()')
            # print(agency_list)
            if not title_list or not pub_date_list:
                continue

            pub_date = pub_date_list[0].strip()
            if pub_date not in valid_dates:
                continue

            title = title_list[0].strip()
            href = href_list[0] if href_list else ""
            full_url = urljoin("https://www.yingcaicheng.com", href)

            results.append({
                "标题": title,
                "发布日期": pub_date,
                "地区": region_list[0].strip() if region_list else "",
                "采购单位": agency_list[0].strip() if agency_list else "",
                "URL": full_url,
                "来源": self.source
            })

        return results


    def fetch(self):
        html_content = self.fetch_html()
        return self.parse(html_content)

# 使用示例
if __name__ == "__main__":
    crawler = JingCaiZongHengCrawler()
    results = crawler.fetch()
    for r in results:
        print(r)

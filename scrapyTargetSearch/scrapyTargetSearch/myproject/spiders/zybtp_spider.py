import scrapy
import re
from urllib.parse import urljoin
from datetime import datetime, timedelta

class ZybtpSpider(scrapy.Spider):
    name = "zybtp"
    allowed_domains = ["www.zybtp.com"]
    source = "中原招采"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://www.zybtp.com/search.jspx"
        self.start_url = f"{self.base_url}?rangedatabase=title&q={keyword}"
        today = datetime.now()
        self.valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))
        # 确保 all_results 是一个列表
        self.all_results = all_results if all_results is not None else []

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_url,
            callback=self.parse,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        # print("Request sent to:", self.start_url)

    def parse(self, response):
        li_list = response.xpath('//div[@class="List2 Top10 PaddingLR15"]//ul/li')
        for li in li_list:
            title = li.xpath('.//a/@title').get()
            # print("====",title)
            # pub_date = li.xpath('.//span[@class="Gray fr"]/text()').get()

            pub_date_s = li.xpath('.//span[@class="Gray fr"]/text()').get()
            pub_date = re.search(r'(\d{4}-\d{2}-\d{2})', pub_date_s).group()

            # print("====",pub_date)
            href = li.xpath('.//a/@href').get()

            if not title or not pub_date:
                continue

            pub_date_str = pub_date.strip()
            if pub_date_str not in self.valid_dates:
                continue

            full_url = urljoin(self.base_url, href) if href else ""
            item = {
                "标题": title.strip(),
                "发布日期": pub_date_str,
                "地区": "",
                "采购单位": "",
                "URL": full_url,
                "来源": self.source
            }

            # print(item)
            # 将抓取到的数据存储到 all_results 中
            self.all_results.append(item)

            yield item

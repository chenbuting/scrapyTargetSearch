import scrapy
from urllib.parse import urljoin
from datetime import datetime, timedelta

class CncecycSpider(scrapy.Spider):
    name = "cncecyc"
    allowed_domains = ["bid.cncecyc.com"]
    source = "中国化学电子招标投标交易平台"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://bid.cncecyc.com/cms/search.htm"
        self.start_url = f"{self.base_url}?kwd={keyword}&channelIds=221%2C222%2C223%2C224%2C225%2C226%2C227%2C228%2C229%2C230%2C231%2C232%2C233%2C237%2C238%2C239%2C240%2C241%2C242"
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
        li_list = response.xpath('//ul[@id="list1"]/li')
        for li in li_list:
            title = li.xpath('.//a/@title').get()
            # print("====",title)
            pub_date = li.xpath('.//span[last()]/text()').get()
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

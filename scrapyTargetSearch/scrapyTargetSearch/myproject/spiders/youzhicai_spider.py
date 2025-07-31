import scrapy
from urllib.parse import urljoin
from datetime import datetime, timedelta

class PowerChinaSpider(scrapy.Spider):
    name = "youzhicai"
    allowed_domains = ["youzhicai.com"]
    source = "优质采"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://www.youzhicai.com/s/0_0_0_0_.html"
        self.start_url = f"{self.base_url}?key={keyword}"
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

    def parse(self, response):
        li_list = response.xpath('//ul[@class="projects-list"]/li[@class="project-li clearfix"]')
        for li in li_list:
            title = li.xpath('.//a/@title').get()
            # print("====",title)
            pub_date = li.xpath('.//span[@class="pub-value0"]/text()').get()
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

            print(item)
            # 将抓取到的数据存储到 all_results 中
            self.all_results.append(item)

            yield item

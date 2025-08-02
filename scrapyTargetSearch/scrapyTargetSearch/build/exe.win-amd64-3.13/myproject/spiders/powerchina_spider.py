import scrapy
from urllib.parse import urljoin
from datetime import datetime, timedelta

class PowerChinaSpider(scrapy.Spider):
    name = "powerchina"
    allowed_domains = ["ec.powerchina.cn"]
    source = "中国电建"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://ec.powerchina.cn/zgdjcms/category/bulletinList.html"
        self.start_url = f"{self.base_url}?word={keyword}&categoryId=2&purType=物资类"
        today = datetime.now()
        self.valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))
        self.all_results = all_results  # 将外部传入的 all_results 保存在爬虫实例中

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_url,
            callback=self.parse,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

    def parse(self, response):
        li_list = response.xpath('//ul[@id="bulletinList"]/li')
        for li in li_list:
            title = li.xpath('.//a/@title').get()
            pub_date = li.xpath('.//div[@class="newsDate"]/div/text()').get()
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

            # 将抓取到的数据存储到 all_results 中
            self.all_results.append(item)

            yield item

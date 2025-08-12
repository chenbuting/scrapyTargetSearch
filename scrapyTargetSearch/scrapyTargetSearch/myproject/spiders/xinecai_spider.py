import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from datetime import datetime, timedelta


class XinCaiSpider(scrapy.Spider):
    name = "xincai"
    allowed_domains = ['www.xinecai.com']
    source = "信e采（安天智采）"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://www.xinecai.com/bidding"
        self.start_url=f"{self.base_url}?title={keyword}"
        today = datetime.now()
        self.valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))
        self.all_results = all_results  # 将外部传入的 all_results 保存在爬虫实例中
        # 如果外部没传入 all_results，自己初始化成空列表
        if all_results is None:
            self.all_results = []
        else:
            self.all_results = all_results

    def start_requests(self):
        # cookies = {
        #     "Cookie": "Hm_lvt_3de3de274245e7cf84e90b616331fc3f=1754627794,1754790069,1754871752,1754958219; HMACCOUNT=317DDC2BC9E60037; Hm_lpvt_3de3de274245e7cf84e90b616331fc3f=1754969881"
        # }

        yield scrapy.Request(
            url=self.start_url,
            callback=self.parse,
            # cookies=cookies,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )

    def parse(self, response):
        print("---------",response.text)
        li_list=response.xpath("//div[@class='public-list']//ul[@class='public-list-cot']//li[@class='js-li-item']")
        print("-----------",li_list.get())
        print(f"共找到 {len(li_list)} 条招标信息")
        for li in li_list:
            title=li.xpath(".//h5/a/text()").get().strip()
            print("==========",title)
            pub_date = li.xpath('.//span/text()').get()
            href = li.xpath(".//h5[@class='public-list-cotit']/a/@href").get()
            if not href:
                continue
                
            full_url = urljoin(self.base_url, href)
            print("name:",title)
            print("href:",href)

            if not title or not pub_date:
                continue

            pub_date_str = pub_date.strip()
            if pub_date_str not in self.valid_dates:
                continue

            # 构造输出的 item
            item = {
                "标题": title,
                "发布日期": pub_date,
                "地区": "",
                "采购单位": "",
                "URL": full_url,
                "来源": self.source
            }

            print(item)  # 打印提取的数据
            self.all_results.append(item)
            yield item
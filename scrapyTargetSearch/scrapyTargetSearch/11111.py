import scrapy
import json
from urllib.parse import urlencode
from datetime import datetime, timedelta

class HuaRunSpider(scrapy.Spider):
    name = "huarun"
    allowed_domains = ['szecp.com.cn']
    source = "华润守正"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://www.szecp.com.cn/rcms-external-rest/content/getSZExtData"
        today = datetime.now()
        self.valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))
        self.all_results = all_results  # 将外部传入的 all_results 保存在爬虫实例中

    def start_requests(self):
        # 定义请求的参数
        payload = {
            'channelIds': '26915',
            'pageNo': '1',
            'pageSize': '10',
            'title': '电缆',
            'words': '{}'
        }

        # 使用 urlencode 将字典转换为查询字符串
        query_string = urlencode(payload)

        # 组合 URL 和查询字符串
        url = f"{self.base_url}?{query_string}"

        # 发起 GET 请求
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(f"Response text: {response.text}")
        # 打印返回的 JSON 数据
        json_data = json.loads(response.text)

        # 提取 'data' 键的内容
        data = json_data.get('data', {}).get('data', [])

        # print(f"Data: {data}")  # 输出数据

        # 遍历数据并提取需要的信息
        for item in data:
            title = item.get('title', 'No title') 
            pageLink = item.get('pageLink', 'No pageLink')  
            full_url = item.get('url', 'No url') 
            pub_date_str=item.get("registerDeadline","null")

            item = {
                "标题": title,
                "发布日期": pub_date_str,
                "地区": "",
                "采购单位": "",
                "URL": full_url,
                "来源": self.source
            }
            # 将抓取到的数据存储到 all_results 中
            print(item)
            self.all_results.append(item)

            yield item
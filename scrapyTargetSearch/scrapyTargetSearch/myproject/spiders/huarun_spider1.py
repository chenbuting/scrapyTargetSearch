import scrapy
import json
from datetime import datetime, timedelta

class HuaRunSpider1(scrapy.Spider):
    name = "huarun1"
    allowed_domains = ["szecp.com.cn"]
    source = "华润"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.start_urls = ["https://www.szecp.com.cn/rcms-external-rest/content/getSZExtData"]
        today = datetime.now()
        self.valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))
        
        # 确保传递了 all_results 参数
        self.all_results = all_results if all_results is not None else []  # 默认创建一个空列表

    def start_requests(self):
        # 定义请求的参数
        params = {
            "channelIds": "26915",
            "pageNo": "1",
            "pageSize": "10",
            "title": self.keyword,  # 动态传入的搜索关键词
            "words": "{}"  # 空的JSON对象
        }

        # 定义请求头
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            'Accept': '*/*',
            'Host': 'www.szecp.com.cn',
            'Connection': 'keep-alive',
            "accept-ranges": "bytes",
            "content-encoding": "gzip",
            "content-length": "2080",
            "content-type": "application/json",
            "date": "Thu, 24 Jul 2025 09:42:36 GMT",
            "eo-cache-status": "HIT",
            "eo-log-uuid": "278692282967270993",
            "server": "TencentEdgeOne",
            "x-frame-options": "SAMEORIGIN",
            "x-request-id": "66cf152d20f419365fc1190d4ba37da5",
        }

        # 发起GET请求
        yield scrapy.Request(
            url=self.start_urls[0],
            method='GET',
            headers=headers,
            params=params,
            callback=self.parse
        )

    def parse(self, response):
        # 解析JSON响应
        data = json.loads(response.text)
        print("=========")
        print(data)

        # 处理API返回的数据
        if data:
            results = []
            for item in data.get("data", []):  # 假设返回的数据包含一个 "data" 字段
                result = {
                    "标题": item.get("title", ""),
                    "发布日期": item.get("publishDate", ""),
                    "地区": item.get("region", ""),
                    "采购单位": item.get("agency", ""),
                    "URL": item.get("url", ""),
                    "来源": self.source
                }
                
                # 将数据保存到 all_results 中
                self.all_results.append(result)
                results.append(result)

                yield result  # 也可以将数据交给 Scrapy 内部处理并保存

import scrapy
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from datetime import datetime, timedelta


class HuaRunSpider(scrapy.Spider):
    name = "huarun"
    allowed_domains = ['www.szecp.com.cn']
    source = "华润守正"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://www.szecp.com.cn/rcms-external-rest/content/getSZExtData"
        today = datetime.now()
        self.valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))
        self.all_results = all_results  # 将外部传入的 all_results 保存在爬虫实例中
        # 如果外部没传入 all_results，自己初始化成空列表
        if all_results is None:
            self.all_results = []
        else:
            self.all_results = all_results

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
        # print(f"Requesting URL: {url}")  # 打印请求的 URL

        # 发起 GET 请求
        try:
            yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            print(f"Request failed with error: {e}")

    def parse(self, response):
        
        # print(response.text)
        # 打印返回的原始文本，检查是否为有效 XML 格式
        # print(f"Response Text (first 500 chars): {response.text[:500]}")  # 打印前 500 个字符作为调试

        # 尝试解析 XML 数据
        try:
            tree = ET.ElementTree(ET.fromstring(response.text))
            root = tree.getroot()
            print(f"Root element: {root.tag}")

            # 提取 XML 数据中的 <data> 节点
            data_list = root.findall('./data/data/data')  # 获取所有的 <data> 内部的 <data> 节点
            if not data_list:
                print("No data found in the XML response.")
                return

            # 提取每个 <data> 元素中的信息
            for item in data_list:
                title = item.findtext('biddingName', default='无招标名称')
                full_url = item.findtext('url', default='无URL')
                publish_date = item.findtext('publishDate', default='无发布日期')
                # bidding_name = item.find('biddingName').text if item.find('biddingName') is not None else 'No bidding name'
                purchase_org = item.find('purchaseOrg/label')
                purchase_org_text = purchase_org.text if purchase_org is not None else '无采购组织'

                # 构造输出的 item
                item = {
                    "标题": title,
                    "发布日期": publish_date,
                    "地区": "",
                    "采购单位": purchase_org_text,
                    "URL": full_url,
                    "来源": self.source
                }

                print(item)  # 打印提取的数据
                self.all_results.append(item)
                yield item
        except Exception as e:
            print(f"Error parsing XML: {e}")

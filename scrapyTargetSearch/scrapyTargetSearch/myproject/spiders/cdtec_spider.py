import scrapy
from urllib.parse import urljoin
from datetime import datetime, timedelta

class CdtEcSpider(scrapy.Spider):
    name = "cdtec"
    allowed_domains = ["www.cdt-ec.com"]
    source = "中国大唐集团有限公司"

    def __init__(self, keyword="电缆", days=3, all_results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.days = int(days)
        self.base_url = "https://www.cdt-ec.com/notice/moreController/getList"
        today = datetime.now()
        self.valid_dates = set((today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days + 1))
        self.all_results = all_results if all_results is not None else []

    def start_requests(self):
        form_data = {
            "page": str(1),
            "limit": str(10),
            "messagetype": str(4),
            "pro_bidding_mothod": str(0),
            "message_title": self.keyword,
            "purchase_unit": "",
            "purchase_unit_agent": "",
            "message_no": "",
            "purchase_code": "",
            "startDate": "",
            "endDate": "",
            "purchase_type": str(0),
        }

        yield scrapy.FormRequest(
            url=self.base_url,
            formdata=form_data,
            callback=self.parse,
            method="POST",
            headers={'User-Agent': 'Mozilla/5.0'},
        )

    def parse(self, response):
        print("----------")
        tr_list = response.xpath('//div[@class="layui-table-body layui-table-main"]/table/tbody/tr')
        print(tr_list)
        for tr in tr_list:
            # 提取第一列中的data-content
            title = tr.xpath('.//td[@data-field="message_title"]/@data-content').get()
            # 提取第二列中的发布日期
            publish_time = tr.xpath('.//td[@data-field="publish_time"]/div/text()').get()

            if title:
                print("======", title.strip())  # 去掉前后空格并打印标题
            else:
                print("No title found for this row")

            if publish_time:
                print("Publish Time:", publish_time.strip())  # 去掉前后空格并打印发布日期
            else:
                print("No publish time found for this row")
        # # 解析 JSON 响应
        # data = response.json()  # 假设响应是JSON格式

        # if not data.get('data'):
        #     return  # 如果没有数据，直接返回

        # for item in data['data']:
        #     # 提取数据字段
        #     title = item.get('message_title')
        #     pub_date = item.get('publish_time')
        #     deadline = item.get('deadline')
        #     purchase_unit = item.get('purchase_unit', '')
        #     purchase_unit_agent = item.get('purchase_unit_agent', '')
        #     item_id = item.get('id')

        #     # 过滤数据：检查发布日期是否在有效日期范围内
        #     if not title or not pub_date:
        #         continue

        #     pub_date_str = pub_date.split(" ")[0]  # 只取日期部分，忽略时间
        #     if pub_date_str not in self.valid_dates:
        #         continue

        #     # 创建完整的URL（如果需要）
        #     full_url = urljoin(self.base_url, f"/notice/{item_id}")  # 假设你需要这个URL

            # # 构造输出数据
            # result_item = {
            #     "标题": title.strip(),
            #     "发布日期": pub_date_str,
            #     "采购单位": purchase_unit.strip(),
            #     "采购单位代理": purchase_unit_agent.strip(),
            #     "截止日期": deadline,
            #     "公告ID": item_id,
            #     "URL": full_url,
            #     "来源": self.source
            # }

            # print(result_item)
            # 将抓取到的数据存储到 all_results 中
            # self.all_results.append(result_item)

            # 输出数据
            # yield result_item
            yield 0


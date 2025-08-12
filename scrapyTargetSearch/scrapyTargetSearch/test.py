import requests

class CdtEcCrawler:
    def __init__(self, keyword="电缆", days=3):
        self.keyword = keyword
        self.days = days
        self.source = "中国大唐集团有限公司"
        self.api_url = "https://www.cdt-ec.com/notice/moreController/getList"
        self.session = requests.Session()  # 使用 Session 来保存 Cookie 和会话信息

    def login(self):
        login_url = "https://www.cdt-ec.com/login"  # 这是一个假设的登录 URL
        login_data = {
            "username": "your_username",  # 填写你的用户名
            "password": "your_password",  # 填写你的密码
        }

        # 模拟登录
        response = self.session.post(login_url, data=login_data)
        response.raise_for_status()  # 检查登录是否成功

        # 登录后，获取 Cookies（session 会自动保存）
        cookies = self.session.cookies.get_dict()
        print(f"Cookies after login: {cookies}")

    def fetch(self):
        today = datetime.now()
        start_date = today - timedelta(days=self.days)
        date_format = "%Y-%m-%d %H:%M:%S"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Origin': 'https://chinasalt.china-tender.com.cn',
            'Referer': 'https://chinasalt.china-tender.com.cn/zbcg/moreinfo.html'
        }

        form_data = {
            "page": 1,
            "limit": 10,
            "messagetype": 4,
            "pro_bidding_mothod": 0,
            "message_title": self.keyword,
            "purchase_unit": "",
            "purchase_unit_agent": "",
            "message_no": "",
            "purchase_code": "",
            "startDate": "",  # 起始日期
            "endDate": "",  # 截止日期
            "purchase_type": 0,
        }

        try:
            # 使用已登录的 session 对象发送请求（Cookies 会自动处理）
            response = self.session.post(self.api_url, data=form_data, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            json_data = response.json()  # 获取JSON数据

            results = []
            if 'data' in json_data:
                for item in json_data['data']:
                    # 解析时间并比较
                    pub_date = datetime.strptime(item['publish_time'], date_format)
                    if start_date <= pub_date <= today:  # 检查公告时间是否在日期范围内
                        results.append({
                            "标题": item['message_title'],
                            "发布日期": item['publish_time'],
                            "地区": "",
                            "采购单位": "",
                            "URL": f"https://www.cdt-ec.com/notice/moreController/xjdhtml?id={item['id']}",
                            "来源": self.source
                        })
            return results
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")  # 请求错误
            return []
        except ValueError as e:
            print(f"解析JSON时出错: {e}")  # JSON解析错误
            return []

# 使用示例
crawler = CdtEcCrawler(keyword="电缆", days=3)
crawler.login()  # 首次登录并获取 Cookie
results = crawler.fetch()  # 使用登录的会话进行数据抓取
print(results)

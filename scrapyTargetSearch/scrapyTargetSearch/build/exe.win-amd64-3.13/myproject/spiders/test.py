import scrapy

class testSpider(scrapy.Spider):
    name='test' #爬虫名字
    allowed_domains=['www.szecp.com.cn'] #当前爬虫允许访问的域名
    #不符合上述规则的域名url将会自动屏蔽

    #起始url，第一个要访问的url
    start_urls=['https://www.szecp.com.cn/first_cggg/index.html']

    def parse(self,response):
        # print("===>",response)
        print(response.text)
        div_list=response.xpath("//div[@class='szb-zbcgTable']/div")
        for div in div_list:
            name=div.xpath(".//div[@class='szb-zbcgTable-other']/a/text()")
            print(name)
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from myproject.spiders.powerchina_spider import PowerChinaSpider
from myproject.spiders.huarun_spider import HuaRunSpider
from myproject.utils.ygcgfw_api import YgcgfwApiCrawlerV2
from myproject.utils.jincaizongheng_api import JingCaiZongHengCrawler
from myproject.utils.chinasalt_api import ChinaSaltCrawler
from datetime import datetime

def run_all(keyword="电缆", days=3):
    all_results = []

    # API 数据
    print("阳光采购网（API）...")
    try:
        ygcg = YgcgfwApiCrawlerV2(keyword=keyword, days=days)
        all_results.extend(ygcg.fetch())
    except Exception as e:
        print(f"阳光采购网出错: {e}")

    print("精彩纵横（API）...")
    try:
        jczh = JingCaiZongHengCrawler(keyword=keyword, days=days)
        all_results.extend(jczh.fetch())
    except Exception as e:
        print(f"精彩纵横出错: {e}")

    print("中盐（API）...")
    try:
        chinasalt = ChinaSaltCrawler(keyword=keyword, days=days)
        all_results.extend(chinasalt.fetch())
    except Exception as e:
        print(f"中盐出错: {e}")

    # Scrapy 爬虫
    print("启动 Scrapy 爬虫...")
    process = CrawlerProcess(get_project_settings())
    process.crawl(PowerChinaSpider, all_results=all_results, keyword=keyword, days=days)
    process.crawl(HuaRunSpider, all_results=all_results, keyword=keyword, days=days)
    process.start()  # 等所有爬虫完成

    # 输出 Excel
    print(f"所有任务完成，总共 {len(all_results)} 条数据")
    if all_results:
        save_to_excel(all_results)
    else:
        print("没有数据，未生成 Excel")


def save_to_excel(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f"result_{timestamp}.xlsx"
    
    df = pd.DataFrame(data)

    # 调整列顺序（如果有固定格式，比如 标题、发布日期、来源、URL）
    preferred_columns = ["标题", "发布日期", "地区", "采购单位", "URL", "来源"]
    columns = [col for col in preferred_columns if col in df.columns]
    df = df[columns]

    # 写入 Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='数据')
        ws = writer.sheets['数据']

        # 自动调整列宽
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            ws.column_dimensions[col_letter].width = max_length + 2

        # 超链接（URL 列）
        if "URL" in df.columns:
            url_index = df.columns.get_loc("URL") + 1
            for row in range(2, len(df) + 2):  # 从第2行开始
                cell = ws.cell(row=row, column=url_index)
                cell.hyperlink = cell.value
                cell.style = "Hyperlink"

    print(f"数据已写入 {excel_file}")


if __name__ == "__main__":
    run_all()

import scrapy
import time

from oschina.items import OschinaItem




class DmozSpider(scrapy.Spider):
    name = "my_spider"
    allowed_domains = ["www.oschina.net"]
    start_urls = [
        "https://www.oschina.net/blog/widgets/_blog_index_recommend_list?classification=5593654&p=1&type=ajax",

    ]

    _page=1

    def _get_next_url(self,cur_url):
        DmozSpider._page+=1
        arr=cur_url.split("&")
        for a in arr:
            if "p=" in a:
                cur_page=int(a.split("=")[-1])
                next_page=cur_page+1

                return cur_url.replace(a,"p=%s" % next_page)


    def parse(self, response):
        lists = response.css(".item.blog-item")
        print("size==",len(lists))
        if len(lists)==0:
            print("data empty")
            return

        for sel in lists:
            title=sel.css("a::attr(title)").extract_first()
            url=sel.css("a::attr(href)").extract_first()
            print("txt--->",title)
            print("url--->",url)
            item=OschinaItem()
            item['title']=title
            item['url']=url
            yield item
        print("response===", response.url)
        url = self._get_next_url(response.url)
        time.sleep(1)
        yield scrapy.Request(url, callback=self.parse)
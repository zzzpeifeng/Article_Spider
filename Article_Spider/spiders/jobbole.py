# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1.获取文章列表url，并下载；
        2.获取下一页文章列表url，并下载；
        '''
        # 解析当前页url：
        # post_urls=response.css("#archive .archive-title::attr(href)").extract()
        # post_urls = response.xpath("//a[@class='archive-title']/@href").extract()
        post_nodes = response.css("#archive .post-thumb a")
        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")
            post_image = post_node.css("img::attr(src)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_img": post_image},
                          callback=self.parse_detail)

        # response.xpath("//a[@class='archive-title']/@href").extract()  #xpath版本
        # 提取下一页
        next_page = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_page:
            yield Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        # 提取文章的具体字段

        #图片
        image=response.meta.get("front_img","")

        # 标题
        title = response.xpath("//div[@class='entry-header']/h1/text()")
        title_result = title.extract()
        # 创建时间
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()")
        create_date_result = create_date.extract()[0].replace("·", "").strip()
        # 点赞数
        praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()")
        praise_num_result = int(praise_num.extract()[0])
        # 收藏数
        fav_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()")
        match_re = re.match(r".*?(\d+).*", fav_num.extract()[0])
        if match_re:
            fav_num = int(match_re.group(1))
        else:
            fav_num = 0

        # 评论数
        comment_num = response.xpath("//a[@href='#article-comment']/span/text()")
        match_re = re.match(".*?(\d+).*", comment_num.extract()[0])
        if match_re:
            comment_num = int(match_re.group(1))
        else:
            comment_num = 0
        # 文章内容
        # article_content=response.xpath("//")
        content = response.xpath("//div[@class='entry']//text()").extract()
        content_data = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        content_key = [content_key for content_key in content_data if not content_key.strip().endswith("评论")]
        content_keys = ','.join(content_key)

    pass

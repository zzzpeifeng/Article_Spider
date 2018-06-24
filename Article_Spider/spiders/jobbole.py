# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from items import JobboleArticleItem,ArticleItemLoader
from utils.commen import get_md5
import datetime
from scrapy.loader import ItemLoader


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
        article_item = JobboleArticleItem()

        # 图片
        image = response.meta.get("front_img", "")
        #
        # # 标题
        # title = response.xpath("//div[@class='entry-header']/h1/text()")
        # title_result = title.extract_first("")
        # # 创建时间
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()")
        # create_date_result = create_date.extract()[0].replace("·", "").strip()
        # # 点赞数
        # praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()")
        # praise_num_result = int(praise_num.extract()[0])
        # # 收藏数
        # fav_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()")
        # match_re = re.match(r".*?(\d+).*", fav_num.extract()[0])
        # if match_re:
        #     fav_num = int(match_re.group(1))
        # else:
        #     fav_num = 0
        #
        # # 评论数
        # comment_num = response.xpath("//a[@href='#article-comment']/span/text()")
        # match_re = re.match(".*?(\d+).*", comment_num.extract()[0])
        # if match_re:
        #     comment_num = int(match_re.group(1))
        # else:
        #     comment_num = 0
        # # 文章内容
        # # article_content=response.xpath("//")
        # content = response.xpath("//div[@class='entry']//text()").extract()
        # content_data = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # content_key = [content_key for content_key in content_data if not content_key.strip().endswith("评论")]
        # content_keys = ','.join(content_key)
        #
        # article_item['url'] = response.url
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['front_img_url'] = [image]
        # article_item['title'] = title_result
        # try:
        #     create_date_result = datetime.datetime.strptime(create_date_result, '%Y/%m/%d').date()
        # except Exception as e:
        #     create_date_result = datetime.datetime.now()
        # article_item['create_time'] = create_date_result
        # article_item['praise_num'] = praise_num_result
        # article_item['fav_num'] = fav_num
        # article_item['comment_num'] = comment_num
        # article_item['content'] = content
        # article_item['tags'] = content_keys

        # 通过item loader 加载item
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_img_url", [image])
        item_loader.add_xpath("title", "//div[@class='entry-header']/h1/text()")
        item_loader.add_xpath("create_time", "//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loader.add_xpath("praise_num", "//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_xpath("fav_num", "//span[contains(@class,'bookmark-btn')]/text()")
        item_loader.add_xpath("comment_num", "//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath("content", "//div[@class='entry']//text()")
        item_loader.add_xpath("tags", "//p[@class='entry-meta-hide-on-mobile']/a/text()")

        article_item= item_loader.load_item()

        yield article_item

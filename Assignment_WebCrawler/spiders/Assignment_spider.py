import scrapy
from ..items import AssignmentWebcrawlerItem

class AssignmentSpider(scrapy.Spider):
    name = 'reuters'
    start_urls=[
        'https://in.reuters.com/news/top-news'
    ]

    def parse(self, response):

        starts_with = 'https://in.reuters.com'
        
        item=AssignmentWebcrawlerItem()

        stories = response.css('article.story')
        
        for story in stories:
            
            story_images = story.css('div.story-photo')
            
            for story_img in story_images:
                img_link = story_img.css('img::attr(org-src)').extract_first()
                if (img_link == None):
                    img_link = story_img.css('img::attr(src)').extract_first()
                item['img_link'] = img_link
            
            stories_rest = story.css('div.story-content')
            
            for story_rest in stories_rest:
                title = story_rest.css('h3.story-title::text').extract_first().strip()
                summary = story_rest.css('p::text').extract_first()
                time_of_publish = story_rest.css('.timestamp::text').extract_first()
                web_link = story_rest.css('a::attr(href)').extract_first()
                
                item['title'] = title
                item['summary'] = summary
                item['time_of_publish'] = time_of_publish
                item['web_link'] = starts_with+web_link
            
            yield item
        
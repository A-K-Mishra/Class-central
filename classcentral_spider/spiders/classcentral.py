from scrapy import Spider
from scrapy.http import Request


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://www.classcentral.com/subjects']

    def __init__(self,subject=None):
        self.subject =subject
    
    def parse(self,response):
        if self.subject:
            subject_url = response.xpath('//a[contains(@title,"'+self.subject+'")]/@href').extract_first()
            absolute_subject_url = response.urljoin(subject_url)
            yield Request(absolute_subject_url,callback = self.parse_subject)
        else:
            subjects = response.xpath('//h3/a[1]/@href').extract()
            for subject in subjects:
                absolute_subject_url = response.urljoin(subject)
                yield Request(absolute_subject_url,callback = self.parse_subject)
            

    def parse_subject(self,response):
        subject_name = response.xpath('//h1//text()').extract_first()
        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')
        for course in courses :
            course_name = course.xpath('.//a[@itemprop = "url"]/@title').extract_first()
            course_url = course.xpath('.//a[@itemprop = "url"]/@href').extract_first()
            absolute_course_url = response.urljoin(course_url)
            
            yield {
                'subject_name':subject_name,
                'course_name' : course_name,
                'absolute_course_url' : absolute_course_url
            }
        next_page = response.xpath('//link[@rel = "next"]/@href').extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page);
            yield Request(next_page_url,callback=self.parse_subject)
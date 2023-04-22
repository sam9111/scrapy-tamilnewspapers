import scrapy

import re


def clean(content):
    if not content:
        return ""
    CLEAN_HTML = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    CLEAN_ALPHA = re.compile("[a-zA-Z0-9 ]+")
    CLEAN_PUNCT = re.compile(r"[\"&.;:`!\'?,\"()\[\]-|’‘-“”-]")
    CLEAN_MONEY = re.compile(r"ரூ\.")
    CLEAN_SINGLE = re.compile(r"\s+[^\u0B80-\u0BFF]{0,1}\s+")
    CLEAN_SINGLE_2 = re.compile(r"\s+ம்\s+")
    CLEAN_SINGLE_3 = re.compile(r"\s+க்கு\s+")
    CLEAN_SINGLE_4 = re.compile(r"\s+க்கும்\s+")
    CLEAN_SINGLE_5 = re.compile(r"\s+க்குள்\s+")
    CLEAN_SINGLE_6 = re.compile(r"\s+ரூ\s+")
    CLEAN_MULTIPLE = re.compile(r"\.{2,}")
    CLEAN_WHITE = re.compile(r"\s{2,}")

    content = re.sub(CLEAN_HTML, " ", content)
    content = re.sub(CLEAN_ALPHA, " ", content)
    content = re.sub(CLEAN_PUNCT, "", content)
    content = re.sub(CLEAN_MONEY, "", content)
    content = re.sub(CLEAN_MULTIPLE, " ", content)
    content = re.sub(CLEAN_SINGLE, " ", content)
    content = re.sub(CLEAN_SINGLE_2, " ", content)
    content = re.sub(CLEAN_SINGLE_3, " ", content)
    content = re.sub(CLEAN_SINGLE_4, " ", content)
    content = re.sub(CLEAN_SINGLE_5, " ", content)
    content = re.sub(CLEAN_SINGLE_6, " ", content)
    content = re.sub(CLEAN_WHITE, " ", content)
    content = content.strip()
    return content


class MalaimurasuSpider(scrapy.Spider):
    name = "malaimurasu"
    allowed_domains = ["www.malaimurasu.com"]
    start_urls = [
        "https://www.malaimurasu.com/rss/latest-posts",
        "https://www.malaimurasu.com/rss/category/cover-story",
        "https://www.malaimurasu.com/rss/category/viral",
        "https://www.malaimurasu.com/rss/category/tamilnadu",
        "https://www.malaimurasu.com/rss/category/india",
        "https://www.malaimurasu.com/rss/category/worldnews",
    ]

    def parse(self, response):
        response.selector.register_namespace(
            "content", "http://purl.org/rss/1.0/modules/content/"
        )

        try:
            for article in response.xpath("//item"):
                if article:
                    yield {
                        "title": clean(article.xpath("title/text()").extract_first()),
                        "link": article.xpath("link/text()").extract_first(),
                        "pubDate": article.xpath("pubDate/text()").extract_first(),
                    }

        # trunk-ignore(flake8/E722)
        except:
            self.logger.error("Failed to parse feed: %s", response.url)

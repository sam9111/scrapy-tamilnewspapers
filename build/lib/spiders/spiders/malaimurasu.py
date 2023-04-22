import scrapy

import re


def clean(content):
    if not content:
        return ""
    CLEAN_HTML = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    CLEAN_ALPHA = re.compile(".*?[A-Za-z0-9].*?")
    CLEAN_PUNCT = re.compile(r"[%\"&.;:`!\'?,\"()\[\]-|’‘-“”-]")
    CLEAN_WHITE = re.compile(r"\s{2,}")

    content = re.sub(CLEAN_HTML, " ", content)
    content = re.sub(CLEAN_ALPHA, " ", content)
    content = re.sub(CLEAN_PUNCT, "", content)
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

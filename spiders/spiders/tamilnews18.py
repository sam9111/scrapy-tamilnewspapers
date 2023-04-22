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


class Tamilnews18Spider(scrapy.Spider):
    name = "tamilnews18"
    allowed_domains = ["tamil.news18.com"]
    start_urls = [
        "https://tamil.news18.com/rss/live-updates.xml",
        "https://tamil.news18.com/rss/national.xml",
        "https://tamil.news18.com/rss/international.xml",
        "https://tamil.news18.com/rss/local-news.xml",
        "https://tamil.news18.com/rss/trend.xml",
    ]

    def parse(self, response):
        response.selector.register_namespace(
            "content", "http://purl.org/rss/1.0/modules/content/"
        )
        try:
            for article in response.xpath("//item"):
                if article:
                    yield {
                        "processed_title": clean(article.xpath("title/text()").extract_first()),
                        "title": article.xpath("title/text()").extract_first(),
                        "link": article.xpath("link/text()").extract_first(),
                        "pubDate": article.xpath("pubDate/text()").extract_first(),
                    }

        # trunk-ignore(flake8/E722)
        except:
            self.logger.error("Failed to parse feed: %s", response.url)

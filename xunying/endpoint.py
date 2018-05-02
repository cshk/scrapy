from scrapy.cmdline import execute


execute(["scrapy", "crawl", "xymovies"])

from scrapy.dupefilter import RFPDupeFilter
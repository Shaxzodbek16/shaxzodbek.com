from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            "blog:home",
            "blog:aboutme",
            "blog:post",
            "blog:certifications",
            "blog:projects",
        ]

    def location(self, item):
        return reverse(item)

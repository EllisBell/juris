from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from jurisapp.models import Acordao


class AcordaoSiteMap(Sitemap):
    changefreq = "never"
    priority = 0.5
    limit = 5000

    def items(self):
        return Acordao.objects.only("acordao_id", "date_loaded")

    def lastmod(self, obj):
        return obj.date_loaded


class StaticViewSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['termos', 'sobre']

    def location(self, item):
        return reverse(item)

"""
Data source configuration for CeylonPulse
Contains all URLs and API endpoints for data collection
"""

ADA_DERANA_URLS = {
    'rss_feed': 'https://www.adaderana.lk/rss.php',
    'news_page': 'https://www.adaderana.lk/news.php',
    'breaking_news': 'https://www.adaderana.lk/breaking-news',
    'business': 'https://www.adaderana.lk/business-news',
    'sports': 'https://www.adaderana.lk/sports-news'
}

ECONOMYNEXT_URLS = {
    'rss_feed': 'https://economynext.com/rss',
    'main_site': 'https://economynext.com/',
    'sri_lanka_news': 'https://economynext.com/c/sri-lanka',
    'business': 'https://economynext.com/c/business',
    'politics': 'https://economynext.com/c/politics'
}

TWITTER_SOURCES = {
    'api_base': 'https://api.twitter.com/2/',
    'key_accounts': [
        'https://twitter.com/AdaDerana',
        'https://twitter.com/newsfirstlk', 
        'https://twitter.com/adaderanaenglish',
        'https://twitter.com/PresSecSL',
        'https://twitter.com/PMD_SL',
        'https://twitter.com/DMCSriLanka',
        'https://twitter.com/CBSL',
        'https://twitter.com/CEBSriLanka'
    ]
}

MET_DEPARTMENT_URLS = {
    'main_site': 'http://www.meteo.gov.lk/',
    'english_version': 'http://www.meteo.gov.lk/index.php?lang=en',
    'warnings': 'http://www.meteo.gov.lk/index.php?option=com_content&view=article&id=94&Itemid=310&lang=en',
    'weather_forecast': 'http://www.meteo.gov.lk/index.php?option=com_content&view=article&id=96&Itemid=512&lang=en'
}

CENTRAL_BANK_URLS = {
    'main_site': 'https://www.cbsl.gov.lk/',
    'statistics': 'https://www.cbsl.gov.lk/statistics',
    'economic_indicators': 'https://www.cbsl.gov.lk/economic-indicators',
    'publications': 'https://www.cbsl.gov.lk/publications',
    'news': 'https://www.cbsl.gov.lk/news'
}

GOOGLE_TRENDS = {
    'sri_lanka_trends': 'https://trends.google.com/trends/explore?geo=LK',
    'api_documentation': 'https://trends.google.com/trends/api/'
}

PARLIAMENT_URLS = {
    'main_site': 'https://www.parliament.lk/',
    'news': 'https://www.parliament.lk/news.php',
    'bills': 'https://www.parliament.lk/en/bills',
    'hansard': 'https://www.parliament.lk/hansard-search',
    'cabinet_decisions': 'https://www.parliament.lk/cabinet-decisions'
}

ADVOCATA_URLS = {
    'main_site': 'https://www.advocata.org/',
    'publications': 'https://www.advocata.org/publications',
    'research': 'https://www.advocata.org/research',
    'commentary': 'https://www.advocata.org/commentary',
    'media': 'https://www.advocata.org/media'
}

BRS_URLS = {
    'linkedin': 'https://www.linkedin.com/company/brs-equity-research/',
    'reports_platform': 'https://www.researchgate.net/institution/BRS-Equity-Research',
    'financial_portals': 'Watch on Bloomberg, Reuters financial platforms'
}

NWSDB_URLS = {
    'main_site': 'https://www.waterboard.lk/',
    'announcements': 'https://www.waterboard.lk/announcements.html',
    'water_interruptions': 'https://www.waterboard.lk/water_interruptions.html',
    'contact': 'https://www.waterboard.lk/contact_us.html'
}

CEB_URLS = {
    'main_site': 'https://ceb.lk/',
    'outage_notices': 'https://ceb.lk/outage-notices',
    'load_shedding': 'https://ceb.lk/load-shedding-schedule',
    'facebook': 'https://www.facebook.com/cebsrilanka',
    'twitter': 'https://twitter.com/CEBSriLanka'
}

CSE_URLS = {
    'main_site': 'https://www.cse.lk/',
    'market_summary': 'https://www.cse.lk/home/marketSummary',
    'listed_companies': 'https://www.cse.lk/home/listedCompanies',
    'trading_statistics': 'https://www.cse.lk/home/tradeSummary'
}

# All sources grouped by type
SCRAPING_SOURCES = {
    'ada_derana': ADA_DERANA_URLS,
    'economynext': ECONOMYNEXT_URLS,
    'met_department': MET_DEPARTMENT_URLS,
    'central_bank': CENTRAL_BANK_URLS,
    'parliament': PARLIAMENT_URLS,
    'advocata': ADVOCATA_URLS,
    'nwsdb': NWSDB_URLS,
    'ceb': CEB_URLS,
    'cse': CSE_URLS
}

API_SOURCES = {
    'twitter': TWITTER_SOURCES,
    'google_trends': GOOGLE_TRENDS
}


# -*- coding: utf-8 -*-
BOT_NAME = 'newspy'
SPIDER_MODULES = ['newspy.spiders']
NEWSPIDER_MODULE = 'newspy.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'newspy.pipelines.MongoDBPipeline': 100
}

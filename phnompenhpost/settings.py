
BOT_NAME = 'phnompenhpost'

SPIDER_MODULES = ['phnompenhpost.spiders']
NEWSPIDER_MODULE = 'phnompenhpost.spiders'

ROBOTSTXT_OBEY = False
LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'phnompenhpost.pipelines.MySQLPipeline': 2
}

DOWNLOADER_MIDDLEWARES = {
	'phnompenhpost.middlewares.SeleniumMiddleware': 200
}

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = 'tU/x@168rY'
DB_DB = 'khmergoo_sequelize'

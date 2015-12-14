WORKER_PROCESSES = 5

TELEGRAM_BOT_TOKEN = '0123456789'

RESOLVER = 'resolver'

MIDDLEWARES = [
    #'telegram.middlewares.dryrun.DryRun',
    'telegram.middlewares.sessions.SessionMiddleware',
    ]

BDVOICE_TOKEN = '0123456789'

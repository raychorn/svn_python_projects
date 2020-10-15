from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    #'vypercms/code.js',
)

if not hasattr(settings, 'ACCOUNT_ACTIVATION_DAYS'):
    settings.ACCOUNT_ACTIVATION_DAYS = 10

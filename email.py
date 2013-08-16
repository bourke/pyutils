from mailshake import Mailer, SMTPMailer, ToMemoryMailer


def make_mailer(config):
    keys = set(('SMTP_HOST', 'SMTP_PORT', 'SMTP_USERNAME',
                'MAIL_MODE', 'SMTP_PASSWORD', 'SMTP_USE_TLS'))
    if keys <= set(config.keys()) and \
            config['MAIL_MODE'] == 'production':
        return SMTPMailer(
            host=config.get('SMTP_HOST'),
            port=config.get('SMTP_PORT'),
            username=config.get('SMTP_USERNAME'),
            password=config.get('SMTP_PASSWORD'),
            use_tls=config.get('SMTP_USE_TLS'),
            default_from=config.get('SMTP_FROM_EMAIL',
                'donotreply@comfortfoodkitchen.com')
        )
    elif 'MAIL_MODE' in config and \
            config['MAIL_MODE'] == 'test':
        return ToMemoryMailer()
    else:
        return Mailer()

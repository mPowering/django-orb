

def is_search_crawler(user_agent):
    spiders = {'Googlebot', 'Yammybot', 'Openbot', 'Yahoo', 'Slurp', 'msnbot', 'ia_archiver', 'Lycos', 'Scooter', 'AltaVista', 'Teoma', 'Gigabot', 'Googlebot-Mobile'}
    for s in spiders:
        if s in user_agent:
            return True
    return False
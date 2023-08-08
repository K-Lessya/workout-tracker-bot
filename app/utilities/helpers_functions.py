from app.bot import bot


def process_tg_link(link: str):
    if "https://t.me/" in link:
        return link.replace("https://t.me/", "")
    else:
        return link


def check_link(link: str):
    if "http://" or "https://" in link:
        return True
    else:
        return False



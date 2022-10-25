mode = "local"

if mode == "PROD":
    IN_PATH = r"/home/ubuntu/app/prod/kv2/global-crawl-engine/social-media-crawl/drive/in"
    SCRAPPED_PATH = r"/home/ubuntu/app/prod/kv2/global-crawl-engine/social-media-crawl/drive/out"
    PROCESSED_PATH = r"/home/ubuntu/app/prod/kv2/global-crawl-engine/social-media-crawl/drive/processed"
    LOG_PATH = r"/home/ubuntu/app/prod/kv2/global-crawl-engine/social-media-crawl/drive/log"
    CHROME_PATH = r"/snap/bin/chromium.chromedriver"
    SERVER_HOST = r"44.203.14.141:6003"
elif mode == "DEV":
    IN_PATH = r"/home/ubuntu/kv2/dev/sub-platform/kv2-global-crawl-engine/socialmedia_crawl/drive/in"
    SCRAPPED_PATH = r"/home/ubuntu/kv2/dev/sub-platform/kv2-global-crawl-engine/socialmedia_crawl/drive/out"
    PROCESSED_PATH = r"/home/ubuntu/kv2/dev/sub-platform/kv2-global-crawl-engine/socialmedia_crawl/drive/processed"
    LOG_PATH = r"/home/ubuntu/kv2/dev/sub-platform/kv2-global-crawl-engine/log"
    CHROME_PATH = r"/usr/bin/chromedriver"
    SERVER_HOST = r"54.90.61.114:6003"
else:
    IN_PATH = r"W:/STRATESPHERE/drive/Social_media_crawler/in"
    SCRAPPED_PATH = r"W:/STRATESPHERE/drive/Social_media_crawler/out"
    HISTORY_PATH = r"W:/STRATESPHERE/drive/Social_media_crawler/history"
    PROCESSED_PATH = r"W:/STRATESPHERE/drive/Social_media_crawler/processed"
    LOG_PATH = r"W:/STRATESPHERE/drive/Social_media_crawler/log"
    CHROME_PATH = r"C:/Users/subha/Downloads/chromedriver_win32/chromedriver"
    SERVER_HOST = r"127.0.0.1:5000"

MAX_RETRY = 5
SOURCES = "linkedin, pitchbook"

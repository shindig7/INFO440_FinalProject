from person import *
from utils import get_twitter_handler
from time import sleep
from pprint import pprint
from twitter.api import TwitterHTTPError
import logging

FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(funcName)s] - %(message)s"
logging.basicConfig(level=10, format=FORMAT)

i = 0
jon = 4919781293
to_get = [jon]

t = get_twitter_handler()
follow_dict = {}

while i < 50:
    new_id = to_get.pop(0)
    logging.info(f"Getting id {i+1}")
    try:
        new_followers = get_followers(t, new_id)
        sleep(60)
    except TwitterHTTPError:
        logging.error("Rate limiting exceeded; waiting then trying again...")
        sleep(60)
        new_followers = get_followers(t, new_id)

    to_get.extend(new_followers)
    follow_dict[new_id] = new_followers
    i += 1


with open("followers.txt", 'w') as F:
    F.write(follow_dict)

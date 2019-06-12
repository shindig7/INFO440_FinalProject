from person import *
from utils import *
import pandas as pd
from time import sleep
import logging

FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(funcName)s] - %(message)s"
logging.basicConfig(level=10, format=FORMAT)


def divide_user_list(users, n=100):
    for i in range(0, len(users), n):
        yield users[i:i+n]


def get_user_followers(twitter_handler, user_set):
    u = get_multiple_people(twitter_handler, twitter_ids=None, twitter_handles=user_set)
    followers = [P.Followers_Count for P in u]
    return dict(zip(user_set, followers))


def main():
    from pprint import pprint
    full_df = pd.read_csv("ten_percent_sample.csv")
    th = get_twitter_handler()

    users_nodupes = list(set(full_df.User.tolist()))
    user_gen = divide_user_list(users_nodupes)
    ten_per = round(len(users_nodupes) / 1000)

    logging.info("Starting collection...")
    user_followers = {}
    for i, user_set in enumerate(user_gen):
        if i % ten_per == 0:
            logging.info("{}% Complete".format(round((i * 10) / ten_per)))
        #logging.info(f"i:{i}")
        user_followers.update(get_user_followers(th, user_set))
        sleep(1)

    logging.info("100% Complete")
    output_df = pd.DataFrame.from_dict(user_followers, 'index', columns=["Followers"])
    output_df.to_csv("followers.csv")
    logging.info("Written to file; Process Complete")


if __name__ == "__main__":
    main()

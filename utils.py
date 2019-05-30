import yaml
from twitter import Twitter, OAuth


def load_config():
    with open(
        "C:/Users/eagle/Documents/Drexel/Junior_18_19/Spring/INFO440_SocialMediaDataAnalysis/config.yml",
        "r",
    ) as c:
        return yaml.load(c, Loader=yaml.CLoader)


def get_twitter_handler():
    config = load_config()
    return Twitter(
        auth=OAuth(
            config["access-token"],
            config["secret-token"],
            config["consumer-key"],
            config["secret-key"],
        ),
        retry=True,
    )


def get_rate_limit_status(twitter_handler, arg):
    rl = twitter_handler.application.rate_limit_status()["resources"]
    if arg == "followers":
        return rl["followers"]["/followers/ids"]["remaining"]
    elif arg == "users_lookup":
        return rl["users"]["/users/lookup"]["remaining"]
    elif arg == "users_show":
        return rl["users"]["/users/show"]["remaining"]


def main():
    t = get_twitter_handler()
    print(get_rate_limit_status(t, "followers"))


if __name__ == "__main__":
    main()

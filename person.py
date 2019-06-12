from datetime import datetime, timezone


class Person(object):
    def __init__(self, twitter_data):
        self.ID = twitter_data["id"]
        self.Name = twitter_data["name"]
        self.Handle = twitter_data["screen_name"]
        self.Location = (
            None if twitter_data["location"] == "" else twitter_data["location"]
        )
        self.Description = twitter_data["description"]
        self.Followers_Count = twitter_data["followers_count"]
        self.Friends_Count = twitter_data["friends_count"]
        self.Verified = twitter_data["verified"]

        now = datetime.now(timezone.utc)
        self.Create_Date = datetime.strptime(
            twitter_data["created_at"], "%a %b %d %H:%M:%S %z %Y"
        )
        self.Account_Age = now - self.Create_Date

        self.Favorite_Count = twitter_data["favourites_count"]
        self.Language = twitter_data["lang"]
        self.Status_Count = twitter_data["statuses_count"]

    def __repr__(self):
        return "Name: {} Handle: {} Followers: {}".format(
            self.Name, self.Handle, self.Followers_Count
        )

    def __str__(self):
        return "Name: {} Handle: {} Followers: {}".format(
            self.Name, self.Handle, self.Followers_Count
        )


def get_person_by_id(twitter_handler, twitter_id):
    p = twitter_handler.users.show(user_id=twitter_id)
    return Person(p)


def get_multiple_people(twitter_handler, twitter_ids=None, twitter_handles=None):
    if twitter_ids:
        user_list = twitter_handler.users.lookup(user_id=",".join(twitter_ids))
    elif twitter_handles:
        user_list = twitter_handler.users.lookup(screen_name=",".join(twitter_handles))
    return [Person(u) for u in user_list]


def get_followers(twitter_handler, twitter_id):
    return twitter_handler.followers.ids(user_id=twitter_id)["ids"]


def main():
    from twitter import Twitter, OAuth
    from utils import get_twitter_handler

    t = get_twitter_handler()

    followers = t.followers.ids()["ids"]

    print(get_multiple_people(t, followers))


if __name__ == "__main__":
    main()

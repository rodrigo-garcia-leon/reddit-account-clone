from os import environ
import praw

USER_AGENT = 'script:account-clone:1.0.0'

source = praw.Reddit(
    client_id=environ['REDDIT_SOURCE_CLIENT_ID'],
    client_secret=environ['REDDIT_SOURCE_CLIENT_SECRET'],
    password=environ['REDDIT_SOURCE_PASSWORD'],
    user_agent=USER_AGENT,
    username=environ['REDDIT_SOURCE_USERNAME']
)


def getItemType(itemType):
    if itemType == "<class 'praw.models.reddit.submission.Submission'>":
        return 'submission'

    if itemType == "<class 'praw.models.reddit.comment.Comment'>":
        return 'comment'

    return itemType


savedItems = []
# savedItems = [{'id': item.id, 'type': getItemType(str(type(item)))}
#               for item in source.user.me().saved(limit=None)]
# print(savedItems)

# savedSubreddits = []
savedSubreddits = [{'name': item.display_name, 'favorite': item.user_has_favorited}
                   for item in source.user.subreddits(limit=None)]
# print(savedSubreddits)

target = praw.Reddit(
    client_id=environ['REDDIT_TARGET_CLIENT_ID'],
    client_secret=environ['REDDIT_TARGET_CLIENT_SECRET'],
    password=environ['REDDIT_TARGET_PASSWORD'],
    user_agent=USER_AGENT,
    username=environ['REDDIT_TARGET_USERNAME']
)

for savedItem in savedItems:
    item = None

    if savedItem['type'] == 'submission':
        item = target.submission(savedItem['id'])

    if savedItem['type'] == 'comment':
        item = target.comment(savedItem['id'])

    if not item:
        continue

    item.save()
    print(f"Item #{item} saved")

for savedSubreddit in savedSubreddits:
    subreddit = target.subreddit(savedSubreddit['name'])
    subreddit.subscribe()

    if savedSubreddit['favorite']:
        print(savedSubreddit)
        print(subreddit)
        subreddit.favorite()

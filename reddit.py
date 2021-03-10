import praw
import settings
import time
import os

agent = 'Gmusic playlist app by /u/Sigmatics'

class Reddit:
    def __init__(self):
        if settings['reddit']['refresh_token'] == "":
            print("Please run setup first!")
            return

        self.reddit = praw.Reddit(client_id=settings['reddit']['client_id'],
                             client_secret=settings['reddit']['client_secret'],
                             refresh_token=settings['reddit']['refresh_token'],
                             user_agent=agent)

    def comment_EDM(self, content):
        sub = self.reddit.subreddit('EDM')
        query = 'title:"New EDM This Week"'
        results = sub.search(query, time_filter="week")
        commented = False
        for x in results:
            if time.time() - x.created_utc < 86400:
                print("Commenting post: " + x.title)
                x.reply(content)
                commented = True
                break

        return commented

    def get_top_new(self, time="week"):
        sub = self.reddit.subreddit('EDM')
        query = 'flair:"new music"'
        results = sub.search(query, time_filter=time, sort="top")
        urls = [x.url for x in results]
        spotify = []
        youtube = []
        youtube_pos = []
        count = 0
        for url in urls:
            if "open.spotify.com" in url:
                spotify.append(url)
                count += 1
            elif "youtu.be" in url or "youtube.com" in url:
                youtube.append(url)
                youtube_pos.append(count)
                count += 1
        return {
            "spotify": spotify,
            "youtube": youtube,
            "youtube_pos": youtube_pos,
        }


if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__)) + os.sep
    filename = path + "comment.txt"
    if not os.path.isfile(filename):
        exit()
    f = open(filename, 'r')
    comment = f.read()
    r = Reddit()
    success = r.comment_EDM(comment)
    if success:
        os.remove(filename)


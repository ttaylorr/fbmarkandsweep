import facebook
import requests

access_token = "CAACEdEose0cBAOKcwPISS7FEOlEe5qZBJFVOT9rTKlf0RYFYeFX0NputJJt3AeztZAOX1N4pOQ64DriyLiZAtVB4JZA3HjC6BxzY6ZAHSDyykhur2isg5k4aMXZAQfkISYnN78ZBcSu9KdBUEIvOaoA1VicYCSjalFXsL2t1jAmMrTZAkSJV11BOqgELbH38QL1ZAqZBf1xQrn3amQ6IEkwxqX"

class GroupPoller:
    def __init__(self, access_token, group_id):
        self.access_token = str(access_token)
        self.group_id = str(group_id)

        self.graph = facebook.GraphAPI(self.access_token)

    def paginate_top(self):
        posts = self.graph.get_connections(self.group_id, "feed")
        all_posts = (FacebookPost(post) for post in posts['data'])

        for post in all_posts:
            print post.post_id + "||" + post.contents.replace("\n", " ")

    def paginate_all(self):
        all_posts = list()
        posts = self.graph.get_connections(self.group_id, "feed")

        while True:
            # This will evaluate to false when there is no data
            if 'paging' in posts:
                for post in posts['data']:
                    fb_post = FacebookPost(post)
                    if fb_post:
                        all_posts.append(fb_post)

                posts = requests.get(posts['paging']['next']).json()
            else:
                break

        return all_posts

class FacebookPost:
    def __init__(self, post):
        self.group_id = post['id'].split("_")[0]
        self.post_id = post['id'].split("_")[1]

        self.poster = post['from']

        # Not all posts have messages, apparently!
        try:
            self.contents = post['message']
        except KeyError:
            return # It'll just return nil if nothing exists
        
    def post_comment(self, body, post_id):
        r = requests.post('https://graph.facebook.com/v2.1/' + post_id + '/comments?access_token=' + access_token + '&message=' + body)
        return r.json()

gp = GroupPoller(access_token, '759985267390294')
all_posts = gp.paginate_all()

import requests

class FirstFruits:
    def __init__(self, instagram_user):
        self.instagram_user = instagram_user

    def get_profile_posts(self, instagram_user):
        url = "https://www.instagram.com/{username}/feed/?__a=1&__d=dis".format(
            username=instagram_user
        )
        headers = {
            'Host': 'www.instagram.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }

        response = requests.get(url, headers=headers)
        response_json = response.json()
        posts = response_json['graphql']['user']['edge_owner_to_timeline_media']
        
        return posts

    def get_most_recent_post(self, posts):
        images = []
        post = posts['edges'][0]['node']

        description = post['edge_media_to_caption']['edges'][0]['node']['text']
        nodes = post['edge_sidecar_to_children']['edges']

        for node in nodes:
            display_url = node['node']['display_url']
            images.append(display_url)

        return {description: images}


if __name__ == '__main__':
    FirstFruitsx = FirstFruits('firstfruitscbccoc')
    posts = FirstFruitsx.get_profile_posts('firstfruitscbccoc')
    print(FirstFruitsx.get_most_recent_post(posts))

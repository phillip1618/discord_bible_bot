import requests

class FirstFruits:
    def __init__(self, instagram_user):
        self.instagram_user = instagram_user

    def get_profile_posts(self, instagram_user):
        url = "https://www.instagram.com/{username}/?__a=1&__d=dis".format(
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

    def process_graph_post_media(self, node):
        if node['__typename'] == "GraphImage":
            media_url = node['display_url']
        elif node['__typename'] == "GraphVideo":
            media_url = node['video_url']
        
        return media_url

    def process_graph_sidecar_media(self, node):
        media_url_list = []
        sidecar_nodes = node['edge_sidecar_to_children']['edges']

        for sidecar_node in sidecar_nodes:
            media_url = self.process_graph_post_media(sidecar_node)
            media_url_list.append(media_url)
        
        return media_url_list

    def get_most_recent_post(self, posts):
        post = posts['edges'][0]['node']

        description = post['edge_media_to_caption']['edges'][0]['node']['text']

        if post['__typename'] == "GraphSidecar":
            media_url_list = self.process_graph_sidecar_media(post)
        else:
            media_url = self.process_graph_post_media(post)
            media_url_list = [media_url]

        return {description: media_url_list}


if __name__ == '__main__':
    FirstFruitsx = FirstFruits('firstfruitscbccoc')
    posts = FirstFruitsx.get_profile_posts('firstfruitscbccoc')
    print(FirstFruitsx.get_most_recent_post(posts))

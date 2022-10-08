import discord

import requests
import os
from time import sleep

from urllib.request import urlopen
from bs4 import BeautifulSoup

class FirstFruits:
    def __init__(self, instagram_user):
        self.instagram_user = instagram_user
        self.number_of_posts = self.get_number_of_posts(self.instagram_user)

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

    def get_number_of_posts(self, instagram_user):
        url = "https://www.instagram.com/{username}/".format(
            username=instagram_user
        )
        page = urlopen(url)
        html = page.read().decode('utf-8')

        soup = BeautifulSoup(html, 'html.parser')
        html_text = soup.find('meta', property='og:description')
        meta_description = html_text['content']
        number_of_posts = meta_description.split(',')[2].strip()[:2]

        return number_of_posts
    
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

    def send_recent_post(self, post_json):
        print('wow new post!')
        return

    def instagram_webhook(self):
        webhook = discord.Webhook.from_url(
            os.getenv('INSTAGRAM_WEBHOOK_URL'),
            adapter=discord.RequestsWebhookAdapter()
        )
        while True:
            current_number_of_posts = self.get_number_of_posts(
                self.instagram_user
            )
            if self.number_of_posts != current_number_of_posts:
                posts = self.get_profile_posts(self.instagram_user)
                recent_post = self.get_most_recent_post(posts)
                self.send_recent_post(recent_post)
            else:
                print('no new post :(')
            sleep(60)


if __name__ == '__main__':
    FirstFruitsx = FirstFruits('mikpillihp')
    # posts = FirstFruitsx.get_profile_posts('firstfruitscbccoc')
    # print(FirstFruitsx.get_most_recent_post(posts))
    print(FirstFruitsx.get_number_of_posts('mikpillihp'))
    print(FirstFruitsx.number_of_posts)
    FirstFruitsx.instagram_webhook()

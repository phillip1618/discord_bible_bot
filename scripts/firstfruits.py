import discord

import requests
import os
import cv2
from time import sleep

import urllib.request
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

    def get_most_recent_post(self, instagram_access_token):
        profile_url = 'https://graph.instagram.com/me/media'
        fields = [
            'id',
            'caption',
            'media_type',
            'media_url',
            'permalink',
            'thumbnail_url',
            'timestamp',
            'username',
            'children{media_url,media_type,thumbnail_url}'
        ]
        fields_str = ','.join(fields)
        access_token = instagram_access_token
        params = {
            'fields': fields_str,
            'access_token': access_token
        }
        request = requests.get(profile_url, params=params)
        recent_post = request.json()['data'][0]

        return recent_post

    def process_recent_post(self, recent_post):
        media_url_dict = {}
        description = recent_post['caption']
        media_type = recent_post['media_type']
        if media_type == 'IMAGE' or media_type == 'VIDEO':
            media_url_dict[recent_post['media_url']] = media_type
        else:
            recent_post_children = recent_post['children']['data']
            for child in recent_post_children:
                media_url_dict[child['media_url']] = child['media_type']
        
        return {description: media_url_dict}

    def generate_hconcat_minimum_height(self, img_file_name_list):
        img_list = [cv2.imread(img) for img in img_file_name_list]
        h_min = min(img.shape[0] 
                    for img in img_list)
        return h_min

    def generate_hconcat_resize_image_file(
                self,
                img_file_name_list,
                h_min,
                concat_image_index,
                interpolation = cv2.INTER_CUBIC):
        # take minimum hights
        img_list = [cv2.imread(img) for img in img_file_name_list]
        
        len_img_list = len(img_list)
        
        if len_img_list < 5:
            # image resizing
            im_list_resize = [cv2.resize(img,
                            (int(img.shape[1] * h_min / img.shape[0]),
                                h_min), interpolation
                                        = interpolation) 
                            for img in img_list]
            im_concat = cv2.hconcat(im_list_resize)
            file_name = f'concat_image{concat_image_index}.jpg'
            cv2.imwrite(file_name, im_concat)
        else:
            division_smaller = len_img_list // 2
            division_larger = len_img_list - division_smaller

            im_list_resize_1 = [cv2.resize(img,
                            (int(img.shape[1] * h_min / img.shape[0]),
                                h_min), interpolation
                                        = interpolation) 
                            for img in img_list[:division_larger]]
            im_list_resize_2 = [cv2.resize(img,
                            (int(img.shape[1] * h_min / img.shape[0]),
                                h_min), interpolation
                                        = interpolation) 
                            for img in img_list[division_larger:]]
            im_concat1 = cv2.hconcat(im_list_resize_1)
            im_concat2 = cv2.hconcat(im_list_resize_2)
            file_name_1 = f'concat_image{concat_image_index}.jpg'
            file_name_2 = f'concat_image{concat_image_index + 1}.jpg'
            cv2.imwrite(file_name_1, im_concat1)
            cv2.imwrite(file_name_2, im_concat2)
    
    def modify_media_lists(
        self,
        img_file_list,
        file_name_list,
        discord_file_list,
        concat_image_index):
        len_img_file_list = len(img_file_list)
        h_min = self.generate_hconcat_minimum_height(
            img_file_list
        )
        self.generate_hconcat_resize_image_file(
            img_file_list,
            h_min,
            concat_image_index
        )
        if len_img_file_list > 4:
            file_name_list.append(f'concat_image{concat_image_index}.jpg')
            file_name_list.append(f'concat_image{concat_image_index + 1}.jpg')
            discord_file_list += [
                discord.File(fp=f'concat_image{concat_image_index}.jpg'),
                discord.File(fp=f'concat_image{concat_image_index + 1}.jpg')
            ]
        else:
            file_name_list.append(f'concat_image{concat_image_index}.jpg')
            discord_file_list.append(
                discord.File(f'concat_image{concat_image_index}.jpg')
            )
    
    def send_recent_post2(self, discord_webhook, discord_json):
        description = next(iter(discord_json.keys()))
        media_url_dict = list(discord_json.values())[0]
        file_name_list = []
        discord_files = []

        media_index = 1
        concat_image_index = 1
        img_file_name_list = []
        for key, value in media_url_dict.items():
            media_index_str = str(media_index)
            if value == 'IMAGE':
                file_name = f'insta_thing{media_index_str}.jpg'
                urllib.request.urlretrieve(
                    key,
                    file_name
                )
                img_file_name_list.append(file_name)
            else:
                if img_file_name_list:
                    len_file_name_list = len(file_name_list)
                    self.modify_media_lists(
                        img_file_name_list,
                        file_name_list,
                        discord_files,
                        concat_image_index
                    )
                    concat_image_index += len(file_name_list) - len_file_name_list
                    img_file_name_list = []
                file_name = f'insta_thing{media_index_str}.mp4'
                urllib.request.urlretrieve(
                    key,
                    file_name
                )
                discord_files.append(
                    discord.File(fp=file_name)
                )

            file_name_list.append(file_name)
            media_index += 1
    
        if img_file_name_list:
            self.modify_media_lists(
                img_file_name_list,
                file_name_list,
                discord_files,
                concat_image_index
            )
        
        discord_webhook.send(
            content=description,
            files=discord_files
        )
        for file in file_name_list:
            os.remove(file)
    
    def send_recent_post(self, discord_webhook, discord_json):
        description = next(iter(discord_json.keys()))
        media_url_dict = list(discord_json.values())[0]
        files_list = []
        discord_files = []

        media_index = 1
        for key, value in media_url_dict.items():
            media_index_str = str(media_index)
            if value == 'IMAGE':
                file_name = f'insta_thing{media_index_str}.jpg'
            else:
                file_name = f'insta_thing{media_index_str}.mp4'
            files_list.append(file_name)
            urllib.request.urlretrieve(
                key,
                file_name
            )
            discord_files.append(
                discord.File(fp=file_name)
            )
            media_index += 1

        discord_webhook.send(
            content=description,
            files=discord_files
        )
        for file in files_list:
            os.remove(file)

    def instagram_webhook(self):
        instagram_webhook = os.getenv('INSTAGRAM_WEBHOOK_URL')
        instagram_access_token = os.getenv('INSTAGRAM_API_DEV_TOKEN')
        discord_webhook = discord.Webhook.from_url(
            instagram_webhook,
            adapter=discord.RequestsWebhookAdapter()
        )
        while True:
            current_number_of_posts = self.get_number_of_posts(
                self.instagram_user
            )
            try:
                if self.number_of_posts != current_number_of_posts:
                    recent_post = self.get_most_recent_post(instagram_access_token)
                    recent_post_json = self.process_recent_post(recent_post)
                    self.send_recent_post2(discord_webhook, recent_post_json)
                    self.number_of_posts = current_number_of_posts
                    print('execution successful!')
                else:
                    print('no new post :(')
            except Exception as err:
                print('connectivity issues. sorry try again!')
                print(err)
            sleep(60)


if __name__ == '__main__':
    FirstFruitsx = FirstFruits('mikpillihp')
    # posts = FirstFruitsx.get_profile_posts('firstfruitscbccoc')
    # print(FirstFruitsx.get_most_recent_post(posts))
    print(FirstFruitsx.get_number_of_posts('mikpillihp'))
    print(FirstFruitsx.number_of_posts)
    FirstFruitsx.instagram_webhook()

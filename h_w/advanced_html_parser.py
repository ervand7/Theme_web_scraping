from pprint import pprint  # Do not delete this! It is for checking with examples below
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class AdvancedHtmlParser:
    def __init__(self, *args):
        self.keywords = args
        self.response_from_main_url = requests.get('https://habr.com/ru/all')
        self.soup_for_resp_from_main_url = BeautifulSoup(self.response_from_main_url.text, 'html.parser')
        self.list_of_posts_descriptions = self.soup_for_resp_from_main_url.find_all('h2', class_='post__title')
        self.links = [post.find('a', class_='post__title_link').attrs.get('href') for post in
                      self.list_of_posts_descriptions]

        for link in tqdm(self.links):
            inner_response = requests.get(link)
            inner_soup = BeautifulSoup(inner_response.text, 'html.parser')
            inner_posts = inner_soup.find_all('div', class_='post__text post__text_v2')
            inner_posts_text_lower = list(map(lambda x: x.text.strip().lower(), inner_posts))
            for inner_post in inner_posts_text_lower:
                if any(key_word in str(inner_post) for key_word in self.keywords):
                    post_publication_date = self.getting_post__time(link)
                    post_link = self.getting_post__title_link(link)
                    post_title = self.getting_post__title_text(link)
                    print(f'date: {post_publication_date}, title: "{post_title}", link: {post_link}')
                    break

    @staticmethod
    def getting_post__time(url):
        response_from_every_link = requests.get(url)
        soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
        return soup_for_resp_from_every_link.find('span', class_='post__time').text.strip()

    @staticmethod
    def getting_post__title_link(url):
        response_from_every_link = requests.get(url)
        soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
        return soup_for_resp_from_every_link.find('link', rel='canonical').attrs.get('href')

    @staticmethod
    def getting_post__title_text(url):
        response_from_every_link = requests.get(url)
        soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
        return soup_for_resp_from_every_link.find('span', class_='post__title-text').text.strip()


if __name__ == '__main__':
    experimental = AdvancedHtmlParser('программист', 'регуляр')
# ______________________________________________________________


# ______________________________________________________________
# # # # ||||||||||||| a variant where all in global scope |||||||||||||
# # # # it's very comfortable for manual debugging

# import requests
# from bs4 import BeautifulSoup
# from pprint import pprint

# keywords = ['сервис', 'программист']
# response_from_main_url = requests.get('https://habr.com/ru/all')
# soup_for_resp_from_main_url = BeautifulSoup(response_from_main_url.text, 'html.parser')
#
# list_of_posts_descriptions = soup_for_resp_from_main_url.find_all('h2', class_='post__title')
#
#
# # pprint(list_of_posts_descriptions)
#
#
# def getting_post__time(url):
#     response_from_every_link = requests.get(url)
#     soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
#     return soup_for_resp_from_every_link.find('span', class_='post__time').text.strip()
#
#
# def getting_post__title_link(url):
#     response_from_every_link = requests.get(url)
#     soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
#     return soup_for_resp_from_every_link.find('link', rel='canonical').attrs.get('href')
#
#
# def getting_post__title_text(url):
#     response_from_every_link = requests.get(url)
#     soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
#     return soup_for_resp_from_every_link.find('span', class_='post__title-text').text.strip()
#
#
# links = [post.find('a', class_='post__title_link').attrs.get('href') for post in list_of_posts_descriptions]
# # pprint(links)
# for link in tqdm(links):
#     inner_response = requests.get(link)
#     # print(inner_response)
#     inner_soup = BeautifulSoup(inner_response.text, 'html.parser')
#     # print(inner_soup)
#     inner_posts = inner_soup.find_all('div', class_='post__text post__text_v2')
#     # print(inner_posts)
#     # print(f'\n\n\n\n')
#     inner_posts_text_lower = list(map(lambda x: x.text.strip().lower(), inner_posts))
#     # print(inner_posts_text_lower)
#     # print(f'\n\n\n\n')
#     for inner_post in inner_posts_text_lower:
#         if any(key_word in str(inner_post) for key_word in keywords):
#             post_publication_date = getting_post__time(link)
#             post_link = getting_post__title_link(link)
#             post_title = getting_post__title_text(link)
#             print(f'date: {post_publication_date}, title: "{post_title}", link: {post_link}')
#             break
# ______________________________________________________________


# ______________________________________________________________
# # # # ||||||||||||| a variant with functions and without classes |||||||||||||

# def advanced_html_parser(*args):  # 'хакер', 'алгоритм', 'сервис'
#     keywords = args
#     response_from_main_url = requests.get('https://habr.com/ru/all')
#     soup_for_resp_from_main_url = BeautifulSoup(response_from_main_url.text, 'html.parser')
#     list_of_posts_descriptions = soup_for_resp_from_main_url.find_all('h2', class_='post__title')
#
#     def getting_post__time(url):
#         response_from_every_link = requests.get(url)
#         soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
#         return soup_for_resp_from_every_link.find('span', class_='post__time').text.strip()
#
#     def getting_post__title_link(url):
#         response_from_every_link = requests.get(url)
#         soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
#         return soup_for_resp_from_every_link.find('link', rel='canonical').attrs.get('href')
#
#     def getting_post__title_text(url):
#         response_from_every_link = requests.get(url)
#         soup_for_resp_from_every_link = BeautifulSoup(response_from_every_link.text, 'html.parser')
#         return soup_for_resp_from_every_link.find('span', class_='post__title-text').text.strip()
#
#     links = [post.find('a', class_='post__title_link').attrs.get('href') for post in list_of_posts_descriptions]
#
#     for link in tqdm(links):
#         inner_response = requests.get(link)
#         inner_soup = BeautifulSoup(inner_response.text, 'html.parser')
#         inner_posts = inner_soup.find_all('div', class_='post__text post__text_v2')
#         inner_posts_text_lower = list(map(lambda x: x.text.strip().lower(), inner_posts))
#         for inner_post in inner_posts_text_lower:
#             if any(key_word in str(inner_post) for key_word in keywords):
#                 post_publication_date = getting_post__time(link)
#                 post_link = getting_post__title_link(link)
#                 post_title = getting_post__title_text(link)
#                 print(f'date: {post_publication_date}, title: "{post_title}", link: {post_link}')
#                 break
#
#
# advanced_html_parser('сервис', 'программист')

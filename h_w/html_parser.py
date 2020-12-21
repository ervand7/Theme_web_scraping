import requests
from bs4 import BeautifulSoup
from pprint import pprint
from tqdm import tqdm


def html_parsing(*args):
    list_of_selected_articles = []
    keywords = args
    resp = requests.get('https://habr.com/ru/all')
    soup = BeautifulSoup(resp.text, 'html.parser')

    posts = soup.find_all('article', class_='post post_preview')
    # print(posts)
    for post in tqdm(posts):
        # print(post)
        previews = post.find_all('div', class_='post__text_v2')
        # print(previews)
        previews_text = list(map(lambda x: x.text.strip().lower(), previews))
        # print(previews_text)
        for preview_text in previews_text:
            # pprint(preview_text)
            if any(key_word in preview_text for key_word in keywords):
                date = post.find('span', class_='post__time').text.strip()
                our_link = post.find('a', class_='post__title_link')
                our_link_link = our_link.attrs.get('href')
                our_link_text = our_link.text.strip()
                row_ = f'date: {date}, heading: "{our_link_text}", link: {our_link_link}'
                list_of_selected_articles.append(row_)
                break
    return pprint([i for i in list_of_selected_articles])


if __name__ == '__main__':
    html_parsing('криптографическая', 'в', 'неочевидным', 'злоумышленников', 'сервис')
# ______________________________________________________________


# ______________________________________________________________
# Variant with global scope
# keywords = ['криптографическая', 'тысячи', 'неочевидным', 'злоумышленников', 'программисты']
# resp = requests.get('https://habr.com/ru/all')
# soup = BeautifulSoup(resp.text, 'html.parser')
#
# posts = soup.find_all('article', class_='post post_preview')
# # print(posts)
# for post in posts:
#     # print(post)
#     previews = post.find_all('div', class_='post__text_v2')
#     # print(previews)
#     previews_text = list(map(lambda x: x.text.strip().lower(), previews))
#     # print(previews_text)
#     for preview_text in previews_text:
#         # pprint(preview_text)
#         if any(key_word in preview_text for key_word in keywords):
#             date = post.find('span', class_='post__time').text.strip()
#             our_link = post.find('a', class_='post__title_link')
#             our_link_link = our_link.attrs.get('href')
#             our_link_text = our_link.text.strip()
#             print(f'date: {date}, heading: "{our_link_text}", link: {our_link_link}')
#             break

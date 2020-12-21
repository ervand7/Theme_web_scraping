# Парсим https://2ip.ru
# вариант с requests и без BeautifulSoup
import requests
from bs4 import BeautifulSoup

response = requests.get('https://2ip.ru')
index_id = response.text.index('id="d_clip_button"')  # <div class="ip" id="d_clip_button" style="cursor: pointer;">
# <span>93.157.169.19</span><i class="ip-icon-shape btn-copy"></i></div>
# 1) ищем открывающий тег span:
index_span = response.text.index('<span>', index_id)  # index(self, sub, start=None, end=None) -
# тут мы прописываем что искать ('<span>') и начиная с какой позиции (index_id)
# 2) ищем закрывающий тег span:
index_span_end = response.text.index('</span>', index_id)

# print(response.text[index_span + 6:index_span_end])  # поскольку индекс будет возвращаться с самого начала
# строки '</span>', то мы должны пропустить эти символы именования тега
# ____________________________________________________


# ____________________________________________________
# Парсим https://2ip.ru
# вариант с requests + BeautifulSoup
response2 = requests.get('https://2ip.ru')
# формируем наше дерево с детьми
soup = BeautifulSoup(response2.text, 'html.parser')  # здесь response2.text - это HTML разметка
# по умолчанию в BeautifulSoup стоит html.parser, но мы все равно каждый раз должны его указывать
element = soup.find(id="d_clip_button")

# print(element.text.strip())  # а здесь element.text - это визуальный текст для каждого элемента
# ____________________________________________________


# ____________________________________________________
# Парсим https://habr.com/ru/ и ищем все статьи, в которых есть один из след хабов:
# 'devops', 'фото', 'laravel', 'криптография'
# нам нужно название, ссылка и дата выпуска (в конце еще
# и react добавим для того, чтобы понять, зачем нам break нужен
DESIRED_HUBS = ['devops', 'фото', 'laravel', 'криптография', 'react']
resp = requests.get('https://habr.com/ru/all')
soup2 = BeautifulSoup(resp.text, 'html.parser')

# извлекаем посты
# здесь будем использовать find_all, а не find, так как find возвращает нам только первое вхождение,
# а find_all будет нам возвращать все вхождения
# первым параметром мы указываем тег. Если не укажем, то он будет пытаться найти среди всех тегов
posts = soup2.find_all('article', class_='post')  # очень важно писать class_ -  это требование библиотеки
for post in posts:
    # print(post)
    # теперь в рамках каждого поста нам нужно найти вообще все хабы которые есть
    # это у нас будут ссылки, которые находятся внутри тега <li> у которого class_='inline-list__item_hub'
    hubs = post.find_all('li', class_='inline-list__item_hub')
    # print(hubs)

    # _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    # сейчас чисто для пробы попробуем вывести только чисто списки (text)  с хабами
    # функция map делает преобразование для каждого элемента
    # в данном случае функция берет x и делает с ним x.text.strip().lower(), и все это происходит
    # списке hubs. Мы все переводим в нижний регистр чтобы не париться с написанием забов
    # в DESIRED_HUBS, чтобы избежать ошибок связвнных с регистрами
    hubs_text = list(map(lambda x: x.text.strip().lower(), hubs))
    # print(hubs_text)
    # # # с помощью map мы заменяем эти 4 строки кода:
    # hubs_text = []
    # for hub in hubs:
    #     hubs_text.append(hub.text.strip())
    # print(hubs_text)
    # _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    for hub_text in hubs_text:
        # нам нужно, чтобы хотя бы один из этих хабов ('devops', 'фото', 'laravel', 'криптография')
        # присутствовал внутри списка hub_text
        # функция any проверяет, чтобы хотя бы один из элементов был истинным
        if any(one_hub in hubs_text for one_hub in DESIRED_HUBS):
            date = post.find('span', class_='post__time').text.strip()  # если мы раньше
            # использовали post.find_all(), то сейчас, поскольку нам нужно только первое вхождение,
            # мы уже будем использовать просто find()
            our_link = post.find('a', class_='post__title_link')
            our_link_link = our_link.attrs.get('href')
            our_link_text = our_link.text.strip()

            print(date, our_link_link, our_link_text)
            break  # если мы тут не поставим break, то в некоторых ситуациях будет
            # дублироваться так как в одной статье может быть несколько подходящтх
            # нам хабов, на которые может отреагировать наш парсер
        # else:
        #     print('Таких хабов не обнаружено')
# ____________________________________________________


# ____________________________________________________
# Код с презентации
# # определяем список хабов, которые нам интересны
# DESIRED_HUBS = ['дизайн', 'фото', 'web', 'python']
# # получаем страницу с самыми свежими постами
# ret = requests.get('https://habr.com/ru/all/')
# soup = BeautifulSoup(ret.text, 'html.parser')
#
# # извлекаем посты
# posts = soup.find_all('article', class_='post')
# for post in posts:
#     post_id = post.parent.attrs.get('id')
#     # если идентификатор не найден, это что-то странное, пропускаем
#     if not post_id:
#         continue
#     post_id = int(post_id.split('_')[-1])
#     print('post', post_id)
#
#     # извлекаем хабы поста
#     hubs = post.find_all('a', class_='hub-link')
#     for hub in hubs:
#         hub_lower = hub.text.lower()
#         # ищем вхождение хотя бы одного желаемого хаба
#         if any([hub_lower in desired for desired in DESIRED_HUBS]):
#             title_element = post.find('a', class_='post__title_link')
#             print(title_element.text, title_element.attrs.get('href'))
#             break

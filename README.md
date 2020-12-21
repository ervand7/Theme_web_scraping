![Bootstrap](https://hackernoon.com/hn-images/0*pp7uaEHrKY5iiWw9)
# Homework for lecture 6. "Web-scrapping"
Let's try to get the articles of interest to us on Habré the very first :)

1. It is necessary to parse the page with fresh articles ([this one](https://habr.com/ru/all/)) and select those articles in which at least one of the keywords is found (we define these words at the beginning of the script). Search for all available preview-information (this is information available directly from the current page). Output to the console a list of matching articles in the format: < date > - < heading > - < link >.

```python
# define a list of keywords
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Your code
```

2. Improve the script so that it analyzes not only the preview information of the article, but also the entire text of the article.
This will require retrieving article pages and searching for text within that page.
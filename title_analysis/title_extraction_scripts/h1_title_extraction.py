import pandas as pd
import pyppeteer.errors
import requests_html
from bs4 import BeautifulSoup
from tqdm import tqdm

session = requests_html.HTMLSession()
df = pd.read_csv('../datasets/news_urls.csv', sep=';')
data = {
    'url': [],
    'h1_title_result': []
}
results_df = pd.DataFrame(data)


def extract_title(site_url):
    response = session.get(site_url)
    try:
        response.html.render(timeout=20)
    except pyppeteer.errors.PageError:
        return " "
    except requests_html.MaxRetries:
        return " "
    soup = BeautifulSoup(response.html.html, 'html.parser')
    headlines = []
    for headline in soup.find_all('h1'):
        headlines.append(headline.text)
    if len(headlines) > 0:
        result = max(headlines, key=len)
        if "data" in result:
            soup = BeautifulSoup(response.html.html, 'html.parser')
            for headline in soup.find_all('title'):
                headlines.append(headline.text)
            if len(headlines) > 0:
                return max(headlines, key=len)
        return result
    soup = BeautifulSoup(response.html.html, 'html.parser')
    for headline in soup.find_all('title'):
        headlines.append(headline.text)
    if len(headlines) > 0:
        return max(headlines, key=len)



try:
    with tqdm(total=len(df)) as pbar:
        for row in df.itertuples(index=True):
            extracted_title = extract_title(row.url)
            new_row = {'url': row.url, 'h1_title_result': extracted_title}
            results_df.loc[len(results_df)] = new_row
            pbar.update(1)
finally:
    pbar.close()
    results_df.to_csv('./results/h1_title_extracted.csv', sep=';', index=False)

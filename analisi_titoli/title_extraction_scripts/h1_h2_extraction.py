import requests_html
import pyppeteer.errors
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

session = requests_html.HTMLSession()
df = pd.read_csv('../datasets/news_urls.csv', sep=';')
data = {
    'url': [],
    'h1_h2_result': []
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
        return max(headlines, key=len)
    soup = BeautifulSoup(response.html.html, 'html.parser')
    for headline in soup.find_all('h2'):
        headlines.append(headline.text)
    if len(headlines) > 0:
        return max(headlines, key=len)


try:
    with tqdm(total=len(df)) as pbar:
        for row in df.itertuples(index=True):
            extracted_title = extract_title(row.url)
            new_row = {'url': row.url, 'h1_h2_result': extracted_title}
            results_df.loc[len(results_df)] = new_row
            pbar.update(1)
finally:
    pbar.close()
    results_df.to_csv('./results/h1_h2_extracted.csv', sep=';', index=False)

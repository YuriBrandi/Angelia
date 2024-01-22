import asyncio
import pandas as pd
import pyppeteer.errors
from pyppeteer import launch


async def main(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3419.0 Safari/537.36')
    await page.goto(url=url)

    await page.waitForFunction('() => document.readyState === "complete"')

    time_tag_info = None

    time_tag_info = await page.evaluate('''() => {
                const timeElement = document.querySelector('time');
                if (timeElement) {
                    const datetimeAttr = timeElement.getAttribute('datetime');
                    const textContent = timeElement.textContent;
                    return { datetime: datetimeAttr, textContent: textContent };
                }
                return null;
            }''')

    datetime_value = None

    if time_tag_info:
        datetime_value = time_tag_info['datetime'] or time_tag_info['textContent']

    await browser.close()
    return datetime_value


df = pd.read_csv('csv/FakeNewsTopicLinkDataset.csv')
df['Date'] = [None] * df.shape[0]

for i in range(0, df.shape[0]):
    try:
        print(i)
        url = df.loc[i]['Link']
        datetime_value = asyncio.get_event_loop().run_until_complete(main(url))
        df.loc[i]['Date'] = datetime_value
    except pyppeteer.errors.PageError:
        pass
    except Exception as e:
        pass

df.to_csv('csv/FakeNewsTopicLinkDateDataset.csv', index=False)

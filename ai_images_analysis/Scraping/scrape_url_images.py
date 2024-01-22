import asyncio
import pandas as pd
from pyppeteer import launch


async def main(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3419.0 Safari/537.36')
    await page.goto(url, {'timeout': 60000})

    await page.waitForFunction('() => document.readyState === "complete"')

    img_src = await page.evaluate('''() => {
            const imgElements = document.querySelectorAll('img');
            return Array.from(imgElements).map(img => {
                return {
                    src: img.src,
                    width: img.width,
                    height: img.height
                };
            });
        }''')

    new_img_src = [img['src'] for img in img_src if img['width'] >= 32 and img['height'] >= 32]
    await browser.close()
    return new_img_src


df = pd.read_csv('csv/FakeNewsTopicLinkDateDataset.csv')
df['Images_url'] = [None] * df.shape[0]

for i in range(0, df.shape[0]):
    print(i)
    try:
        url = df.loc[i]['Link']
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        images_url = asyncio.get_event_loop().run_until_complete(main(url))
        if len(images_url) > 0:
            images_url = [img for img in images_url if img.startswith('http') or img.startswith('https')]
            df.loc[i, 'Images_url'] = 'SEPARATORLINK'.join(images_url)
    except Exception as e:
        print(e)

df.to_csv('csv/FakeNewsTopicLinkDateImagesUrlDataset.csv', index=False)
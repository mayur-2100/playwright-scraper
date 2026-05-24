import asyncio
import json
import os
from playwright.async_api import async_playwright

TARGET_URL = os.environ.get('TARGET_URL', 'https://books.toscrape.com')
OUTPUT_FILE = 'output.json'

async def scrape_products(url: str) -> list:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"Navigating to {url}")
        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        products = []
        items = await page.query_selector_all('article.product_pod')

        for item in items:
            try:
                name  = await item.query_selector('h3 a')
                price = await item.query_selector('.price_color')
                avail = await item.query_selector('.availability')
                rating = await item.query_selector('p.star-rating')

                products.append({
                    "name":         await name.get_attribute('title') if name else None,
                    "price":        (await price.inner_text()).strip() if price else None,
                    "availability": (await avail.inner_text()).strip() if avail else None,
                    "rating":       await rating.get_attribute('class') if rating else None,
                })
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue

        await browser.close()
        return products

async def main():
    print("Starting scraper...")
    products = await scrape_products(TARGET_URL)
    print(f"Scraped {len(products)} products")

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(products, f, indent=2)

    print(f"Output saved to {OUTPUT_FILE}")
    print(json.dumps(products[:3], indent=2))

if __name__ == '__main__':
    asyncio.run(main())
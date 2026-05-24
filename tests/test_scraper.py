import pytest
from scraper import scrape_products
import asyncio

@pytest.mark.asyncio
async def test_scrapes_products():
    products = await scrape_products('https://books.toscrape.com')
    assert len(products) > 0
    assert 'name' in products[0]
    assert 'price' in products[0]
    assert products[0]['name'] is not None

@pytest.mark.asyncio
async def test_product_has_required_fields():
    products = await scrape_products('https://books.toscrape.com')
    for p in products[:5]:
        assert 'name' in p
        assert 'price' in p
        assert 'availability' in p
import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_xiaohongshu_titles():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        # Go to Xiaohongshu explore/discover page
        await page.goto("https://www.xiaohongshu.com/explore", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        titles = []

        # Try to get video note items
        items = await page.query_selector_all('section.note-item, .reds-note, a[href*="/discovery/item/"], .feeds-page .note-item')
        print(f"Found {len(items)} items via selectors")

        # Try another approach: get all links that look like note links
        if len(items) == 0:
            links = await page.query_selector_all('a[href*="/explore/"]')
            print(f"Found {len(links)} explore links")

        # Get page content for debugging
        html = await page.content()
        with open("page_debug.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Try using evaluate to extract titles from the page
        titles = await page.evaluate('''() => {
            const results = [];
            // Try various selectors
            const selectors = [
                '.note-item .title',
                '.note-item .note-title',
                '.reds-note .title',
                '.feeds-page .note-item .title',
                '[class*="title"]',
                'a[class*="note"] span',
                '.card .title'
            ];
            for (const sel of selectors) {
                const els = document.querySelectorAll(sel);
                els.forEach(el => {
                    const text = el.textContent.trim();
                    if (text && text.length > 3 && text.length < 100) {
                        results.push(text);
                    }
                });
            }
            return [...new Set(results)];
        }''')

        await browser.close()
        return titles

if __name__ == "__main__":
    titles = asyncio.run(fetch_xiaohongshu_titles())
    print("=" * 60)
    print("小红书热门视频标题:")
    print("=" * 60)
    for i, title in enumerate(titles[:10], 1):
        print(f"{i}. {title}")
    print("=" * 60)

    # Save to file
    with open("小红书热门标题.txt", "w", encoding="utf-8") as f:
        f.write("小红书热门视频标题（前10条）\n")
        f.write("=" * 40 + "\n")
        for i, title in enumerate(titles[:10], 1):
            f.write(f"{i}. {title}\n")
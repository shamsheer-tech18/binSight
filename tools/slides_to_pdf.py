import pathlib
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox','--allow-file-access-from-files'])
        page = await b.new_page(viewport={'width':1920,'height':1080})
        await page.goto((pathlib.Path(__file__).resolve().parent/'slides.html').as_uri()); await page.wait_for_load_state('networkidle')
        await page.pdf(path=str(pathlib.Path(__file__).resolve().parent.parent/'docs'/'BinSight-Prototype-Journey-Slides.pdf'), width='1920px', height='1080px', print_background=True)
        await b.close()
asyncio.run(main())

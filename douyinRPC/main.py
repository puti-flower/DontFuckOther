import asyncio
from playwright.async_api import async_playwright
from playwright.async_api import Response, Request, Route


js = open("douyinRPC/stealth.min.js", "r", encoding="utf-8").read()
js_ws = open("douyinRPC/rpc.js", "r", encoding="utf-8").read()


async def handle_route(route: Route):
    if "8954.6ca5bd48.js" in route.request.url:
        await route.fulfill(body=js_ws)
    else:
        await route.continue_()


async def run(url):
    async with async_playwright() as playwright:
        chromium = await playwright.chromium.launch(headless=False)
        page = await chromium.new_page()
        await page.add_init_script(js)
        await page.route("**/*.js", handle_route)

        await page.goto(url)
        while 1:

            await asyncio.sleep(330 * 330)


async def main():
    tasks = []
    urls = ["https://live.douyin.com/218532104579"]
    for url in urls:
        task = asyncio.ensure_future(run(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

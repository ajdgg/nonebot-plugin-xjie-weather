import jinja2
from pathlib import Path
from .weather_img_data import weather_iaqamg
from playwright.async_api import async_playwright
weather_iaqamg = weather_iaqamg()


def weather_html(data, api_name: str):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    # env = jinja2.Environment(loader=template_loader)
    # aaa = str(Path(__file__).resolve().parent / "src/index.html")
    # template = env.get_template(aaa)
    current_dir = Path(__file__).resolve().parent
    template_loader = jinja2.FileSystemLoader(searchpath=str(current_dir))
    env = jinja2.Environment(loader=template_loader)
    # 假设 index.html 文件在 src 子目录下
    template_name = "src/index.html"
    template = env.get_template(template_name)

    if api_name == "AMAP":
        rendered_template = template.render(
            name=data['base']["city"],
            content=data['base']["weather-img"],
            temperature=data['base']["temperature"],
            time=data['base']["reporttime"],
            forecast=data['base']["blockdata"],
            lis=data["all"],)
    with open(Path(__file__).resolve().parent / "src/output.html", "w+", encoding="utf-8") as file:
        file.write(rendered_template)
    return "200"


# hasd = html(obj)


async def open_local_html():
    async with async_playwright() as p:
        # browser = p.chromium.launch(headless=False)
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        html_file_path = Path(__file__).resolve().parent / "src/output.html"
        await page.goto(f"file:///{html_file_path}")
        # await page.goto("https://youshou.wiki")
        await page.locator("#main").screenshot(path=Path(__file__).resolve().parent / "weatherforecast.png")
        print(await page.title())
        await browser.close()


# if hasd == "200":
#     open_local_html()

_data_obj = {}


class weather_img:
    def __init__(self) -> None:
        pass

    async def get_weather_img(self, data_all, data_base, api_name):
        if api_name == "AMAP":
            _data_obj["base"] = data_base
            _data_obj["all"] = data_all
            data_ha = weather_iaqamg.get_weather_getimg_data(_data_obj, "AMAP")
            hasd = weather_html(data_ha, api_name)
            if hasd == "200":
                await open_local_html()
            return "200"
        else:
            _data_obj["base"] = data_base
            _data_obj["all"] = data_all
            return _data_obj

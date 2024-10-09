'''
coding: UTF-8
Author: AwAjie
Date: 2024-07-09 19:31:08
'''
import jinja2
from pathlib import Path
from .weather_img_data import weather_iaqamg
from playwright.async_api import async_playwright
weather_iaqamg = weather_iaqamg()


def weather_html(data, data_type: str):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    current_dir = Path(__file__).resolve().parent
    template_loader = jinja2.FileSystemLoader(searchpath=str(current_dir))
    env = jinja2.Environment(loader=template_loader)

    template_name = "src/index.html"
    template = env.get_template(template_name)

    rendered_template = template.render(
        name=data_type,
        weather=data['base']["weather"],
        content=data['base']["weather_img"],
        temperature=data['base']["temp"],
        time=data['base']["obsTime"],
        forecast=data['base']["blockdata"],
        lis=data["all"])
    with open(Path(__file__).resolve().parent / "src/output.html", "w+", encoding="utf-8") as file:
        file.write(rendered_template)
    return "200"


# 新 new
async def open_local_html():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=1000)
        page = await browser.new_page()
        html_file_path = Path(__file__).resolve().parent / "src/output.html"
        await page.goto(f"file:///{html_file_path}")
        screenshot_image = await page.locator("#main").screenshot(type='png')
        print(await page.title())
        await browser.close()
        return screenshot_image


_data_obj = {}


class weather_img:
    def __init__(self) -> None:
        pass

    async def get_weather_img(self, data_all, data_base, api_name, city):
        _data_obj["base"] = data_base
        _data_obj["all"] = data_all
        data_ha = weather_iaqamg.get_weather_getimg_data(_data_obj, api_name)
        hasd = weather_html(data_ha, city)
        if hasd == "200":
            typeimg = await open_local_html()
            return ["200", typeimg]
        else:
            return ["error", "生成html失败"]

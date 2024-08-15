from typing import List


def is_all_booleans(lst):
    return all(isinstance(item, bool) for item in lst)


class HtmlModule:
    """
        HTML 模块
    """
    def humidity_html(self, humidity: str) -> str:
        """
        湿度
        """
        return f'''
                <div class="weather-chunk">
                    <div class="w-image qi-low-humidity2"></div>
                    <div class="humidness-data">{humidity}%</div>
                </div>
                '''

    def WDSP_html(self, wind_direction: str, wind_speed: str, isit: List = [True, True]) -> str:
        if len(isit) > 2 or len(isit) < 1 or isit == [True]:
            isit_i = [True, True]
        elif isit == [False]:
            isit_i = [False, False]
        else:
            isit_i = isit
        return f'''
                <div class="weather-chunk">
                    <div class="w-image qi-wind-chill-advisory"></div>
                    <div class="wind-data">{wind_direction}{"风" if isit_i[0] else ""}<span>{wind_speed}{"级" if isit_i[1] else ""}</span></div>
                </div>
                '''

    def body_surface_temperature_html(self, body_surface_temperature: str) -> str:
        return f'''
                <div class="weather-chunk">
                        <div class="w-image qi-high-temperature3"></div>
                        <div class="humidness-data">体感：{body_surface_temperature.replace("°C", "")}&#xe75b;</div>
                </div>
                '''

    def air_pressure_html(self, air_pressure: str) -> str:
        return f'''
                <div class="weather-chunk">
                    <div class="w-image xj-pressure"></div>
                    <div class="humidness-data">气压：{air_pressure}hPa</div>
                </div>
                '''

    def visibility_html(self, visibility: str) -> str:
        return f'''
                <div class="weather-chunk">
                    <div class="w-image xj-visibility"></div>
                    <div class="humidness-data">能见度：{visibility}/km</div>
                </div>
                '''

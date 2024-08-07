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

    def WDSP_html(self, wind_direction: str, wind_speed: str) -> str:
        return f'''
                <div class="weather-chunk">
                    <div class="w-image qi-wind-chill-advisory"></div>
                    <div class="wind-data">{wind_direction}风<span>{wind_speed}级</span></div>
                </div>
                '''

    def body_surface_temperature_html(self, body_surface_temperature: str) -> str:
        return f'''
                <div class="weather-chunk">
                        <div class="w-image qi-high-temperature3"></div>
                        <div class="humidness-data">体感：{body_surface_temperature}&#xe75b;</div>
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

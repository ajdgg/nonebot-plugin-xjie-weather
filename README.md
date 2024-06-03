<!--
 * @Author: AwAjie 139576615+ajdgg@users.noreply.github.com
 * @Date: 2024-06-02 18:54:27
 * @LastEditors: AwAjie 139576615+ajdgg@users.noreply.github.com
 * @LastEditTime: 2024-06-03 09:56:15
 * @FilePath: \nonebot-plugin-xjie-weather\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<div align="center">

<img width = "100px" src="https://www.freeimg.cn/i/2024/06/02/665c4cfd079d1.png">

# nonebot-plugin-xjie-weather

_✨一个 NoneBot 天气插件✨_

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<img alt="Static Badge" src="https://img.shields.io/badge/awajie-a?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0MzAuMzYgNDA0Ljc3Ij48ZGVmcz48c3R5bGU%2BLmNscy0xe2ZpbGw6I2ZmZjt9LmNscy0ye3N0cm9rZTojMDAwO3N0cm9rZS1taXRlcmxpbWl0OjEwO30uY2xzLTN7ZmlsbDojZGI1NjViO308L3N0eWxlPjwvZGVmcz48ZyBpZD0i5Zu%2B5bGCXzMiIGRhdGEtbmFtZT0i5Zu%2B5bGCIDMiPjxwYXRoIGQ9Ik0yOC4zNS4yNkgxOTMuNjhhMTIsMTIsMCwwLDEsMTIsMTJWNDQuOTVhMTIsMTIsMCwwLDEtMTIsMTJIMTJhMTIsMTIsMCwwLDEtMTItMTJWMjguNkEyOC4zNSwyOC4zNSwwLDAsMSwyOC4zNS4yNloiLz48cGF0aCBkPSJNMzg1LjQxLDBoMTYuMzVhMjguMzUsMjguMzUsMCwwLDEsMjguMzUsMjguMzVWMTE0YTEyLDEyLDAsMCwxLTEyLDEySDM4NS40MWExMiwxMiwwLDAsMS0xMi0xMlYxMkExMiwxMiwwLDAsMSwzODUuNDEsMFoiLz48cGF0aCBkPSJNMzI4LjM2LDM0Ni43NWg5MGExMiwxMiwwLDAsMSwxMiwxMnYxNi42NUEyOC4zNSwyOC4zNSwwLDAsMSw0MDIsNDAzLjc1SDMyOC4zNmExMiwxMiwwLDAsMS0xMi0xMnYtMzNBMTIsMTIsMCwwLDEsMzI4LjM2LDM0Ni43NVoiLz48cGF0aCBkPSJNMTIsMzQ3LjMxaDk4LjIzYTEyLDEyLDAsMCwxLDEyLDEyVjM5MmExMiwxMiwwLDAsMS0xMiwxMkgyOC4zNUEyOC4zNSwyOC4zNSwwLDAsMSwwLDM3NS42NlYzNTkuMzFhMTIsMTIsMCwwLDEsMTItMTJaIi8%2BPHJlY3QgeD0iMTQ2Ljk4IiB5PSIxMjYiIHdpZHRoPSI1Ni42OSIgaGVpZ2h0PSIxMzcuODciIHJ4PSIxMiIvPjxwYXRoIGQ9Ik0yNDQuNDMsMjc5LjQzaC00MS4ybC0uNDEsMC0uNCwwSDgzLjY0YTEyLDEyLDAsMCwwLTEyLDEydjMyLjY5YTEyLDEyLDAsMCwwLDEyLDEySDI0NC40M2ExMiwxMiwwLDAsMCwxMi0xMlYyOTEuNDNBMTIsMTIsMCwwLDAsMjQ0LjQzLDI3OS40M1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC03MS42NCAtNzIuMjUpIi8%2BPHBhdGggZD0iTTIwMy4yMywyNzkuNDNoLS44MWwuNCwwWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTcxLjY0IC03Mi4yNSkiLz48cGF0aCBkPSJNMjE4LjYyLDI2MC4wNXYzLjQ3czAsLjA4LDAsLjEyYTE1LjgxLDE1LjgxLDAsMCwxLTE1LjgxLDE1LjgxbC0uNTYsMGgtMy42MXYxOS40MUgyNDJWMjYwLjA1WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTcxLjY0IC03Mi4yNSkiLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0yMDMuNjMsMjc5LjQzdjBsLS40LDBaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNzEuNjQgLTcyLjI1KSIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTIxOC42MiwyNjMuNzJjMCwuMDgsMCwuMTUsMCwuMjNoMFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC03MS42NCAtNzIuMjUpIi8%2BPHJlY3QgeD0iMzI1LjY3IiB3aWR0aD0iNzYuMDkiIGhlaWdodD0iNTYuNjkiIHJ4PSIxMiIvPjxyZWN0IHg9IjAuNDQiIHk9IjIyLjcyIiB3aWR0aD0iNTYuNjkiIGhlaWdodD0iNTcuNTgiIHJ4PSIxMiIvPjxyZWN0IGNsYXNzPSJjbHMtMiIgeD0iMzcyLjg2IiB5PSIyODUuMjUiIHdpZHRoPSI1NyIgaGVpZ2h0PSIxMDEiIHJ4PSIxMiIvPjwvZz48ZyBpZD0i5Zu%2B5bGCXzQiIGRhdGEtbmFtZT0i5Zu%2B5bGCIDQiPjxjaXJjbGUgY2xhc3M9ImNscy0zIiBjeD0iMjY3LjY5IiBjeT0iNDAuMTUiIHI9IjQwLjE1Ii8%2BPHJlY3QgY2xhc3M9ImNscy0zIiB4PSIyMzYuMzYiIHk9IjE1MC43NSIgd2lkdGg9IjcxLjQ4IiBoZWlnaHQ9IjE3OC4yNSIgcng9IjEyIi8%2BPHJlY3QgY2xhc3M9ImNscy0zIiB4PSIyMTYuMzYiIHk9IjEyNiIgd2lkdGg9IjkxLjQ4IiBoZWlnaHQ9IjQ5LjUiIHJ4PSIxMiIvPjxwYXRoIGNsYXNzPSJjbHMtMyIgZD0iTTI2MC4yNSwzNTYuNUgyMTUuOTRhMTIsMTIsMCwwLDAtMTIsMTJ2MzMuMTVsLjI4LDIuNjdhMTIuMDYsMTIuMDYsMCwwLDAsMTEuNzIsOS40M2g0NC4zMWExMiwxMiwwLDAsMCwxMi0xMlYzNjguNUExMiwxMiwwLDAsMCwyNjAuMjUsMzU2LjVaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNzEuNjQgLTcyLjI1KSIvPjxwYXRoIGNsYXNzPSJjbHMtMyIgZD0iTTIwMy45NCw0MDEuNzVhMTIuMTIsMTIuMTIsMCwwLDAsLjI4LDIuNTdsLS4yOC0yLjY3WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTcxLjY0IC03Mi4yNSkiLz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik0zMDcuOTIsMzg4LjUyYTE3LjI2LDE3LjI2LDAsMCwxLC4xNywyLjI5LDE4LDE4LDAsMCwxLTM2LjA5LDAsMTkuMTQsMTkuMTQsMCwwLDEsLjE2LTIuMjlIMjAzLjk0djEzLjEzbC42LDUuNThDMjEzLjIyLDQ0Ni45MiwyNDguODYsNDc3LDI5MSw0NzdjNDguNTUsMCw4OC40OS0zOS45NCw4OC40OS04OC40OVoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC03MS42NCAtNzIuMjUpIi8%2BPHJlY3QgY2xhc3M9ImNscy0zIiB4PSIxOTAuNzIiIHk9IjMwOC4zOCIgd2lkdGg9IjkuODkiIGhlaWdodD0iMjMuNDkiLz48cmVjdCBjbGFzcz0iY2xzLTMiIHg9IjIzNi4zNiIgeT0iMzA1LjM4IiB3aWR0aD0iNC45IiBoZWlnaHQ9IjIxLjc5Ii8%2BPHJlY3QgY2xhc3M9ImNscy0xIiB4PSIyMzUuNzEiIHk9IjMxMy45NiIgd2lkdGg9IjAuNjUiIGhlaWdodD0iMy43Ii8%2BPHBhdGggY2xhc3M9ImNscy0zIiBkPSJNMzE4LjEsMjQwLjg5SDI5OC44OHY2LjhsLjU3LjA3aDBhOC44OSw4Ljg5LDAsMCwxLDguNTYsOC44OWMwLC4xNCwwLC4yOCwwLC40MnYyLjMzSDMxOC4xWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTcxLjY0IC03Mi4yNSkiLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0zMDgsMjU2LjIxaDBjMCwuMDcsMCwuMTMsMCwuMTlaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNzEuNjQgLTcyLjI1KSIvPjwvZz48L3N2Zz4%3D&labelColor=fbf2e3&color=%23161823">


</div>

<!-- # 安装

- 使用 nb-cli

```
nb plugin install nonebot-plugin-xjie-weather
```

- 使用 pip

```
pip install nonebot-plugin-xjie-weather
``` -->
<style>
    #yes{
        text-align: center;
        background-color: green;
    }
    #no{
        text-align: center;
        background-color: red;
    }
</style>

# 支持
目前支持

| API              | 是否支持    |
| :--------------: | :--------: |
| 高德天气         | 支持✅     |
| 和风天气         | 未完成❌   |
| Visual Crossing | 未完成❌   |
| 心知天气         | 未完成❌  |


# 配置
### 一
- 使用交互式设置key
### 二
- 在插件中找到```xjie_data.json```文件直接写入key
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
import discord
import time

async def capturar_grafico_guilda():
    url = "https://www.fflogs.com/embed/guild-progress-tile/68?difficulty=101&guild=135735"

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1000,700")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(3)

        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))

        # Tamanho do crop desejado
        crop_width = 850
        crop_height = 450
        width, height = image.size

        # Deslocamento manual (ajuste fino)
        offset_x = -70  # mover 50px para a esquerda
        offset_y = -55  # mover 30px para cima

        # Cálculo com deslocamento, mantendo dentro dos limites
        left = max((width - crop_width) // 2 + offset_x, 0)
        top = max((height - crop_height) // 2 + offset_y, 0)
        right = left + crop_width
        bottom = top + crop_height

        cropped_image = image.crop((left, top, right, bottom))

        img_buffer = io.BytesIO()
        cropped_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        return discord.File(fp=img_buffer, filename="guild_chart_cropped.png")

    finally:
        driver.quit()

import requests
import warnings
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

# --------------------- Функции обновления и объявлений ---------------------
def check_for_updates():
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/version.txt"
        )
        remote_version = r.content.decode('utf-8').strip()
        local_version = open('version.txt', 'r').read().strip()
        if remote_version != local_version:
            print("A new version is available. Please download the latest version from GitHub.")
            time.sleep(3)
            return False
        return True
    except:
        return True

def get_announcement():
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/announcement.txt",
            headers={"Cache-Control": "no-cache"}
        )
        return r.content.decode('utf-8').strip()
    except:
        return "No announcement available."

# --------------------- Основная функция ---------------------
def main():
    if not check_for_updates():
        return

    announcement = get_announcement()

    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
       
                       ▄█   ▄█▄  ▄█    ▄████████    ▄█    █▄     ▄█  
                       ███ ▄███▀ ███   ███    ███   ███    ███   ███  
                       ███▐██▀   ███▌  ███    █▀    ███    ███   ███▌ 
                      ▄█████▀    ███▌  ███         ▄███▄▄▄▄███▄▄ ███▌ 
                     ▀▀█████▄    ███▌  ███        ▀▀███▀▀▀▀███▀  ███▌ 
                       ███▐██▄   ███   ███    █▄    ███    ███   ███  
                       ███ ▀███▄ ███   ███    ███   ███    ███   ███  
                       ███   ▀█▀ █▀    ████████▀    ███    █▀    █▀   
                       ▀                                             
Improvements can be made to the code. If you're getting an error, visit my discord.
Discord discord.gg/u4T67NU6xb    
Github  github.com/kichi779
    """)))

    print("")
    print(Colors.red, Center.XCenter("ANNOUNCEMENT"))
    print(Colors.yellow, Center.XCenter(f"{announcement}"))
    print("")

    # --------------------- Настройка прокси ---------------------
    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    proxy_choice = int(os.getenv("PROXY_CHOICE", 1))
    twitch_username = os.getenv("TWITCH_USERNAME", "Kichi779")
    proxy_count = int(os.getenv("PROXY_COUNT", 3))

    proxy_url = proxy_servers.get(proxy_choice, proxy_servers[1])

    print(Colorate.Vertical(Colors.green_to_blue,
        f"Using Proxy Server {proxy_choice}: {proxy_url}"))
    print(Colorate.Vertical(Colors.cyan_to_blue,
        f"Channel: {twitch_username} | Windows of proxy to open: {proxy_count}"))

    # --------------------- Настройка undetected-chromedriver ---------------------
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser"  # путь к Chromium на Render

    # Adblock (опционально)
    extension_path = os.getenv("ADBLOCK_PATH", "adblock.crx")
    if os.path.exists(extension_path):
        options.add_extension(extension_path)

    # Запуск драйвера
    driver = uc.Chrome(options=options)
    driver.get(proxy_url)

    # --------------------- Открываем окна с прокси и Twitch ---------------------
    for i in range(proxy_count):
        if i > 0:
            driver.execute_script("window.open('" + proxy_url + "')")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(proxy_url)

        try:
            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)
        except:
            print(f"Could not send channel URL in proxy window {i+1}")

    print(Colorate.Vertical(Colors.red_to_blue,
        "Viewers have all been sent. The program will close."))

    driver.quit()

if __name__ == '__main__':
    main()

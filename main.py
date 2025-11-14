import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

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


def main():
    if not check_for_updates():
        return

    announcement = get_announcement()

    # Windows-specific title removed for Linux compatibility
    # os.system(f"title Kichi779 - Twitch Viewer Bot @kichi#0779 ")

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

    # Proxy servers dictionary
    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    # Fetch values from environment variables (for Render)
    proxy_choice = int(os.getenv("PROXY_CHOICE", 1))
    twitch_username = os.getenv("TWITCH_USERNAME", "Kichi779")
    proxy_count = int(os.getenv("PROXY_COUNT", 3))

    proxy_url = proxy_servers.get(proxy_choice)
    if not proxy_url:
        print(f"Invalid proxy choice {proxy_choice}, using default 1")
        proxy_url = proxy_servers[1]

    print(Colorate.Vertical(Colors.green_to_blue,
        f"Using Proxy Server {proxy_choice}: {proxy_url}"))
    print(Colorate.Vertical(Colors.cyan_to_blue,
        f"Channel: {twitch_username} | Windows of proxy to open: {proxy_count}"))

    # Chrome setup
    chrome_path = os.getenv("CHROME_PATH", "/usr/bin/google-chrome")
    driver_path = os.getenv("CHROMEDRIVER_PATH", "chromedriver")  # assume chromedriver is in PATH

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Optional: Adblock extension if exists
    extension_path = os.getenv("ADBLOCK_PATH", "adblock.crx")
    if os.path.exists(extension_path):
        chrome_options.add_extension(extension_path)

    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    driver.get(proxy_url)

    for i in range(proxy_count):
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

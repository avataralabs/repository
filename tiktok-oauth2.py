from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
import os

# === Konfigurasi ===
URL = "https://business-api.tiktok.com/portal/auth?app_id=7485627962016923664&state=your_custom_params&redirect_uri=https%3A%2F%2Fn8n.avataralabs.ai%2Fwebhook%2Foauth2-callback"
COOKIE_FILE = "tiktok_cookies.pkl"

# === Setup Chrome dengan opsi anti-deteksi ===
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === Hapus jejak navigator.webdriver ===
driver.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
        '''
    }
)

def save_cookies(driver, filepath):
    with open(filepath, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, filepath):
    with open(filepath, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

# Mulai dari domain TikTok agar bisa set cookies
driver.get("https://business-api.tiktok.com")
time.sleep(3)

# === Autologin pakai cookie (jika ada), atau manual dulu ===
if os.path.exists(COOKIE_FILE):
    load_cookies(driver, COOKIE_FILE)
    driver.get(URL)
else:
    driver.get(URL)
    print("🔐 Silakan login manual di browser jika diminta...")
    input("✅ Tekan Enter setelah login selesai dan halaman Confirm muncul...")
    save_cookies(driver, COOKIE_FILE)

# === Klik tombol Confirm ===
try:
    time.sleep(3)
    confirm_button = driver.find_element(By.XPATH, "//button[contains(text(),'Confirm')]")
    confirm_button.click()
except Exception as e:
    print("❌ Gagal klik tombol Confirm:", e)

time.sleep(5)
driver.quit()

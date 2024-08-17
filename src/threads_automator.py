import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils import retry
from cookie_manager import CookieManager
from image_processor import ImageProcessor
import random
import time


class ThreadsAutomator:
    def __init__(self, config, account, post_manager):
        """
        ThreadsAutomatorクラスのコンストラクタ
        :param config: 設定情報
        :param account: アカウント情報
        :param post_manager: PostManagerインスタンス
        """
        self.config = config
        self.account = account
        self.driver = None
        self.cookie_manager = CookieManager()
        self.image_processor = ImageProcessor(config)
        self.post_manager = post_manager


    def setup_driver(self):
        """Seleniumドライバーのセットアップ"""
        chrome_options = Options()
        if self.config.getboolean('Settings', 'headless'):
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(30)
        logging.info("Chromeドライバーのセットアップが完了しました。")

    @retry(max_attempts=3)
    def click_login_link(self):
        """ログインリンクをクリック"""
        login_link_xpath = "//div[contains(@class, 'x6s0dn4') and contains(@class, 'x78zum5')]//a[@role='link']//div[contains(text(), 'ログイン')]"
        login_link = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, login_link_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", login_link)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", login_link)
        logging.info("ログインリンクのクリックに成功しました。")

    @retry(max_attempts=3)
    def login(self):
        """ログイン処理"""
        username = self.account['username']
        password = self.account['password']
        
        # クッキーを使用してログインを試みる
        self.driver.get("https://www.threads.net/?hl=ja")
        if self.cookie_manager.load_cookies(self.driver, username):
            self.driver.refresh()
            if self.is_logged_in():
                logging.info(f"クッキーを使用して {username} でログインしました。")
                return
        
        # クッキーでのログインに失敗した場合、通常のログインを実行
        logging.info(f"{username} の通常ログインを開始します。")
        self.click_login_link()
        
        username_xpath = "//input[@name='username' or @name='email' or contains(@placeholder, 'ユーザーネーム') or contains(@placeholder, 'メールアドレス')]"
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, username_xpath))
        )
        username_input.clear()
        username_input.send_keys(username)
        username_input.send_keys(Keys.TAB)
        logging.info(f"ユーザー名/メールアドレス {username} を入力しました。")

        time.sleep(10)

        password_xpath = "//input[@name='password' or contains(@placeholder, 'パスワード')]"
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, password_xpath))
        )
        password_input.clear()
        password_input.send_keys(password)
        logging.info("パスワードを入力しました。")

        time.sleep(20)

        login_button_xpath = "//div[@role='button']//div[contains(@class, 'x6s0dn4') and contains(@class, 'x78zum5')]//div[contains(text(), 'ログイン')]"
        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, login_button_xpath))
        )
        self.driver.execute_script("arguments[0].click();", login_button)
        
        if self.is_logged_in():
            logging.info(f"アカウント {username} でログインに成功しました。")
            self.cookie_manager.save_cookies(self.driver, username)
        else:
            raise Exception(f"アカウント {username} でのログインに失敗しました。")
    
    def is_logged_in(self):
        """ログイン状態を確認する"""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Post') or contains(text(), '投稿')]"))
            )
            return True
        except:
            return False

    def random_wait(min_seconds=10, max_seconds=30):
        """
        指定された範囲内でランダムな秒数待機する
        
        :param min_seconds: 最小待機秒数
        :param max_seconds: 最大待機秒数
        """
        wait_time = random.uniform(min_seconds, max_seconds)
        logging.info(f"{wait_time:.2f}秒待機します。")
        time.sleep(wait_time)
    
    @retry(max_attempts=3)
    def post_thread(self):
        """スレッドの投稿"""
        caption, image_paths, post_set = self.post_manager.get_random_post()

        # 画像を処理
        processed_image_paths = self.image_processor.process_images(image_paths, self.account['username'])
        
        post_button_xpath = "//div[contains(@class, 'x1i10hfl') and contains(@class, 'x1ypdohk') and contains(@class, 'xdl72j9')]//div[contains(text(), 'Post') or contains(text(), '投稿')]"
        post_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, post_button_xpath))
        )
        self.driver.execute_script("arguments[0].click();", post_button)
        logging.info("投稿ボタンをクリックしました。")

        self.random_wait()

        file_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys('\n'.join(processed_image_paths))
        logging.info(f"投稿セット '{post_set}' の画像をアップロードしました。")

        self.random_wait()

        caption_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )
        caption_input.send_keys(caption)
        logging.info(f"投稿セット '{post_set}' のキャプションを入力しました。")

        self.random_wait()

        final_post_button_xpath = "//div[@role='button']//div[contains(text(), 'Post') or contains(text(), '投稿')]"
        all_post_buttons = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, final_post_button_xpath))
        )
        
        if len(all_post_buttons) < 2:
            raise Exception("必要な数のPostボタンが見つかりません。")
        
        final_post_button = all_post_buttons[1]
        self.driver.execute_script("arguments[0].click();", final_post_button)
        
        time.sleep(30)

        logging.info(f"アカウント {self.account['username']} で投稿セット '{post_set}' の投稿に成功しました。")
        self.post_manager.remove_post_set(post_set)

    def run(self):
        """自動投稿プロセスの実行"""
        try:
            self.setup_driver()
            self.driver.get("https://www.threads.net/?hl=ja")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            logging.info("Threadsのページを正常に読み込みました。")

            self.click_login_link()
            time.sleep(15)
            self.login()
            time.sleep(22)
            self.post_thread()
            
            logging.info(f"アカウント {self.account['username']} での操作が完了しました。")
        except Exception as e:
            logging.error(f"アカウント {self.account['username']} でエラーが発生しました: {str(e)}")
            raise

    def cleanup(self):
        """リソースのクリーンアップ"""
        if self.driver:
            self.driver.save_screenshot(f"logs/final_state_screenshot_{self.account['username']}.png")
            logging.info(f"スクリーンショットを保存しました: logs/final_state_screenshot_{self.account['username']}.png")
            self.driver.quit()
            logging.info("ブラウザを終了しました。")
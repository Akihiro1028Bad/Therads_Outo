import os
import json
import logging
from selenium import webdriver

class CookieManager:
    def __init__(self, cookies_dir='cookies'):
        """
        CookieManagerクラスのコンストラクタ
        
        :param cookies_dir: クッキーを保存するディレクトリ
        """
        self.cookies_dir = cookies_dir
        if not os.path.exists(cookies_dir):
            os.makedirs(cookies_dir)
        logging.info(f"クッキー保存ディレクトリを設定: {cookies_dir}")

    def save_cookies(self, driver, username):
        """
        ブラウザのクッキーを保存する
        
        :param driver: Seleniumのwebdriverインスタンス
        :param username: クッキーを保存するアカウントのユーザー名
        """
        cookies = driver.get_cookies()
        cookie_file = os.path.join(self.cookies_dir, f"{username}.json")
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f)
        logging.info(f"{username} のクッキーを保存しました: {cookie_file}")

    def load_cookies(self, driver, username):
        """
        保存されたクッキーをブラウザにロードする
        
        :param driver: Seleniumのwebdriverインスタンス
        :param username: クッキーをロードするアカウントのユーザー名
        :return: クッキーのロードに成功したかどうか
        """
        cookie_file = os.path.join(self.cookies_dir, f"{username}.json")
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
            logging.info(f"{username} のクッキーをロードしました")
            return True
        else:
            logging.info(f"{username} のクッキーが見つかりません")
            return False

    def delete_cookies(self, username):
        """
        保存されたクッキーを削除する
        
        :param username: クッキーを削除するアカウントのユーザー名
        """
        cookie_file = os.path.join(self.cookies_dir, f"{username}.json")
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
            logging.info(f"{username} のクッキーを削除しました")
        else:
            logging.info(f"{username} のクッキーが見つかりません")
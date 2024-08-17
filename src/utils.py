import json
import logging
import time
import configparser
from functools import wraps

def load_config():
    """設定ファイルを読み込む"""
    config = configparser.ConfigParser()
    with open('config/config.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config

def load_accounts():
    """アカウント情報を読み込む"""
    with open('config/accounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['accounts']

def setup_logging():
    """ログの設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler("logs/automation.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def retry(max_attempts, delay=5):
    """
    リトライデコレータ
    :param max_attempts: 最大試行回数
    :param delay: リトライ間の待機時間（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(f"試行 {attempts} 回目が失敗しました: {str(e)}。{delay}秒後に再試行します...")
                    time.sleep(delay)
            raise Exception(f"関数 {func.__name__} が {max_attempts} 回の試行後も失敗しました")
        return wrapper
    return decorator

def wait_and_log(seconds, message):
    """
    指定された秒数待機し、ログを出力する関数
    :param seconds: 待機する秒数
    :param message: ログメッセージ
    """
    logging.info(f"{message} {seconds}秒待機します...")
    time.sleep(seconds)
    logging.info(f"{seconds}秒の待機が完了しました。")
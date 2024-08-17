# main.py

import logging
from utils import load_config, load_accounts, setup_logging
from threads_automator import ThreadsAutomator
from post_manager import PostManager
from scheduler import Scheduler
import random
import time

def run_automation(config, accounts, post_manager):
    """
    自動投稿処理を実行する
    
    :param config: 設定情報
    :param accounts: アカウント情報のリスト
    :param post_manager: PostManagerインスタンス
    """
    logging.info("自動投稿処理を開始します。")

    # 1分から60分までのランダムな待機時間を生成
    wait_time_minutes = random.randint(1, 60)
    wait_time_seconds = wait_time_minutes * 60
    
    logging.info(f"ランダムな待機時間: {wait_time_minutes}分 ({wait_time_seconds}秒)")
    logging.info(f"待機開始時刻: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 待機
    time.sleep(wait_time_seconds)

    for account in accounts:
        automator = ThreadsAutomator(config, account, post_manager)
        try:
            automator.run()
        except Exception as e:
            logging.error(f"アカウント {account['username']} の処理中にエラーが発生しました: {str(e)}")
        finally:
            automator.cleanup()
    logging.info("すべてのアカウントの処理が完了しました。")

def main():
    """
    メイン関数。スケジューリングと自動投稿の実行を管理します。
    """
    # ログの設定
    setup_logging()
    
    # 設定とアカウント情報の読み込み
    config = load_config()
    accounts = load_accounts()
    
    # PostManagerの初期化
    posts_directory = config.get('Paths', 'posts_directory')
    post_manager = PostManager(posts_directory)
    
    # スケジューラの初期化
    scheduler = Scheduler()
    
    logging.info("スケジューリングされた自動投稿プロセスを開始します。")
    
    while True:
        # 次の実行時間まで待機
        scheduler.wait_until_next_run()
        
        # 自動投稿処理の実行
        run_automation(config, accounts, post_manager)

if __name__ == "__main__":
    main()
# scheduler.py

import json
import logging
from datetime import datetime, timedelta
import time

class Scheduler:
    def __init__(self, schedule_file='config/schedule.json'):
        """
        スケジューラクラスの初期化
        
        :param schedule_file: スケジュール設定ファイルのパス
        """
        self.schedule_file = schedule_file
        self.schedules = self.load_schedules()
        logging.info(f"スケジューラを初期化しました。スケジュールファイル: {schedule_file}")

    def load_schedules(self):
        """
        JSONファイルからスケジュールを読み込む
        
        :return: スケジュールのリスト
        """
        try:
            with open(self.schedule_file, 'r') as f:
                data = json.load(f)
            logging.info(f"スケジュールを正常に読み込みました。{len(data['schedules'])}件のスケジュールが設定されています。")
            return data['schedules']
        except Exception as e:
            logging.error(f"スケジュールの読み込みに失敗しました: {str(e)}")
            return []

    def get_next_run_time(self):
        """
        次の実行時間を取得する
        
        :return: 次の実行時間（datetime）
        """
        now = datetime.now()
        today = now.date()
        tomorrow = today + timedelta(days=1)

        # 今日の残りのスケジュールをチェック
        for schedule in self.schedules:
            schedule_time = datetime.strptime(schedule['time'], "%H:%M").time()
            schedule_datetime = datetime.combine(today, schedule_time)
            if schedule_datetime > now:
                logging.info(f"次の実行時間: {schedule_datetime}")
                return schedule_datetime

        # 翌日の最初のスケジュールを返す
        first_schedule = min(self.schedules, key=lambda x: datetime.strptime(x['time'], "%H:%M").time())
        next_run_time = datetime.combine(tomorrow, datetime.strptime(first_schedule['time'], "%H:%M").time())
        logging.info(f"次の実行時間: {next_run_time}")
        return next_run_time

    def wait_until_next_run(self):
        """
        次の実行時間まで待機する
        """
        next_run = self.get_next_run_time()
        wait_seconds = (next_run - datetime.now()).total_seconds()
        logging.info(f"次の実行時間まで {wait_seconds:.2f} 秒待機します。")
        time.sleep(wait_seconds)
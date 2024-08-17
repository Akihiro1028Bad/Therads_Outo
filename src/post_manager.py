import os
import random
import logging
from typing import List, Tuple

class PostManager:
    def __init__(self, posts_directory: str):
        """
        PostManagerクラスのコンストラクタ
        
        :param posts_directory: 投稿セットが保存されているディレクトリのパス
        """
        self.posts_directory = posts_directory
        self.post_sets = self._load_post_sets()
        logging.info(f"{len(self.post_sets)}個の投稿セットを読み込みました。")

    def _load_post_sets(self) -> List[str]:
        """
        投稿セットのディレクトリ一覧を読み込む
        
        :return: 投稿セットディレクトリのリスト
        """
        return [d for d in os.listdir(self.posts_directory) 
                if os.path.isdir(os.path.join(self.posts_directory, d))]

    def get_random_post(self) -> Tuple[str, List[str], str]:
        """
        ランダムな投稿セットを選択する
        
        :return: (キャプション, [画像パスのリスト], 投稿セット名)のタプル
        """
        if not self.post_sets:
            raise ValueError("投稿セットが見つかりません。")

        post_set = random.choice(self.post_sets)
        post_dir = os.path.join(self.posts_directory, post_set)
        
        caption_file = next(f for f in os.listdir(post_dir) if f.endswith('.txt'))
        with open(os.path.join(post_dir, caption_file), 'r', encoding='utf-8') as f:
            caption = f.read().strip()

        image_files = [f for f in os.listdir(post_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if len(image_files) != 2:
            raise ValueError(f"投稿セット {post_set} には2つの画像が必要です。")

        image_paths = [os.path.join(post_dir, img) for img in image_files]

        logging.info(f"投稿セット '{post_set}' をランダムに選択しました。")
        return caption, image_paths, post_set

    def remove_post_set(self, post_set: str):
        """
        使用済みの投稿セットをリストから削除する
        
        :param post_set: 削除する投稿セット名
        """
        if post_set in self.post_sets:
            self.post_sets.remove(post_set)
            logging.info(f"投稿セット '{post_set}' を使用済みリストから削除しました。")
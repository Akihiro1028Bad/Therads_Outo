# image_processor.py

import os
import logging
from PIL import Image, ImageDraw, ImageFont, ImageColor

class ImageProcessor:
    def __init__(self, config):
        """
        ImageProcessorクラスのコンストラクタ
        :param config: 設定情報を含むConfigParserオブジェクト
        """
        self.config = config
        self.watermark_enabled = self.config.getboolean('Watermark', 'enabled', fallback=False)
        self.font_size = self.config.getint('Watermark', 'font_size', fallback=30)
        self.font_color = self.config.get('Watermark', 'font_color', fallback='white')
        self.opacity = self.config.getint('Watermark', 'opacity', fallback=128)
        self.position_x = self.config.getfloat('Watermark', 'position_x', fallback=0.5)
        self.position_y = self.config.getfloat('Watermark', 'position_y', fallback=0.5)
        
        logging.info("ImageProcessorが初期化されました。透かし機能: %s", "有効" if self.watermark_enabled else "無効")

    def add_watermark(self, image_path, username):
        """
        画像に透かしを追加する
        :param image_path: 処理する画像のパス
        :param username: 透かしとして追加するユーザーネーム
        :return: 処理された画像のパス
        """
        if not self.watermark_enabled:
            logging.info("透かし機能が無効です。画像 %s は処理されません。", image_path)
            return image_path

        try:
            with Image.open(image_path) as img:
                # 透かし用のレイヤーを作成
                watermark = Image.new('RGBA', img.size, (0,0,0,0))
                draw = ImageDraw.Draw(watermark)

                # フォントの設定（システムデフォルトフォントを使用）
                font = ImageFont.load_default()
                font = font.font_variant(size=self.font_size)

                # テキストサイズの取得（更新された方法）
                bbox = draw.textbbox((0, 0), username, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # 透かしの位置を計算
                x = int((img.width - text_width) * self.position_x)
                y = int((img.height - text_height) * self.position_y)

                # 透かしを描画
                draw.text((x, y), username, font=font, fill=(*ImageColor.getrgb(self.font_color), self.opacity))

                # 元の画像と透かしを合成
                combined = Image.alpha_composite(img.convert('RGBA'), watermark)

                # 処理後の画像を保存
                output_path = os.path.join(os.path.dirname(image_path), f"watermarked_{os.path.basename(image_path)}")
                combined.convert('RGB').save(output_path)

                logging.info("画像 %s に透かし(@%s)を追加しました。出力: %s", image_path, username, output_path)
                return output_path

        except Exception as e:
            logging.error("画像 %s への透かし追加中にエラーが発生しました: %s", image_path, str(e))
            return image_path

    def process_images(self, image_paths, username):
        """
        複数の画像を処理する
        :param image_paths: 処理する画像パスのリスト
        :param username: 透かしとして追加するユーザーネーム
        :return: 処理された画像パスのリスト
        """
        processed_paths = []
        for path in image_paths:
            processed_path = self.add_watermark(path, f"@{username}")
            processed_paths.append(processed_path)
        
        logging.info("%d 枚の画像を処理しました", len(processed_paths))
        return processed_paths
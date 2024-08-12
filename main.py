import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def wait_and_log(seconds, message):
    """指定された秒数待機し、ログを出力する関数"""
    logging.info(f"{message} {seconds}秒待機します...")
    time.sleep(seconds)
    logging.info(f"{seconds}秒の待機が完了しました。")

def click_login_link(driver):
    # ログインリンクのXPathを詳細に指定
    login_link_xpath = "//div[contains(@class, 'x6s0dn4') and contains(@class, 'x78zum5')]//a[@role='link']//div[contains(text(), 'ログイン')]"
    
    try:
        # ログインリンクが表示されるまで待機
        logging.info("ログインリンクを探しています...")
        login_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, login_link_xpath))
        )
        
        # リンクが画面内に表示されるまでスクロール
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", login_link)
        wait_and_log(10, "ログインリンクが表示されるまで")
        
        # リンクが確実にクリック可能になるまで待機
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_link_xpath))
        )
        
        # JavaScriptを使用してクリックを実行
        logging.info("ログインリンクをクリックします...")
        driver.execute_script("arguments[0].click();", login_link)
        
        # クリックが成功したかを確認（例：ログインフォームの要素が表示されるまで待機）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username' or @name='email' or contains(@placeholder, 'ユーザーネーム') or contains(@placeholder, 'メールアドレス')]"))
        )
        logging.info("ログインリンクのクリックに成功しました。")
        wait_and_log(10, "ログインフォームが表示されるまで")
        
    except TimeoutException:
        logging.error("ログインリンクが見つからないか、クリックできませんでした。")
        raise
    except ElementClickInterceptedException:
        logging.error("ログインリンクがクリックできない状態です。他の要素に遮られている可能性があります。")
        raise
    except Exception as e:
        logging.error(f"ログインリンクのクリック中に予期せぬエラーが発生しました: {str(e)}")
        raise

def login(driver, username, password):
    try:
        # ユーザー名/メールアドレス入力
        username_xpath = "//input[@name='username' or @name='email' or contains(@placeholder, 'ユーザーネーム') or contains(@placeholder, 'メールアドレス')]"
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, username_xpath))
        )
        username_input.clear()  # 既存の入力をクリア
        username_input.send_keys(username)
        username_input.send_keys(Keys.TAB)  # TABキーを送信して次のフィールドに移動
        logging.info("ユーザー名/メールアドレスを入力しました。")
        wait_and_log(10, "ユーザー名/メールアドレス入力後")

        # パスワード入力
        password_xpath = "//input[@name='password' or contains(@placeholder, 'パスワード')]"
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, password_xpath))
        )
        password_input.clear()  # 既存の入力をクリア
        password_input.send_keys(password)
        logging.info("パスワードを入力しました。")
        wait_and_log(10, "パスワード入力後")

        # ログインボタンクリック
        login_button_xpath = "//div[@role='button']//div[contains(@class, 'x6s0dn4') and contains(@class, 'x78zum5')]//div[contains(text(), 'ログイン')]"
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, login_button_xpath))
        )
        
        # ボタンが表示されるまでスクロール
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", login_button)
        wait_and_log(10, "ログインボタンが表示されるまで")
        
        # JavaScriptを使用してクリックを実行
        logging.info("ログインボタンをクリックします...")
        driver.execute_script("arguments[0].click();", login_button)
        
        # ログイン成功の確認（例：ホームページの特定の要素が表示されるまで待機）
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Post') or contains(text(), '投稿')]"))
        )
        logging.info("ログインに成功しました。")
        wait_and_log(10, "ログイン成功後")

    except TimeoutException:
        logging.error("ログインボタンが見つからないか、クリックできませんでした。")
        raise
    except ElementClickInterceptedException:
        logging.error("ログインボタンがクリックできない状態です。他の要素に遮られている可能性があります。")
        raise
    except Exception as e:
        logging.error(f"ログイン中にエラーが発生しました: {str(e)}")
        raise

def post_thread(driver, caption, image_paths):
    try:
        # 投稿ボタンをクリック（最初の投稿ボタン）
        logging.info("最初の投稿ボタンを探しています...")
        post_button_xpath = "//div[contains(@class, 'x1i10hfl') and contains(@class, 'x1ypdohk') and contains(@class, 'xdl72j9')]//div[contains(text(), 'Post') or contains(text(), '投稿')]"
        post_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, post_button_xpath))
        )
        driver.execute_script("arguments[0].click();", post_button)
        logging.info("最初の投稿ボタンをクリックしました。")
        wait_and_log(5, "最初の投稿ボタンクリック後")

        # 画像のアップロード
        logging.info("画像アップロードフィールドを探しています...")
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys('\n'.join(image_paths))
        logging.info("画像をアップロードしました。")
        wait_and_log(5, "画像アップロード後")

        # キャプションの入力
        logging.info("キャプション入力フィールドを探しています...")
        caption_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )
        caption_input.send_keys(caption)
        logging.info("キャプションを入力しました。")
        wait_and_log(5, "キャプション入力後")

        # # 最終Postボタンの特定と操作
        logging.info("最終Postボタンを探しています...")
        final_post_button_xpath = "//div[@role='button']//div[contains(text(), 'Post') or contains(text(), '投稿')]"
        
        # すべてのPostボタンを取得
        all_post_buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, final_post_button_xpath))
        )
        
        # 2つ以上のボタンがあることを確認
        if len(all_post_buttons) < 2:
            logging.error("2つ目のPostボタンが見つかりません。")
            raise Exception("Required number of Post buttons not found")
        
        # 2つ目のPostボタンを選択
        final_post_button = all_post_buttons[1]
        
        # Postボタンが表示されるまでスクロール
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", final_post_button)
        wait_and_log(3, "最終Postボタンが表示されるまで")
        
        # JavaScriptを使用してPostボタンをクリック
        logging.info("最終Postボタンをクリックします...")
        driver.execute_script("arguments[0].click();", final_post_button)
        wait_and_log(5, "最終Postボタンクリック後")

        # 投稿成功の確認
        logging.info("投稿成功メッセージを待機しています...")
        success_message_xpath = "//div[contains(text(), 'Your thread was posted') or contains(text(), 'スレッドが投稿されました')]"
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, success_message_xpath))
        )
        logging.info("投稿に成功しました。")
        wait_and_log(5, "投稿成功確認後")

    except TimeoutException as e:
        logging.error(f"タイムアウトエラーが発生しました: {str(e)}")
        raise
    except ElementClickInterceptedException as e:
        logging.error(f"要素がクリックできない状態です: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"投稿中に予期せぬエラーが発生しました: {str(e)}")
        raise

def automate_threads_post():
    # Chromeオプションを設定
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Chromeウェブドライバーを初期化
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)  # ページロードのタイムアウトを30秒に設定
    
    try:
        # Threadsのウェブサイトに移動
        logging.info("ウェブサイトに接続中...")
        driver.get("https://www.threads.net/?hl=ja")
        
        # ページが完全に読み込まれるまで待機
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info("ページの読み込みが完了しました。")
        wait_and_log(10, "ページ読み込み完了後")

        # ログインリンクをクリック
        click_login_link(driver)
        
        # ログイン実行
        login(driver, "ttmakhr1028@gmail.com", "1028Akihiro")
        
        # スレッド投稿
        image_paths = [
            r"C:\Users\ttmak\MyApps\Therads_Outo\deity_image.jpeg",
            r"C:\Users\ttmak\MyApps\Therads_Outo\resized_EADB92B5-19F5-4649-B13A-8D059148509C.jpg"
        ]
        post_thread(driver, "これは自動投稿のテストです。", image_paths)
        
        logging.info("全ての操作が完了しました。")
        
    except Exception as e:
        logging.error(f"エラーが発生しました: {str(e)}")
    finally:
        # エラー発生時にスクリーンショットを保存
        driver.save_screenshot("final_state_screenshot.png")
        logging.info("スクリーンショットを保存しました: final_state_screenshot.png")
        # ブラウザを閉じる
        driver.quit()
        logging.info("ブラウザを終了しました。")

# 自動化関数を実行
if __name__ == "__main__":
    automate_threads_post()
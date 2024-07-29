import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the browser
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
url = 'https://twitter.com/login'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Replace with your credentials
username = 'speechpnumoallergoasr@gmail.com'
username_verif = "@SpeechAsr"
password = 'rh79ziqa'

def login_to_twitter(username, password, username_verif):
    user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'text')) )
    user_input.send_keys(username)
    user_input.send_keys(Keys.RETURN)

    suivant_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Suivant')]")))
    suivant_button.click()

    user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'text')) )
    user_input.send_keys(username_verif)
    user_input.send_keys(Keys.RETURN)
  
    password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password')) )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for the login process to complete
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'nav')))
    
    home_element = driver.find_element(By.CLASS_NAME, "css-175oi2r.r-6koalj.r-eqz5dr.r-16y2uox.r-1habvwh.r-cnw61z.r-13qz1uu.r-1ny4l3l.r-1loqt21")
    home_element.click()
    time.sleep(10)
    print("successful login")


def scrape_tweets():
    login_to_twitter(username, password, username_verif)
    driver.get("https://x.com/netflix")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
        )
    except Exception as e:
        print(f'Error loading tweets for account: {e}')
        return []
    
    tweets_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        tweets = driver.find_elements(By.CSS_SELECTOR, 'article')
        print(len(tweets)) 
        for tweet in tweets:
            try:
                try:
                    date = tweet.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
                    print(date)
                except:
                    date = " "
                try:
                    content = tweet.find_element(By.CSS_SELECTOR, '[lang]').text
                    print(content)
                except:
                    content = " "
                try:
                    views = tweet.find_element(By.XPATH, ".//a[contains(@aria-label, 'views')]//span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
                    print(views)
                except:
                    views =  ""
                try:
                    likes = tweet.find_element(By.XPATH, ".//button[@data-testid='like']//span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
                    print(likes)
                except:
                    likes =  " "
                try:
                    comments = tweet.find_element(By.XPATH, ".//button[@data-testid='reply']//span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
                    print(comments)
                except:
                    comments =  " "
                try:
                    retweets = tweet.find_element(By.XPATH, ".//button[@data-testid='retweet']//span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
                    print(retweets)
                except:
                    retweets = " "
                try:
                    tweet_url = tweet.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    print(tweet_url)
                except:
                    tweet_url =  " "
                media_urls = []
                media_elements = tweet.find_elements(By.CSS_SELECTOR, 'img[src*="https://pbs.twimg.com/media/"], video[src]')
                for media in media_elements:
                    media_urls.append(media.get_attribute('src'))
                    print("vidio link", media_urls)
                
                tweets_data.append([date, likes, content, views, comments, retweets, tweet_url, media_urls])     
            except Exception as e:
                print(f'Error processing tweet: {e}')
            print("*******************************************************************************************************************")
        # Scroll down and wait for new tweets to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    return tweets_data


tweets_data = scrape_tweets()
print(len(tweets_data))
# Close the browser
driver.quit()

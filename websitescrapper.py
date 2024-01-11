import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from supabase import create_client, Client
clietn_id = ""
client_secret = ""
supabase: Client = create_client("",
                                 "")

# Set up the Chrome webdriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed

# Open the homepage of the website
homepage=  "https://podcast.curioushumans.com/episodes?page=1&per=30"
driver.get(homepage)

data = {}
#update on supabase
def updateData(title, transcript):
    data, count = supabase.table('podcasts') \
        .update({'transscript': transcript}) \
        .eq('episode_name', title) \
        .execute()


# Locate and collect all the links on the homepage
titles = [title.text for title in driver.find_elements(By.CLASS_NAME, "site-episode-title")]

def extract_all_text(element):
    if element.tag_name in ["p", "span", "h1", "h2", "h3", "h4", "h5", "h6", "a", "li"]:  # Expand as needed
        return element.text
    else:
        text = ""
        for child in element.find_elements(By.XPATH, "./*"):  # Find immediate children
            text += extract_all_text(child)
        return text

# Iterate through each link
for index, title in enumerate(titles):
    try:
        print(title)
        time.sleep(2)
        link = driver.find_element(By.LINK_TEXT, title)
        link.click()
        # Wait for the metadata element to be present
        try :
            meta_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".site-episode-nav a" )))
            # Now you are on the new page, scrape the data you need
            links = [link for link in meta_element]
            links[1].click()
            time.sleep(2)
            transcript = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/main/section/section/div/div/div[1]/div[1]/p" )))
            transcript_text = [text.text for text in transcript ]
            updateData(title , transcript_text)
        except Exception as e:
            print(f"{e} print no transcript")



        # Go back to the homepage for the next iteration
        driver.get(homepage)
        time.sleep(3)

        # Wait for the homepage to load again
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "site-episode-title")))

    except Exception as e:
        print(f"Error processing link {index + 1}: {title}\n{e}")
        driver.get(homepage)
        time.sleep(3)
# Close the webdriver
driver.quit()

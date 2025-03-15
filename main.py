from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import json
import urllib.parse

from datetime import datetime
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import undetected_chromedriver as uc
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
genai.configure(api_key="AIzaSyDV6eHYnad6ymTNNNU9bZazxGECTPvAaJk")

# Create the model

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    enum = [],
    required = ["name"],
    properties = {
      "name": content.Schema(
        type = content.Type.STRING,
      ),
    },
  ),
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
    generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Generate a name of random and unique newly funded product based indian startup which may be hiring intern dev now which may be esy to get into ",
      ],
    },
  ]
)

linkedin_urls = [
    # r"https://www.linkedin.com/search/results/content/?keywords=fullstack%20developer%20intern&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=hiring%20fullstack%20intern%202025&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=fullstack%20internship%20openings&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=software%20intern%20hiring%20HR&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=fullstack%20intern%20recruiter&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=hiring%20manager%20software%20intern&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=React%20Node.js%20fullstack%20intern&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=Next.js%20internship%20hiring&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=AWS%20cloud%20internship%20hiring&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=remote%20fullstack%20internship%20hiring&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=hiring%20fullstack%20intern%20startups&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=Google%20software%20intern%20hiring&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=Amazon%20fullstack%20intern%20openings&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=Microsoft%20software%20intern%20hiring&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=hiring%20interns%20hackathon%20winners&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=Smart%20India%20Hackathon%20intern%20hiring&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=software%20intern%20referral%20hiring&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=hiring%20interns%20React%20Node.js&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=connect%20with%20recruiters%20software%20intern&origin=SWITCH_SEARCH_VERTICAL",
    r"https://www.linkedin.com/search/results/content/?keywords=internship%20hiring%20latest%20posts&origin=SWITCH_SEARCH_VERTICAL"
]

def save_emails_to_file(emails):
    """
    Saves extracted emails to a timestamped text file.

    :param emails: List of email addresses to save.
    """
    if not emails:
        print("No emails to save.")
        return

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"emails_dump_{timestamp}.txt"

    # Write emails to file
    with open(filename, "w") as file:
        for email in emails:
            file.write(email + "\n")

    print(f"Emails saved to {filename}")

# Use existing Chrome session
options = uc.ChromeOptions()
userdatadir = r"C:\Users\rajha\AppData\Local\BraveSoftware\Brave-Browser\User Data"
options.add_argument(f"--user-data-dir={userdatadir}")
# options.add_argument("--profile-directory=Default")  # Ensure correct profile
options.binary_location = brave_path  # Specify Brave binary location  # Ensure correct profile
# options.add_argument("--remote-debugging-port=9222")  # Enable debugging port
# options.add_argument("--no-sandbox")  # Prevent permission issues
# options.add_argument(
#     "--disable-dev-shm-usage"
# )  # Avoid crashes in restricted environments
# options.add_argument("--disable-extensions")  # 🚀 Disable extensions
# options.add_argument("--disable-blink-features=AutomationControlled")  # Hide Selenium
# options.add_argument("--disable-popup-blocking")  # Ensure no popups block execution
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)
driver = uc.Chrome(options=options)
failed = []

while True:
    try:
        response = chat_session.send_message("name")
        print(response.text)
        encoded_keywords = urllib.parse.quote(json.loads(response.text)["name"])
        url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_keywords}%20hiring&origin=SWITCH_SEARCH_VERTICAL"
        driver.get(url)
        time.sleep(3)
        for i in range(30):  
            driver.execute_script(f"window.scrollBy(0, {random.randint(300, 1000)});")
            time.sleep(random.uniform(0.2, 0.5))
            print(i)
        time.sleep(3)

        main_text = driver.find_element(By.TAG_NAME, "main").text
        # Find all anchor tags with mailto links
        mailto_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "mailto:")]')

        # Extract the email addresses
        emails = [link.get_attribute("href").replace("mailto:", "") for link in mailto_links]
        save_emails_to_file(emails)
        print(emails)
        # print(main_text)
        
        
        time.sleep(1)  

    except Exception as e:
        print("Error: Failed", e)
        # failed.append(link)

print(failed)
time.sleep(5)
driver.quit()

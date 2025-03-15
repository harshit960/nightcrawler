import time
from datetime import datetime
from googlesearch import search
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SE
import undetected_chromedriver as uc
from urllib.parse import urlparse, urljoin, urlunparse
import motor.motor_asyncio
import asyncio

brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://rajharshit960:9wF6duth9IdyrDzj@cluster0.8hlwe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["emails"]
collection = db["current"]
options = uc.ChromeOptions()
userdatadir = r"C:\Users\rajha\AppData\Local\BraveSoftware\Brave-Browser\User Data"
options.add_argument(f"--user-data-dir={userdatadir}")
options.binary_location = brave_path
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-popup-blocking")  # May help in some cases
options.add_argument("--disable-redirects")  # Experimental
options.add_experimental_option("prefs", {"profile.default_content_setting_values.automatic_downloads": 1})

driver = uc.Chrome(options=options)

history = []
count = 0

email_dp=[]
CDN_KEYWORDS = ["cdn", "static", "assets", "fonts", "images","blog","blogs","news"]

# List of common static file extensions
STATIC_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", 
                     ".css", ".js", ".woff", ".woff2", ".ttf", ".otf", ".ico")

def extract_emails_js(driver):
    """Extract all emails using JavaScript from the entire page content."""
    script = r"""
    let emails = new Set();
    let bodyText = document.body.innerHTML;
    let emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
    let matches = bodyText.match(emailRegex);
    if (matches) {
        matches.forEach(email => emails.add(email));
    }
    return Array.from(emails);
    """
    return driver.execute_script(script)

async def addEmail(email: str, site: str):
    if email in email_dp:
        return
    user_data = {
        "email": email,
        "site": site,
        "time": datetime.utcnow(),  # Auto-set current time in UTC
    }

    result = await collection.update_one(
        {"email": email, "site": site},  # Unique constraint
        {"$setOnInsert": user_data},  # Insert only if not existing
        upsert=True,
    )

    if result.upserted_id:
        print("New entry added! " , email)
    else:
        email_dp.append(email)
        # print("Entry already exists!")

def getWebsite(key):
    r = search(key, unique=True, region="in")
    for i in r:
        print(i)
        return i

async def scrape(url,parent_domain):
    try:

        for i in history:
            if i["url"] == url:
                if i["visited"]:
                    return
                i["visited"] = True
                break
        # print(url)
        global count
        count +=1
        try:
            driver.set_page_load_timeout(10)  
            driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*redirect*"]})
            driver.execute_cdp_cmd("Network.enable", {})
            driver.get(url)
            driver.execute_script("window.onbeforeunload = function() { return 'Redirect blocked!'; };")
        except SE.TimeoutException:
            print(f"Page load taking too long. Stopping: {url}")
            driver.execute_script("window.stop();")  # Stop further loading

        
        # time.sleep(0.3)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.01)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        for elem in driver.find_elements(By.XPATH, '//a[starts-with(@href, "mailto:")]'):
            email = elem.get_attribute("href").replace("mailto:", "").split("?")[0]
            # print(email)
            await addEmail(email, parent_domain)  
            
        
        try:
            js_emails = extract_emails_js(driver)
            for email in js_emails:
                # print(f"Found email via JavaScript: {email}")
                await addEmail(email, parent_domain)
        except Exception as e:
            print(f"Error extracting emails via JS: {e}")

        links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")]
        filtered_links = []
        for link in links:
            if link and not link.startswith(("mailto:", "tel:")):
                # Convert relative URLs to absolute
                if not urlparse(link).netloc:
                    link = urljoin(driver.current_url, link)
 
                parsed_link = urlparse(link)
                link_domain = urlparse(link).netloc
                if any(keyword in link_domain for keyword in CDN_KEYWORDS):
                    continue  # Skip this link

                # Exclude links to static files
                if parsed_link.path.endswith(STATIC_EXTENSIONS):
                    continue  # Skip this link

                # Extract link's domain
                # Check if it's the same domain or a subdomain
                if link_domain.endswith(parent_domain):
                    # Remove fragment identifiers (anything after #)
                    clean_link = urlunparse(parsed_link._replace(fragment=""))
                    filtered_links.append(clean_link)

        for link in filtered_links:
            if not any(entry["url"] == link for entry in history):
                history.append({"url": link, "visited": False})
                await scrape(link,parent_domain)
        return
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    url = getWebsite("Watchout Wearables Website")
    parent_domain = urlparse(url).netloc
    await scrape(url,parent_domain)
    print(count)

# Start an event loop properly
if __name__ == "__main__":
    asyncio.run(main())
# 🕷️ Nightcrawler

Nightcrawler is an asynchronous web crawler designed to extract email addresses from websites by recursively navigating through linked pages while staying within the same domain.

## 🛠️ Tech Stack

- **Python**: Core programming language
- **Selenium**: Web automation and interaction
- **undetected_chromedriver**: Browser automation that bypasses anti-bot measures
- **MongoDB**: Database for storing extracted emails
- **motor**: Asynchronous MongoDB driver for Python
- **asyncio**: Python's asynchronous I/O framework
- **googlesearch-python**: For initial website discovery

## ✨ Features

- **🔍 Intelligent Web Crawling**: Recursively navigates through website pages while staying within the same domain
- **📧 Email Extraction**: Captures email addresses using both direct link scanning and JavaScript content analysis
- **🧹 Smart Link Filtering**: Automatically skips CDNs, static assets, and irrelevant links
- **🔄 Duplicate Prevention**: Prevents re-crawling of visited URLs and storing duplicate emails
- **⚡ Asynchronous Operation**: Uses Python's asyncio for efficient concurrent operations
- **💾 Database Integration**: Stores extracted emails in MongoDB with website source information
- **🛡️ Anti-Detection Measures**: Uses undetected_chromedriver to avoid bot detection

## 📁 File Structure

```
nightcrawler/
│
├── app.py              # Main application file with crawler logic
├── .env                # Environment variables configuration
├── README.md           # Project documentation
└── requirements.txt    # Project dependencies
```

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nightcrawler.git
cd nightcrawler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Brave Browser if not already installed.

## ⚙️ Environment Configuration

Create a .env file in the root directory with the following variables:

```
# MongoDB connection string
MONGO_URL=mongodb://username:password@host:port/database

# Optional: Custom browser paths
# BRAVE_PATH=C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe
# USER_DATA_DIR=C:/Users/username/AppData/Local/BraveSoftware/Brave-Browser/User Data
```

Required environment variables:
- `MONGO_URL`: Your MongoDB connection string

## 🔌 Configuration

Before running the application, you need to:

1. Create and configure the .env file (see above)
2. Verify the Brave browser path is correct for your system
3. Check the user data directory path is valid for your system

You can customize these paths directly in the code or via environment variables:

```python
brave_path = os.getenv("BRAVE_PATH", "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
userdatadir = os.getenv("USER_DATA_DIR", r"C:\Users\yourusername\AppData\Local\BraveSoftware\Brave-Browser\User Data")
```

## 🚀 Usage

1. Run the application:
```bash
python app.py
```

2. The application will:
   - Search for the target website using the term "SITE NAME Website"
   - Start crawling from the first search result
   - Extract and store email addresses
   - Display a count of pages visited when complete

## 🛠️ Customization

- Modify the `getWebsite()` function to change how target websites are selected
- Adjust `CDN_KEYWORDS` and `STATIC_EXTENSIONS` lists to refine link filtering
- Update browser options and preferences in the configuration section

## 📊 Deployment

### 💻 Local Deployment

1. Ensure Python 3.7+ is installed
2. Install Brave browser
3. Set up a MongoDB database (local or cloud-based)
4. Create and configure the .env file
5. Run with `python app.py`

### ☁️ Cloud Deployment

For cloud deployment, consider:
1. Containerizing the application with Docker
2. Setting up environment variables for sensitive information
3. Using a cloud service that supports Python applications
4. Ensuring your deployment environment has access to a compatible browser

## 📜 Ethics and Legal Considerations

When using this tool, please:
- Respect website terms of service
- Follow robots.txt guidelines
- Implement reasonable rate limiting
- Consider privacy laws regarding email collection and storage


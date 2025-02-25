# **GeminiScraper 🕷️**  
**AI-Powered Multilingual Web Scraper using Selenium & Google Gemini AI**  

🚀 **GeminiScraper** is an advanced web scraping tool that combines **Selenium** with **Google Gemini AI** to extract structured multilingual content from dynamic websites. It ensures **clean, meaningful, and structured data processing**, making it ideal for research, automation, and data analysis.

---

## **✨ Features:**  
✅ **Multilingual Content Extraction** – Supports **English, Odia**, and other available languages.  
✅ **Selenium-Based Scraping** – Handles **dynamic, JavaScript-heavy websites** efficiently.  
✅ **AI-Powered Content Structuring** – Uses **Google Gemini AI** to process raw HTML into structured **JSON**.  
✅ **Smart Anti-Bot Evasion** – Implements **random delays, user-agent rotation, and human-like browsing** to avoid detection.  
✅ **Headless Mode Support** – Runs in the background for **efficient and seamless scraping**.  
✅ **Recursive Link Crawling** – Extracts and follows **internal links** for deep scraping.  
✅ **Clean JSON Output** – Structured data including **titles, main content, links, and contact information**.  

---

## **📁 Installation**  
Clone the repository and install dependencies:  

```bash
# Clone the repository
git clone https://github.com/yourusername/GeminiScraper.git  
cd GeminiScraper  

# Create a virtual environment (recommended)
python -m venv venv  

# Activate the virtual environment:
# On Windows:
venv\Scripts\activate  
# On macOS/Linux:
source venv/bin/activate  

# Install required dependencies
pip install -r requirements.txt  
```

---

## **⚡ Usage**  
### **1️⃣ Configure Base URL**  
Edit `scraper.py` to define your target website:

```python
base_url = "https://your-target-website.com"
```

### **2️⃣ Run the Scraper**  
Execute the following command to start scraping:

```bash
python scraper.py  
```

### **3️⃣ View Extracted Data**  
Scraped content is saved in `crawl_results.json` in a structured format:

```json
{
  "https://example.com/page1": {
    "url": "https://example.com/page1",
    "english": {
      "title": "Example Page",
      "content": "This is an example extracted text.",
      "links": ["https://example.com/about"],
      "contact": "info@example.com"
    },
    "odia": {
      "title": "ଉଦାହରଣ ପୃଷ୍ଠା",
      "content": "ଏହିଟି ଏକ ଉଦାହରଣ ଟେକ୍ସଟ୍。"
    }
  }
}
```

---

## **🛠 Configuration**  
### **Environment Variables**  
Create a `.env` file to store your **Google Gemini API Key**:

```env
GOOGLE_API_KEY=your_api_key_here
```

### **Logging & Debugging**  
All activity is logged in `crawler.log` for debugging purposes.

---

## **📚 File Structure**  
```
GeminiScraper/
│── venv/                   # Virtual environment (excluded from Git)
│── crawler.log             # Log file for debugging
│── requirements.txt        # Dependencies
│── scraper.py              # Main web scraper script
│── .gitignore              # Ignores unnecessary files
│── .env                    # API keys (excluded from Git)
│── README.md               # Project documentation
```

---

## **🌍 Use Cases**  
- **News Aggregation** – Extract headlines and articles from multiple sources.
- **Academic Research** – Collect multilingual data for NLP and AI projects.

---

## **🎉 Contributing**  
Pull requests are welcome! If you’d like to improve this project, please open an issue first to discuss proposed changes.

---



🎉 **Happy Scraping!** 🚀


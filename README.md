# **GeminiScraper 🕷️**  
**AI-Powered Multilingual Web Scraper using Selenium & Gemini AI**  

🚀 **GeminiScraper** is a cutting-edge web scraping tool that combines **Selenium** with **Gemini AI** to extract structured multilingual content from websites, ensuring clean and meaningful data processing.  

## **✨ Features:**  
✅ **Multilingual Support** – Extracts content in **English & Odia** (or other available languages).  
✅ **Selenium-Based Scraping** – Handles **dynamic & JavaScript-heavy** websites.  
✅ **AI-Powered Data Processing** – Uses **Gemini AI** to convert raw HTML into structured **JSON**.  
✅ **Smart Anti-Bot Evasion** – Mimics human-like browsing behavior to bypass detection.  
✅ **Headless Mode Support** – Runs in the background for **efficient crawling**.  
✅ **Automatic Link Extraction** – Recursively crawls internal links for deep scraping.  
✅ **JSON Output** – Cleanly structured data with **titles, main content, links, and forms**.  

## **📌 Installation**  
Clone the repository and install dependencies:  

```bash
git clone https://github.com/yourusername/GeminiScraper.git  
cd GeminiScraper  
pip install -r requirements.txt  
```

## **⚡ Usage**  
1️⃣ **Set your base URL** in `main()`.  
2️⃣ **Define allowed URLs** manually or via user input.  
3️⃣ Run the scraper:  

```bash
python main.py
```

4️⃣ Extracted content will be saved in **crawl_results.json**.  

## **🔧 Built With**  
- **Selenium** – Automated web browsing  
- **BeautifulSoup** – HTML parsing  
- **Gemini AI** – AI-powered text processing  
- **WebDriver Manager** – ChromeDriver automation  
- **html2text** – Converts HTML to readable text  

## **📂 Output Format (JSON)**  
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
      "content": "ଏହିଟି ଏକ ଉଦାହରଣ ଟେକ୍ସଟ୍।"
    }
  }
}


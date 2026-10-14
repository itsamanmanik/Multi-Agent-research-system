import os, urllib.parse
import feedparser
from fpdf import FPDF
import google.generativeai as genai 

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
_synt = genai.GenerativeModel(model="gemini-2.1")

def scrape_news_articles(topic:str, num_articles:int=5) -> list:
    query = urllib.parse.quote(topic)
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:num_articles]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary
        })
    return articles

def synthesize_insights(news: list, benchmarks: dict, risks: dict) -> str:
    prompt = f"""Produce a STRICT structured report based on the following information:

    EXECUTIVE_SUMMARY
    KEY_NEWS
    MARKET_BENCHMARKS
    COMPLIANCE_RISKS
    RECOMMENDATIONS
    
    NEWS = {news}

    Market Benchmarks:
    {benchmarks}

    Compliance Risks:
    {risks}

    Please provide your insights in a clear and structured manner.
    """
    response = _synt.generate_text(prompt=prompt)
    return response.

def render_pdf_report(report:str, filename:str="report.pdf") -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in report.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename
    
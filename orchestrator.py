import asyncio, json, os
import google.generativeai as genai
from fastmcp import Client
from mcp_server import mcp
from tools import scrape_news_articles, synthesize_insights, render_pdf_report

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
def get_market_benchmarks(topic:str) -> dict:
    return mcp.call_tool("get_market_benchmarks", topic=topic)
def check_compliance_risks(topic:str) -> dict:
    return mcp.call_tool("check_compliance_risks", topic=topic)

TOOL_FUNCS = {
    "scrape_news_articles": scrape_news_articles,
    "synthesize_insights": synthesize_insights,
    "get_market_benchmarks": get_market_benchmarks,
    "check_compliance_risks": check_compliance_risks,
    "render_pdf_report": render_pdf_report
}

llm = genai.GenerativeModel(model="gemini-2.1")

async def execute_tool(tool_name:str, **kwargs) -> dict:
    if tool_name not in TOOL_FUNCS:
        raise ValueError(f"Tool '{tool_name}' is not registered.")
    func = TOOL_FUNCS[tool_name]
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, func, **kwargs)
    return result

async def run(topic:str, num_articles:int=5) -> dict:
    news = await execute_tool("scrape_news_articles", topic=topic, num_articles=num_articles)
    benchmarks = await execute_tool("get_market_benchmarks", topic=topic)
    risks = await execute_tool("check_compliance_risks", topic=topic)
    insights = await execute_tool("synthesize_insights", news=news, benchmarks=benchmarks, risks=risks)
    pdf_filename = await execute_tool("render_pdf_report", report=insights)
    return {
        "news": news,
        "benchmarks": benchmarks,
        "risks": risks,
        "insights": insights,
        "pdf_report": pdf_filename
    }
    
if __name__ == "__main__":
    topic = "Artificial Intelligence in Healthcare"
    result = asyncio.run(run(topic))
    print(json.dumps(result, indent=4))    
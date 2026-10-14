from fastmcp import FastMCP

mcp = FastMCP("company-data")

@mcp.tool
def get_market_benchmarks(topic:str) -> dict:
    return {
        "topic": topic,
        "adoption_rate": 0.67,
        "sentiment" : 0.72,
        "cost_index": 0.45,
        "sample_size": 500
    }

@mcp.tool
def check_compliance_risks(topic:str) -> dict:
    return {
        "topic": topic,
        "risk_level": "medium",
        "regulatory_issues": ["GDPR", "HIPAA"],
        "flags": ["data privacy", "data retention"]
    }
    
if __name__ == "__main__":
    mcp.run()    
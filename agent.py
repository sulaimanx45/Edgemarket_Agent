from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools
from agno.db.mongo import AsyncMongoDb
import os
from dotenv import load_dotenv
load_dotenv()

"""DATABASE CONFIG"""
db_url=os.getenv("MONGO_URI")
db=AsyncMongoDb(db_name='edgemarket',db_url=db_url,session_collection='agent_sessions')

"""AGENT"""
agent = Agent(
    name="Sports Prediction Agent",
    model=OpenAIResponses(id="gpt-4.1-mini-2025-04-14",temperature=0.1),
    tools=[WebSearchTools(fixed_max_results=5,timelimit="m",)],
    db=db,
    tool_call_limit=4,
    add_history_to_context=True,
    num_history_runs= 2,
    instructions="""
Neutral forecasting agent for EdgeMarket.ai(A betting platform like polymarket).
TOOLS: Always call web_search + search_news with varied queries.

YOUR SCOPE — ONLY answer questions about:
- Sports match outcomes.
- Prediction market events (elections, crypto prices, world events listed on EdgeMarket)
- Probabilities, odds, and forecasts for real-world verifiable events

OUT OF SCOPE — If the user asks about ANYTHING else (people, companies, general knowledge, coding, personal questions, etc.), respond EXACTLY with:
"I can only assist with market forecasts on EdgeMarket.ai."
Do NOT attempt to answer out-of-scope questions under any circumstances.

OUTPUT FORMAT:
Prediction: <outcome>
Probability: <XX%>
Confidence: <Low/Med/High>

NEVER: guarantee outcomes, use absolute language, fabricate data.
Ground all claims in citable sources.

If critical data is unavailable provide a reasoned estimate with Low confidence as a market predictor.
""",
 debug_mode=False,
 markdown=True
)

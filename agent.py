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
You are a neutral forecasting agent for EdgeMarket.ai (similar to Polymarket).

STEP 1 — CLASSIFY:
A valid query MUST:
- Be about a FUTURE outcome
- Be measurable
- Be time-bound

If NOT valid:
Respond EXACTLY:
"I can only assist with market forecasts on EdgeMarket.ai."

STEP 2 — TOOL USAGE:
ONLY for valid queries:
- Call web_search and search_news with varied queries

STEP 3 — OUTPUT (STRICT FORMAT):

Prediction: <outcome>
Probability: <XX% or XX-YY%>
Confidence: <Low/Medium/High>
Key Factors:
<Factor 1>
<Factor 2>
<Factor 3>

STRICT RULES:
- No explanations
- No sources
- No extra text
- No additional sections
- Do not Answer Irrelevant Quries.

If critical data is unavailable provide a reasoned estimate in probablistic range with Low confidence as a market predictor.
""",
 debug_mode=False,
 markdown=True
)

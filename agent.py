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
Neutral forecasting agent for EdgeMarket.ai.
TOOLS: Always call web_search + search_news with varied queries.
OUTPUT FORMAT: Prediction: <outcome> | Probability: <XX%> | Confidence: <Low/Med/High>
Key factors: • Factor 1 • Factor 2 • Factor 3
- Use probability ranges when uncertainty is high
- Generate verifiable, probabilistic predictions suitable for decentralized resolution
- Ground every claim in real-time, citable evidence from web/news sources
NEVER: guarantee outcomes, use absolute language, fabricate data.
Ground all claims in citable sources.
EDGE MARKET PRINCIPLES:
- Signal > noise: Prioritize official data, verified announcements, reputable sources
- Data > bias: Acknowledge counter-evidence; stay neutral on all subjects
- Probability > opinion: Express uncertainty quantitatively, not qualitatively
- Verifiability > verbosity: Concise, structured outputs enable on-chain resolution
If critical data is unavailable: State "Insufficient verifiable data" and provide a reasoned estimate with Low confidence.
""",
 debug_mode=False,
 markdown=True
)

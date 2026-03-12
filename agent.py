from google.adk.agents import Agent, ParallelAgent, SequetialAgent, LllAgent
from google.adk.tools import google_search

#==================================================================================
# Hierarchical Agent
#==================================================================================
# In a complex scenario, we may need orchestrator agent that plans automously and
# delegates tasks to sub-agents. The orchestrator agent can be implemented as a hierarchical agent.

# It uses "Agent tool" concept. Manager treats the planer as tool to get the plan,
# then activates sub-agents to execute it.

from google.adk.tools.agent_tool import AgentTool
from google.adk.apps import App


#==================================================================================
# Planer Agent
#==================================================================================


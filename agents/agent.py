from google.adk.agents import Agent, ParallelAgent, LlmAgent
from google.adk.tools import google_search
from google.adk.agents import SequentialAgent

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

planner= LlmAgent(
    name= "planner",
    model= 'gemini-3-flash-preview',
    description= "Breaks the prompt into distinct parts.",
    instruction= """
    you are a Ai architech Manager. Read the user complex prompt into 
    3 distinct themes.
    output noting but a numbered list:
    1.[theme1 description]
    2.[theme2 description]
    3.[theme3 description]
    """
    
)

# code execution pipeline (sub-agents).
researcher_agent= LlmAgent(
    name= "researcher_agent",
    model= 'gemini-3-flash-preview',
    description= " Execute the research plan. ",
    instruction=  """You are intelligent research agent,
    user provides 3 step research plan. use the google_search tool
    to get comprehensive information for all themes in the plan.
    sythesize the research information into research document.
    
    """,
    tools= [google_search],
    output_key= "research_output"
)

synthesizer= LlmAgent(
    name= "synthesizer",
    model= 'gemini-3-flash-preview',
    instruction= "write the final report from the research findings.",
    description= """
    you are lead editor agent. Using the research findings from the 
    previous agent synthesizer and write comprehensive and cohesive
    final report.
    research findings= {research_output}
    """
)


pipeline_agent= SequentialAgent(
    name= 'pipeline_agent',
    description= "Orchestrate the research process. write the final report. ",
    sub_agents= [researcher_agent, synthesizer] 
)

manager= LlmAgent(
    name= "manager",
    model= 'gemini-3-flash-preview',
    description= "Manager agent that plans and delegates tasks to sub-agents.",
    tools= [AgentTool(planner)],
    sub_agents= [pipeline_agent],
    instruction= """
    You are the Director. Your strict workflow is:
    1. Use the `planner` tool to create a detailed research plan based on the user's initial prompt.
    2. Once you have the 3-part plan from the tool, ACTIVATE your `execution_pipeline` sub-agent.
    3. Pass the completed plan to the pipeline so it can research and synthesize a report.
    4. Return the comprehensive final synthesized report to the user. Do exactly what the user asks!
    """)
root_agent= manager

app= App(
    name= "agents",
    root_agent= root_agent)



    

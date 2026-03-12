from google.adk.agents import Agent, ParallelAgent, SequetialAgent, LlmAgent
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

planner= LlmAgent(
    name= "planner",
    model= 'gemini-3-pro',
    description= "Breaks the prompt into distinct parts."
    Instruction= """
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
    model= 'gemini-2.5_pro',
    description= " Execute the research plan. "
    Instruction=  """You are intelligent research agent,
    user provides 3 step research plan. use the google_search tool
    to get comprehensive information for all themes in the plan.
    sythesize the research information into research document.
    
    """
    output_key= "research_output"
)

synthesizer= LlmAgent(
    name= "synthesizer",
    model= 'gemini-2.5-pro',
    Instruction= "write the final report from the research findings."
    description= """
    you are lead editor agent. Using the research findings from the 
    previous agent synthesizer and write comprehensive and cohesive
    final report.
    research findings= {research_output}
    """
)


pipeline_agent= LlmAgent(
    name= 'pipeline_agent',
    model= 'gemini-3-pro',
    description= "Orchestrate the research process. write the final report. ",
    sub_agents= [researcher_agent, synthesizer] 
)

manager= LlmAgent(
    name= "manager",
    model= 'gemini-3-pro',
    description= "Manager agent that plans and delegates tasks to sub-agents.",
    tools= [AgentTool(planner)],
    sub_agents= [pipeline_agent],
    instruction= """
    you are direcor of a research project. follow strict workflow:
    1. use the planner tool to break down the user prompt into 3 distinct themes.
    2. delegate the research task to the pipeline agent, providing the themes as input.
    3. collect the final report from the pipeline agent and return it to the user.
    
    """
root_agent= manager

app= App(
    name= "research_app",
    root_agent= root_agent)



    

from dotenv import load_dotenv
load_dotenv()

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo-0125"

# Define research agent that will search the internet
researcher = Agent(
  role='Senior Researcher',
  goal='Uncover news and trends in the AI landscape. Prioritizing developments on AI applications and AI related startups.',
  verbose=True,
  memory=True,
  backstory=(
    "Driven by curiosity, you're at the forefront of"
    "innovation, eager to explore and share knowledge that could change"
    "the world."
  ),
  tools=[search_tool],
  allow_delegation=False
)

writer = Agent(
  role = "Tech content strategist",
  goal = "Craft compelling content on tech related trends",
  backstory="""You are a renowned content strategist known for your insightful and concise blogs and articles""",
  verbose=True,
  allow_delegation=True
)

editor = Agent(
  role="Tech content editor",
  goal="To make sure the language of written content matches the correct standards and tone that is needed",
  backstory="""You are a renowned tech content editor known for making great edits""",
  verbose=True,
  allow_delegation=True
)
research_task = Task(
  description="""Conduct a comprehensive analysis for the latest developments in the AI landscape, specifically focusing on new startups that have entered the space""",
  expected_output="Full analysis report in bullet points",
  agent=researcher
)

writing_task = Task(
  description="""Using the insights provided, develop an engaging blog post that highlights the most
  significant startups in the space. Your post should be informative yet accessible,
  catering to a tech-savvy audience.""",
  expected_output="Full blog post with at least 4 paragraphs",
  agent=writer
)

editing_task = Task(
  description="Using the written content provided, edit the tone and style of the article to reflect a very excited Yoda from Star Wars",
  expected_output="Full blog post that has been edited",
  agent=editor
)

crew = Crew(
  agents=[researcher, writer, editor],
  tasks=[research_task, writing_task, editing_task],
  verbose=1
)

result = crew.kickoff()
print("#############")
print(result)
# QA Research Analyst
# QA Documentation Writer
from crewai import Agent,Task,Crew,Process
from crewai import LLM
from dotenv import load_dotenv #.env file 
import os
load_dotenv()

# Step 0 - define the LLM or brain

groq_llm = LLM(
    model = f"openai/{os.getenv('GROQ_MODEL')}",
    api_key = os.getenv("GROQ_API_KEY"),
    base_url = os.getenv("GROQ_BASE_URL")
)

# Step 1 - Researchere agent
researcher_agent = Agent(
    role = "QA Research Analyst",
    goal= "Find the common buts in the web application",
    backstory="You are a QA researcher who has analysed thousands of bug reports" \
    "across web applications you specialise in identifying pattersn and trends in software defects.",
    llm = groq_llm,
    verbose = True
) 
# Step 2 - Researcher Task
researcher_task = Task(
    description="""Research and list the top 4 common bug categories in modern 
    web applications. For each category provide: name, frequency (percentage), example and impact""",
    expected_output="""A ranked list of 4 bug categories with name,
    frequency, example and impact for each.""",
    agent=researcher_agent
)

# Step 3 - Writer agent writes the documenatation

writer_agent = Agent(
    role="QA Documentation Writer",
    goal = "Create clear, actionable bug prevention guidelines",
    backstory ="""You are a technical writer specializing in QA 
    documentation. you turn complext bug data into simple,
    actionable checklists that developers can fallow""",
    llm=groq_llm,
    verbose=True
)

writing_task = Task(
    description = """Based on the research provided, create a bug prevention checklist
    that developers can use before submitteing a pull request.Make it practical and actionable items""",
    expected_output = """A formated checklist with 5-10 items that developers can quickly review before code submission""",
    agent = writer_agent
)

crew = Crew (
    agents = [researcher_agent,writer_agent],
    tasks = [researcher_task,writing_task],
    process = Process.sequential,
    verbose = True
)

# Step 4 - Run the crew
result = crew.kickoff()
print(result)



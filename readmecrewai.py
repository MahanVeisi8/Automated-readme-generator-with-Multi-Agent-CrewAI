# -*- coding: utf-8 -*-
"""ReadMeCrewAI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LQAnuuqdHNWhfrBc6KH03WDKyTlc4AeR

# **🚀 CREW AI Project: Automated README Generator using AI**

## **Introduction 📖**

This notebook demonstrates how to automate the generation of a professional and well-structured `README.md` file using **CREW AI** in combination with **Langchain** and **GROQ LLM**. The project utilizes multiple agents, each with specific tasks such as scanning directories, reading content, analyzing information, and producing the final `README.md`. By breaking down the task of creating documentation into smaller, manageable steps, this approach significantly reduces the manual effort required to maintain high-quality project documentation.

##**🛠 Installation and Setup**

To get started, we need to install the necessary libraries and set up the environment. This includes **Langchain**, **CREW AI**, and **Google Generative AI** tools.
"""

pip install --upgrade langchain langchain_core crewai langchain_groq duckduckgo-search crewai[tools]

"""## **🔑 Setting Up Environment Variables**

We need to set up our **GROQ API Key** and install any remaining required packages. Ensure you have access to the necessary APIs before proceeding.
"""

import os

# Set your API key as an environment variable
os.environ["GROQ_API_KEY"] = pass # removed the KEY after using it for privacy

"""## **🤖 Setting Up a Crew of Agents to Read and Analyze README Files**

### **📂 Cloning the GitHub Repository**

In this section, we will clone the repository containing various projects for which we need to analyze the style of `README.md` files. This will help us create a standardized template.
"""

# Commented out IPython magic to ensure Python compatibility.
# Clone the GitHub repository
!git clone https://github.com/MahanVeisi8/RL_practices.git

# Navigate to the repository directory
# %cd RL_practices

# Verify the contents of the directory
!ls -R

"""### **Step 1: Setting Up the Large Language Model (LLM)**

We will set up **GROQ LLM**, a large language model, to handle natural language processing tasks such as reading and analyzing the `README.md` file.
"""

from crewai import Agent
from crewai_tools import DirectoryReadTool, FileReadTool, FileWriterTool   # Correct import of tools
from langchain_groq import ChatGroq
import time
from crewai import Agent, Task

# Setting up the LLM (GROQ_LLM)
GROQ_LLM = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192"
)

# Test the LLM with a simple prompt using invoke
response = GROQ_LLM.invoke("What is the capital of France?")
print("LLM Response:", response)

"""### **Step 2: Initializing Tools for Directory and File Operations**

We will initialize the tools required to read directories and files from the project. These tools will be used by various agents throughout the process.

### **🕵️‍♂️ Step 3: Defining the Agents for the README Style Analysis Crew**

This section defines the **three agents** that will perform the key tasks of reading the `README.md` files, analyzing their content, and creating a standardized template based on the identified style.
"""

# Initialize the tools correctly
directory_read_tool = DirectoryReadTool()  # Initialize the DirectoryReadTool
file_read_tool = FileReadTool()            # Initialize the FileReadTool
file_write_tool = FileWriterTool()

# Define the variables for dynamic input
target_directory = "Cartpole"
target_subdirectory = "1 - DQN"

"""#### **Agent 1: Directory Analyzer**

The **Directory Analyzer** is responsible for scanning the specified directory (`Cartpole`) and identifying the `README.md` files that need to be analyzed.
"""

# Directory Analyzer Agent
directory_analyzer = Agent(
    role='Directory Analyzer',
    goal=f'Identify all README.md files in the {target_directory} directory and its subdirectories. Pass the path of a README.md file that is in a directory named something similar to {target_subdirectory}.',
    backstory="""You are a methodical analyst, excellent at traversing and cataloging directory contents.""",
    verbose=True,
    llm=GROQ_LLM,
    tools=[directory_read_tool],  # Use the initialized DirectoryReadTool
    max_iterations=100,  # Increase iterations
    time_limit=300  # Increase time limit in seconds
)

# Directory Scanning Task
directory_scan_task = Task(
    description=f"Identify and list all README.md files within the {target_directory} directory and its subdirectories. "
                f"Find a README.md file that is located in a directory named something similar to {target_subdir}. "
                "Pass the file path to the next agent.",
    agent=directory_analyzer,
    expected_output="A full path to the README.md file located in the target directory."
)

"""#### **Agent 2: Content Reader and Analyzer**

The **Content Reader and Analyzer** agent reads the identified `README.md` file and provides a detailed analysis of its style, structure, and key elements. This analysis will be passed to the next agent for template creation.
"""

# Content Reader Agent
reader_agent = Agent(
    role='Content Reader and Analyzer',
    goal=f'Read the content of the README.md file that its path is identified by the Directory Analyzer and Analyze the content of it identify its styles, structure, and key elements with details. Pass the analysis to the Template Creator.',
    backstory="""You are an avid reader with a sharp memory for details. You are an AI expert with a deep understanding of algorithms and a knack for recognizing writing styles in README files.""",
    verbose=True,
    llm=GROQ_LLM,
    tools=[file_read_tool],  # Use the initialized FileReadTool
)

# Content Reading Task
content_reading_and_analysis_task = Task(
    description="Read the content of the README.md file that its path is identified by the Directory Analyzer and Analyze the content it. Build up an understanding of the style, structure, and key elements used in the README. Provide a comprehensive summary of the style to the Template Creator agent."
                "Once the content is read, pass it to the Content Analyzer agent for further processing.",
    agent=reader_agent,
    expected_output="An explanation of how the repository creator prefers to write README files. including the style, structure, and key elements."
)

"""#### **Agent 3: Template Creator**

The **Template Creator** synthesizes the analysis provided by the Content Reader and creates a standardized, reusable `README.md` template based on the patterns identified in the original file.
"""

# Template Creator Agent
template_creator_agent = Agent(
    role='Template Creator',
    goal=f'Create a standardized README template based on the analysis provided by the Content Reader and Analyzer agent. Use the identified patterns to create a coherent and reusable template.',
    backstory="""You are a skilled technical writer, capable of synthesizing insights into a coherent and reusable template.""",
    verbose=True,
    llm=GROQ_LLM,
    tools=[file_write_tool],  # Use the initialized DirectoryReadTool
    max_iterations=100,  # Increase iterations
    time_limit=300  # Increase time limit in seconds
)

# Template Creation Task
template_creation_task = Task(
    description="Create a standardized README template based on the common patterns identified by the Content Analyzer. "
                "Ensure that the template reflects the style, structure, and key elements derived from the analysis.",
    agent=template_creator_agent,
    expected_output="A new README template file that follows the identified style and structure."
)

"""### **🚀 Running the Style Analysis Crew**

Now that we have defined the agents and their tasks, we can launch the **Style Analysis Crew** to perform the task of reading and analyzing the style of the `README.md` files.
"""

from crewai import Crew, Process

# Define the crew
crew = Crew(
    agents=[directory_analyzer, reader_agent, template_creator_agent],
    tasks=[directory_scan_task, content_reading_and_analysis_task, template_creation_task],
    process=Process.sequential,  # Ensures tasks are executed one after the other
    verbose=True
)

# Kickoff the crew - start the analysis
style_found = crew.kickoff(inputs={"Cartpole_directory": "Cartpole"})

# Print the result to confirm output
print("Style Found: ", style_found)

# Extract the final task output (from the Template Creator Agent)
style_template = style_found.tasks_output[-1].raw  # Access the last task's raw output

# Save the result to a file
output_file_path = "style_found_output.txt"
with open(output_file_path, "w") as output_file:
    output_file.write(style_template)

print(f"Style analysis and template saved to: {output_file_path}")

style_template

"""### **Summary of the Style Analysis Crew**:
- **Directory Analyzer** scans and locates the relevant `README.md` files.
- **Content Reader** reads and analyzes the style, structure, and key elements of the `README.md`.
- **Template Creator** uses the analysis to generate a reusable `README.md` template.

## **🤖 Setting Up the ML Code Analysis Crew**

In this section, we will use agents to locate a specific file (`os_labfinalpy`), read and analyze its content (focused on ML methods), and generate a detailed report. This report will include the file’s methods, problems addressed, and the results.

### **📂 Cloning the GitHub Repository for ML Code**

We will clone a different repository containing machine learning models for readahead optimization and navigate into the appropriate directory.
"""

cd ..

# Commented out IPython magic to ensure Python compatibility.
# Clone the GitHub repository
!git clone https://github.com/MahanVeisi8/Readahead-Optimization-Using-ML-Models.git

# Navigate to the repository directory
# %cd Readahead-Optimization-Using-ML-Models

# Verify the contents of the directory
!ls -R

"""### **Initializing Agents for the ML Code Analysis Crew**

In this step, we define the three agents responsible for locating, reading, and analyzing the target file (`os_labfinalpy`), followed by generating a structured report.

#### **Agent 1: File Finder**

This agent is tasked with locating the target file (`os_labfinalpy`) within the project directory or subdirectories.
"""

# Define the variables for dynamic input
target_file = "os_labfinalpy"

# File Finder Agent
file_finder_agent = Agent(
    role='File Finder',
    goal=f'Identify the {target_file} file in the current directory. Pass the file path to the next agent.',
    backstory=f"You are a methodical analyst, skilled at locating files in complex directory structures. Your task is to locate the {target_file} file.",
    verbose=True,
    llm=GROQ_LLM,
    tools=[directory_read_tool],  # Use the initialized DirectoryReadTool
    max_iterations=100,
    time_limit=300
)

# File Finding Task
file_finding_task = Task(
    description=f"Locate the {target_file} file in the current directory or its subdirectories. Pass the path of the file to the File Reader agent.",
    agent=file_finder_agent,
    expected_output=f"Path to the {target_file} file."
)

"""#### **Agent 2: File Reader and ML Analyzer**

This agent reads the content of the identified file, focusing on analyzing ML methods, the problem it addresses, and the results. The analysis is then passed to the Report Writer Agent.
"""

# File Reader Agent
file_reader_agent = Agent(
    role='ML Expert Reader and Analyzer',
    goal=f'Read the content of the {target_file} file identified by the File Finder agent, analyze the ML methods, the problem it addresses, the results obtained, and other important elements. Provide a comprehensive analysis and review for the Report Generator agent.',
    backstory=f'You are an avid reader capable of handling large files and an expert in ML and algorithms. Your task is to retrieve and read the file content, handle large files if necessary, and analyze the code in the {target_file} file, identifying its key methods, problem scope, and results. Provide an overview with details of everything.',
    verbose=True,
    llm=GROQ_LLM,  # Using the powerful flash_llm for content reading and analysis
    tools=[file_read_tool],  # Use the initialized FileReadTool
    max_iterations=1000,
    time_limit=900
)

# File Reading Task
file_reading_task = Task(
    description=f"Read the content of the {target_file} file identified by the File Finder and analyze the code. Identify key ML methods, the problem addressed, and the results. Provide a comprehensive analysis.",
    agent=file_reader_agent,
    expected_output=f"A comprehensive analysis of the ML methods, problem, and results, to be passed to the Report Writer agent."
)

"""#### **Agent 3: Report Writer**

This agent organizes the analysis provided by the File Reader Agent into a detailed, structured report, including an introduction, methods, results, and conclusion.
"""

# Report Writer Agent
report_writer_agent = Agent(
    role='Report Writer',
    goal=f'Generate a structured and detailed report based on the analysis provided by the ML Expert Reader and Analyzer agent. Organize the analysis into a clear format with sections for introduction, methodology, results, and conclusion.',
    backstory=f'You are a skilled technical writer capable of synthesizing complex technical information into a well-organized report. Use the analysis provided by the ML Expert to generate a formal report.',
    verbose=True,
    llm=GROQ_LLM,  # You can use a standard LLM here, no need for the more powerful model
    tools=[file_write_tool],  # Tool to write the report to a file
    max_iterations=100,
    time_limit=600
)

# Report Writing Task
report_writing_task = Task(
    description="Take the analysis from the ML Expert Reader and Analyzer agent and generate a detailed, structured report. Organize the content into a professional format with an introduction, methods, results, and conclusion.",
    agent=report_writer_agent,
    expected_output="A detailed written report based on the analysis of the ML practice code."
)

"""### **🚀 Running the ML Code Analysis Crew**

Now that we have defined the agents and their tasks, we can launch the **ML Code Analysis Crew** to locate, analyze, and generate a report on the target file.
"""

# Define the crew with the new Report Writer Agent
crew_ML = Crew(
    agents=[file_finder_agent, file_reader_agent, report_writer_agent],
    tasks=[file_finding_task, file_reading_task, report_writing_task],
    process=Process.sequential,  # Ensures tasks are executed one after the other
    verbose=True
)

# Kickoff the crew - start the process
ML_report = crew_ML.kickoff()

"""#### **Saving the Final Report to a File**

Once the analysis is completed and the report is generated, we will save the final report to a file named `code_content.txt`.
"""

# Extract the final report (from the Report Writer Agent)
ML_analysis = ML_report.tasks_output[-1].raw  # Access the last task's raw output

# Print the result to confirm output
print("ML Analysis Report: ", ML_analysis)

# Save the result to a file
output_file_path = "code_content.txt"
with open(output_file_path, "w") as output_file:
    output_file.write(ML_analysis)

print(f"code content and template saved to: {output_file_path}")

"""## **📝 Setting Up the Final README Generation Crew**

In this section, we will set up a crew of agents to read the two reports generated from the previous analysis (style and code), merge their content, and create a professional `README.md` file. This final README will be polished, structured, and enhanced with creative elements.
"""

cd ..

"""### **🤖 Defining the Agents for the Final README Generation**

We define three agents: one to read the reports, one to merge the content, and one to generate and refine the final README.
"""

code_report = "code_content.txt"
style_report = "style_found_output.txt"

"""#### **Agent 1: File Reader**

This agent will read the content of both the `style_report` and `code_report` files and pass the content to the next agent.
"""

# File Reader Agent: Reads content from the two text files
file_reader_agent = Agent(
    role='File Reader',
    goal=f'Read the content of both {style_report} and {code_report} and pass them to the Content Creator (content_merger_agent) Agent.',
    backstory="You are a methodical reader with a focus on retrieving and passing content for analysis.",
    verbose=True,
    llm=GROQ_LLM,  # Use the LLM for handling complex content reading tasks
    tools=[file_read_tool],  # Use the initialized FileReadTool
    max_iterations=100,
    time_limit=300
)


# File Reading Task: Read content from the two text files
file_reading_task = Task(
    description=f"Read the content of both {style_report} and {code_report}. Make sure to clearly distinguish between the two. When passing the content to the Content Creator (content_merger_agent) Agent, explain that the first section is for {style_report} (which contains the preferred style and structure) and the second section is for {code_report} (which contains the code analysis and details). Provide a detailed breakdown of both sections to help the Content Creator Agent form a clear understanding.",
    agent=file_reader_agent,
    expected_output="Content of both {style_report} and {code_report} in one message, clearly divided into two sections."
)

"""#### **Agent 2: Content Merger**

This agent merges the content from the `style_report` (style and structure) and `code_report` (code analysis) into a coherent README draft.
"""

# Content Merger Agent: Merges the content from the two files
content_merger_agent = Agent(
    role='Content Creator',
    goal=f'Write a Readme file based on the style and structure of {style_report} section and with the info of the current code report {code_report} section that all has been provided by the File Reader already. So when the File Reader agent gives you the message, do not ask for more info from it. use analyse the info given and create a good readme. Pass the created README to the README editor (readme_generator_agent) and try to interact with it whenever it wants info from you.',
    backstory="You are a skilled synthesizer, capable of combining information from multiple sources into a unified format and create a good readme based on the code report info and style wanted given.",
    verbose=True,
    llm=GROQ_LLM,
    tools=[],  # No specific tools needed, just the LLM
    max_iterations=100,
    time_limit=300
)

# Content Merging Task: Merge the content from the two files into a structured README draft
content_merging_task = Task(
    description=f"Using the content provided by the File Reader (file_reader_agent) Agent, combine the two sections into a coherent and well-organized README draft. Make sure that the style from {style_report} is applied to the project analysis from {code_report}. Structure the README in a way that fits well with the identified style, while including the detailed information from the code analysis. Once the draft is created, pass it to the README editor (readme_generator_agent) Agent for final review and improvements. Be sure to interact with the README Editor Agent if it requires further details or clarification.",
    agent=content_merger_agent,
    expected_output="A structured README text draft with the merged content, applying the preferred style to the code analysis.to be passed to the README editor agent."
)

"""#### **Agent 3: README Generator**

This agent refines the draft README, adding creative elements such as emojis and formatting enhancements, and writes the final `README.md` file.
"""

# README Generator Agent: Writes the final README file
readme_generator_agent = Agent(
    role='README editor',
    goal='Have a review based on the readme file given by the Content Creator and rewrite a final README and edit it well to produce a really cool and detiled Readme file. Add lots of fun things too, for exmaple adding emojies to create a great readme. Try to rewrite it and add emojies or anything other needed for make it perfect. Ensure it is formatted professionally and coherently and write the final README file.',
    backstory="You are an expert technical writer and reviewr for README files, proficient at organizing information into professional documentation formats. You have a great knowledge in the features of the cool README files and try to rewrite readme files to make them great.",
    verbose=True,
    llm=GROQ_LLM,
    tools=[file_write_tool],  # Use the FileWriterTool to save the README
    max_iterations=100,
    time_limit=300
)



# README Writing Task: Finalize and enhance the README file
readme_writing_task = Task(
    description="Review the draft README provided by the Content Creator (content_merger_agent) Agent. Refine the content for clarity and coherence, making sure that it adheres to professional standards. Add enhancements such as emojis, icons, and other creative elements to make the README engaging and visually appealing. Ensure the README follows best practices for formatting and layout. Once finalized, give the final README content.",
    agent=readme_generator_agent,
    expected_output="A polished and professionally formatted README content (maybe as string or txt) with added creative touches such as emojis."
)

"""### **🚀 Running the Final README Generation Crew**

Now that the agents and tasks are defined, we can launch the final crew to generate the `README.md` file.
"""

# Define the new crew
crew_readme = Crew(
    agents=[file_reader_agent, content_merger_agent, readme_generator_agent],
    tasks=[file_reading_task, content_merging_task, readme_writing_task],
    process=Process.sequential,  # Tasks are executed one after the other
    verbose=True
)

# Kickoff the crew - start the process
final_readme_creation = crew_readme.kickoff()

"""### **💾 Saving the Final README to a File**

Once the `README.md` is generated, we save the result to a file.
"""

# Extract the final README (from the README Generator Agent)
final_readme_content = final_readme_creation.tasks_output[-1].raw  # Access the last task's raw output

# Print the result to confirm output
print("Final README Content: ", final_readme_content)

# Save the result to a README file
output_readme_file_path = "FINAL_README.md"
with open(output_readme_file_path, "w") as output_file:
    output_file.write(final_readme_content)

print(f"Final README saved to: {output_readme_file_path}")

"""### **Summary of the Final README Generation Crew**

- **File Reader** reads both the style and code reports and passes the content to the Content Merger.
- **Content Merger** combines the two reports into a structured README draft.
- **README Generator** enhances the README by adding creative elements and saves the final result.

## **🔚 Conclusion**

In this project, we successfully automated the generation of a professional `README.md` file by utilizing **CREW AI**, **Langchain**, and **GROQ LLM**. We developed a multi-step process involving agents that scanned directories, read and analyzed project files, and combined this information into a well-structured and visually engaging README.

By breaking down the workflow into manageable tasks—analyzing the style, reviewing the code, and merging the content—we created a reusable solution that can be applied to a variety of repositories. This project showcases the power of AI in automating documentation tasks, making it easier to maintain high-quality project documentation with minimal manual effort.
"""
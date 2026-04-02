
# 🧑‍💼 Agentic HR Manager

## Table of Contents

**Introduction**
- [💡 Use case description](#use-case-description)

**Part I**
- [🥇 Talent acquisition agent](#-talent-acquisition-agent)
- [📝 HR case review agent](#-hr-case-review-agent)
- [🎯 HR Manager Agent](#-hr-manager-agent-orchestrator)

**Part II**
- [🤖 Automate talent acquisition agent using agentic workflows](#-automate-talent-acquisition-agent-using-agentic-workflows)
    
## 💡 Use Case Description

**Luisa** is an HR manager for a large corporation that's looking to hire many employees as part of an effort to set up a new division. Her struggle is two-fold:

1. **Recruiting candidates** for their open positions
2. **Handling reports** from existing employees for potential Business Conduct Guidelines violations.

For recruiting, Luisa must evaluate candidate résumés.  
Some of the relevant steps in this process include:

- Check if candidates **fulfill the requirements** of a given position
- Fill in a **table** with the skills/experience of each candidate
- Select **candidates** to be interviewed
- Assign **interviewers** from the team
- Coordinate **interviews** with candidates and interviewers via email
- Schedule **interviews**
- **Report back** the results to the hiring manager

Luisa would like to make her hiring process more efficient.

# Part I
## 🤖 Improve process efficiency with agents
In this portion of the lab we will create a multiagent system to help make the processes described above more efficient. We will leverage watsonx Orchestrate's low code agent builder to build our agents, empower them with tools and knowledge, and connect them such that they can work together to handle complex tasks.  

 **Please *[click here](./hands-on-lab-part-I.md)* to proceed to the instructions for Part I - Agents.**

# Part II
## 🤖 Automate talent acquisition agent using agentic workflows

Earlier in the lab you built an agent leveraging the **Chat with documents** feature of watsonx Orchestrate to upload and interact with résumés, job descriiptions, and interviewer schedules. In this case the agent's LLM does all the heavy lifting while it is Luisa's role to provide the right prompt/query.  

However, it is often not obvious what the right prompt should be creating room for ambiguity and inconsistency. Additionally, there may be deterministic steps that need to be taken every time such as automatically reaching out to the selected candidate or automatically scheduling an interview. In this case we might leverage **Agentic Workflows**.  

*Disclaimer: The workflows portion of lab requires some familiarity with basic programming concepts such as variables and loops. If you have any questions please reach out to one of your instructors for clarification or assistance.* 

 **Please *[click here](./hands-on-lab-part-II.md)* to proceed to the instructions for Part II - workflows.**

# *Optional Materials* 

## Flow Inspector
The agentic flow inspector is a powerful diagnostic tool that provides visibility into how your workflows execute in real-time helping builders understand agent behavior.

 **Please *[click here](./agentic-flow-inspector.md)* to proceed to the instructions for the Flow Inspector.**


## Agent Monitoring
Agent monitoring allows you to evaluate chat interacts, measure answer relevance, faithfulness, and tool Usage. It also enables root cause analyis.

 **Please *[click here](./agent-monitoring.md)* to proceed to the instructions for Agent Monitoring.**

## Ask-HR Lab
## 🤖 Automate HR Tasks like checking leave balance, requesting time off, and updating employee details with Agentic AI

This use case targets developing and deploying an AskHR agent leveraging IBM watsonx Orchestrate, as depicted in the provided architecture diagram. This agent will empower employees to interact with HR systems and access information efficiently through conversational AI.

 **Please *[click here](../../ask-hr/assets/hands-on-lab-askHR.md)* to proceed to the instructions for the Ask-HR Lab**



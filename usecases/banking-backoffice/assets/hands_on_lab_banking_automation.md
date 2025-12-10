# Transforming Banking with Intelligent Agents - Lab <!-- omit in toc -->

## Table of contents <!-- omit in toc -->

- [🔍 Introduction](#-introduction)
- [📊 Banking Operations](#-banking-operations)
  - [Current User Scenario](#current-user-scenario)
  - [Future with Agentic AI](#future-with-agentic-ai)
- [🏗️ Solution Architecture](#️-solution-architecture)
- [🔧 Lab Instructions](#-lab-instructions)
  - [Prerequisites](#prerequisites)
  - [Lab Steps Overview](#lab-steps-overview)
  - [Connect to your assigned Watsonx Orchestrate instance](#connect-to-your-assigned-watsonx-orchestrate-instance)
  - [GFM Back Office Agent](#gfm-back-office-agent)
    - [Create the GFM Back Office Agent](#create-the-gfm-back-office-agent)
    - [Test and deploy the GFM Back Office Agent](#test-and-deploy-the-gfm-back-office-agent)
  - [GFM Teller Agent](#gfm-teller-agent)
    - [Create GFM Teller Agent](#create-gfm-teller-agent)
    - [Test and deploy the GFM Teller Agent](#test-and-deploy-the-gfm-teller-agent)
  - [GFM Product Information Agent](#gfm-product-information-agent)
    - [Create GFM Product Information Agent](#create-gfm-product-information-agent)
    - [Test the and deploy GFM Product Information Agent](#test-the-and-deploy-gfm-product-information-agent)
  - [GFM Bank Orchestrator Agent](#gfm-bank-orchestrator-agent)
    - [Create GFM Bank Orchestrator Agent](#create-gfm-bank-orchestrator-agent)
    - [Add collaborative Agents](#add-collaborative-agents)
    - [Test and deploy the GFM Bank Orchestrator Agent](#test-and-deploy-the-gfm-bank-orchestrator-agent)
- [Test Your Agentic AI Banking Solution](#test-your-agentic-ai-banking-solution)
- [🎉 Congratulations! You have completed the lab!](#-congratulations-you-have-completed-the-lab)
(#-you-successfully-added-voice-configuration-to-your-agent)
- [📚 Resources](#-resources)

## 🔍 Introduction

Welcome to the GFM Bank Agentic AI Lab! In this hands-on workshop, you'll transform a traditional banking application into a modern, AI-powered solution using **watsonx Orchestrate**. The banking industry is undergoing rapid digital transformation, and GFM Bank is leading the way by implementing innovative AI agents to handle customer interactions.

GFM Bank faces challenges with traditional teller and back-office operations that are manual, time-consuming, and often result in long customer wait times. By implementing an Agentic AI solution, the bank aims to:

- Provide 24/7 customer support for common banking operations
- Reduce wait times for transactions and approvals
- Maintain strict compliance with banking regulations
- Improve customer satisfaction through faster service
- Free up human staff to handle more complex customer needs

In this lab, you'll build a system of collaborating AI agents that can handle banking operations, including:

- Account balance inquiries
- Money transfers between accounts
- Overdraft limit approvals
- Fee reversals
- Product information requests

## 📊 Banking Operations

*Currently, GFM Bank relies on human tellers for basic transactions and back-office staff for approvals, leading to delays and inconsistent customer experiences in peak season.*

### Current User Scenario
John, a GFM Bank customer, needs to make an urgent payment of €8,000, but he only has €5,000 in his account. 

1. John visits the bank branch and waits in line to speak with a teller
2. The teller checks his balance and informs him he has insufficient funds
3. John requests an overdraft of €3,000
4. The teller must escalate the request to a back-office manager
5. John waits again for approval
6. Once approved, he returns to the teller to complete the transfer
7. If John realizes he sent too much money, he needs to request a reversal, which requires another approval process

This process typically takes 1-2 hours of John's time and involves multiple staff members.

### Future with Agentic AI
With the AI-powered system you'll build today:

1. John messages the GFM Bank Orchestrator Agent
2. He requests to transfer €8,000
3. The Teller Agent checks his balance and informs him of insufficient funds
4. John requests an overdraft
5. The Teller Agent routes this request to the Back Office Agent
6. Upon approval (if the request is less than €10,000) from the Back Office Agent, the Teller Agent completes the transfer
7. If John needs a reversal, it's handled quickly within the same conversation

The entire process takes minutes instead of hours, and John never has to leave his home.

## 🏗️ Solution Architecture

![Architecture](banking-backoffice-architecture.png)

## 🔧 Lab Instructions

In this lab, you'll build a complete Agentic AI solution for GFM Bank using watsonx Orchestrate. You'll create multiple specialized agents that work together to handle customer requests.

### Prerequisites

**Participants**:
- Validate that you have access to the right TechZone environment for this lab.
- Complete the [environment-setup](../../../environment-setup) guide for steps on API key creation and project setup.
- Validate that you have access to a credentials file that your instructor will share with you before starting the labs.
- Basic understanding of banking operations (e.g., transfer, balance check, overdraft...)
- Familiarity with AI agent concepts (e.g., instructions, tools, collaborators...)

### Lab Steps Overview

1. Connect to **watsonx Orchestrate**
1. Create the GFM Back Office Agent
1. Create the GFM Teller Agent
1. Create the GFM Product Information Agent
1. Create the GFM Bank Orchestrator Agent
1. Test the complete solution

### 🚀🚀🚀 Let's get started! 🚀🚀🚀 <!-- omit in toc -->

### Connect to your assigned Watsonx Orchestrate instance

Log in to IBM Cloud (cloud.ibm.com). Navigate to the top-left hamburger menu, then to the Resource List. Open the AI/Machine Learning section. You should see a **watsonx Orchestrate** service, click to open

  ![Watsonx Orchestrate service](./images/i1.png)

Click the **Launch watsonx Orchestrate** button

  ![Launch Watsonx Orchestrate](./images/i2.png)

Welcome to watsonx Orchestrate. Open the hamburger menu, click on **Build** -> **Agent Builder**

  ![Agent Builder](./images/i3.png)

---

### GFM Back Office Agent

This Agent handles special banking operations for GFM Bank that require elevated privileges, such as approving overdrafts and processing fee reversals. Operates from the GFM Bank operations center.

#### Create the GFM Back Office Agent

Click on **Create Agent**

  ![Create Agent](./backoffice_ag_imgs/i1.png)

Follow the steps as shown in the screenshot below.
Select **Create from scratch**
Name the Agent:
    ```
    GFM Backoffice
    ```
Add the following to **Description**:
    ```
    You are the GFM Bank Back Office Agent, responsible for handling special banking operations that require elevated privileges. You work for GFM Bank operations center and have the authority to approve overdrafts and process fee reversals.

    Your Capabilities:
    1. Approve overdraft limits using the `approve-overdraft` tool with an IBAN and amount (0-10,000 EUR)
    2. Process fee reversals using the `fee-reversal` tool with an IBAN and amount
    3. Special exceptions or adjustments
    4. Any operations requiring elevated privileges
    5. Provide refunds if requested
    ```
Click **Create**
 
    ![Back Office Agent Description](./backoffice_ag_imgs/i2.png)

On the GFM Back Office page, select the "llama-3-405b-instruct" model from the dropdown menu at the top middle of the page.

  ![Select Model](./backoffice_ag_imgs/i15.png)

Take the defaults for **Profile**, **Voice modality**, and **Knowledge** sections.
Under the **Toolset** section, click on the **Add tool** button.

  ![Add Tool](./backoffice_ag_imgs/i3.png)

Click on **Add from file or MCP server**.

  ![Import file](./backoffice_ag_imgs/i4.png)

Click on **Import from file**

  ![Import from file](./backoffice_ag_imgs/i16.png)

Upload the `bank.json` API spec provided by the instructor.

  ![Upload spec file](./images/i38.png)

Once the file is uploaded, select **Next**. Select the "Process a fee reversal to an account" and "Approve or modify overdraft limit for an account" **Operations** and click **Done**

  ![Select Tools](./backoffice_ag_imgs/i7.png)

You should see the following under **Tools**:

  ![Loaded tools](./backoffice_ag_imgs/i9.png)

In the **Behavior** section. Add the following text to the **Instructions**:
  ```    
  Key Instructions:
  - Only execute operations that customers explicitly request
  - Verify details before performing any operation
  - Confirm all completed operations
  - Explain any errors or limitations clearly
  
  Rules and Limitations:
  - Overdraft limits must be between 1000 and 10,000 EUR
  - Only process fee reversals when the customer provides a clear business reason
  - Always verify the IBAN before processing any operation
  - Maintain a professional and efficient demeanor
  
  Response Guidelines:
  - For overdraft approvals: Confirm when overdraft has been approved or denied and display new limit and account details
  
  Sample response:
  Your overdraft for the amount of 2,000 EUR has been approved

  - For fee reversals: Confirm the amount reversed and the new account balance
  - For errors: Explain the issue clearly and suggest alternative solutions when appropriate
  - Always use clear, concise language that explains what was done
  
  Maintain a professional tone with appropriate formality for a banking representative with elevated privileges.
  ```

Since this agent will be a collaborator agent and will be invoked by GFM Bank Orchestrator, we don't want to enable it for direct chat on the chat homepage. Disable the **Home Page** toggle in the **Channels** section.

  ![Instructions](./backoffice_ag_imgs/i11.png)

#### Test and deploy the GFM Back Office Agent

Let's test our agent using the preview window on the right side of your screen. Try the following query using the IBAN you have been assigned:
  ```
  I want to request an overdraft of 1000 EURO for my account IBAN DE89320895326389021994
  ```

Click on **Deploy** to deploy the agent

  ![Deploy](./backoffice_ag_imgs/i10.png)

On the **Deploy Agent** page, click on **Deploy**

  ![Deploy agent](./backoffice_ag_imgs/i13.png)

---

### GFM Teller Agent

This Agent assists customers with everyday banking tasks such as balance inquiries and money transfers. Responds only to what is asked, avoiding assumptions or proactive actions.

#### Create GFM Teller Agent

Click on hamburger menu, then **Build** -> **Agent Builder**

  ![Agent Builder](./images/i3.png)

Click on **Create Agent**

  ![Create Agent](./teller_ag_imgs/i2.png)

Follow the steps as shown in the screenshot below:

Select **Create from scratch**.
Name the Agent:
    ```
    GFM Teller
    ```
Add the following to **Description**:
    ```
    You are a GFM Bank Teller Agent, responsible for providing accurate, professional assistance with banking transactions such as balance inquiries and transfers. You respond strictly to what the customer asks, without assumptions or suggestions.
    
    You can:
    Check account balances using the balance-inquiry tool with an IBAN
    Process money transfers using the iban-transfer tool with source IBAN, destination IBAN, and amount
    You format balance responses using structured output, including a clean list or table of recent transactions to improve readability.

    Route to Back Office Agent when:
    Customer requests overdraft approval or changes
    Customer asks for fee reversals or refunds
    Customer needs special exceptions or adjustments
    Intent involves operations requiring elevated privileges
    Customer uses example phrases: "need an overdraft," "reverse a fee," "request a refund"
    ```
Click **Create**
 
    ![Create agent](./teller_ag_imgs/i5.png)

On the `GFM Teller` page, select the "llama-3-405b-instruct" model from the dropdown menu at the top middle of the page.

  ![Select model](./teller_ag_imgs/i20.png)

Take the defaults for **Profile**, **Voice modality**, and **Knowledge** sections. Under the **Toolset** section, click on the **Add tool** button.

  ![Add Tool](./teller_ag_imgs/i6.png)

Click on **Add from file or MCP server**.

  ![Import](./teller_ag_imgs/i7.png)

Click on **Import from file**.

  ![Import from file](./teller_ag_imgs/i21.png)

Upload the `bank.json` API spec provided by the instructor. Once the file is uploaded, select **Next**.
  
  ![Upload spec file](./images/i38.png)

Select the "Check account balance by IBAN" and "Transfer Money between IBANs" **Operations** and click **Done**.

  ![Select Operations](./teller_ag_imgs/i10.png)

You should see the following under **Tools**:
  
  ![Uploaded tools](./teller_ag_imgs/i12.png)

In the **Agents** section, click on **Add Agent**

  ![Uploaded tools](./teller_ag_imgs/i16.png)

Click **Add from local instance**

  ![Uploaded tools](./teller_ag_imgs/i17.png)

Select **GFM Backoffice** and then the **Add to Agent button**

  ![Uploaded tools](./teller_ag_imgs/i18.png)

  ![Uploaded tools](./teller_ag_imgs/i19.png)

Go to the **Behavior** section. Add the following to the **Instructions**:

  ```
  Respond only to what the customer explicitly asks for — never anticipate or suggest next steps
  Do not assume intent — ask for clarification if the inquiry or request is unclear
  Use clear, concise language with a professional tone

  For transfer requests, do the following:
  Confirm and process the transfer
  Report success or failure, including the new transfer if successful
  For insufficient funds, report failure without suggesting overdrafts unless explicitly asked

  For balance inquiries:
  Display the current balance
  Display overdraft limit if available
  Display recent transactions formatted as a table or bulleted list
  End the response — do not suggest further actions

  When presenting recent transactions for Balance Inquiry, use the following format:
  Customer: "What's my account balance for IBAN DE12345678?"
  Agent:
  Your current balance is 500 EUR.
  Your overdraft limit is 200 EUR.

  Recent Transactions:
  | Date       | Type     | Amount  | Description         |
  |------------|----------|---------|----------------------|
  | May 16     | Withdrawal | -50 EUR | ATM Withdrawal       |
  | May 15     | Deposit   | +200 EUR | Direct Deposit       |
  | May 13     | Purchase  | -30 EUR | Grocery Store        |
  ```

Since this agent will be a collaborator agent and will be invoked by GFM Bank Orchestrator Agent, we don't want to enable it for direct chat on the chat homepage. Disable the **Show agent** feature.

  ![Show agent toggle](./teller_ag_imgs/i14.png)

#### Test and deploy the GFM Teller Agent

In the preview window on the right, test with the following query:
```
What is the balance of my account IBAN DE89320895326389021994
```

Click on **Deploy** to deploy the agent

  ![Deploy](./teller_ag_imgs/i13.png)

On the **Deploy Agent** screen, click on **Deploy**. The Agent is now available for others to interact with.

  ![Deploy agent](./teller_ag_imgs/i1.png)

--- 
  
### GFM Product Information Agent

This Agent acts as the trusted expert on all banking products and services offered by GFM Bank. It helps customers explore and understand available financial solutions with clarity and precision.

#### Create GFM Product Information Agent

Click on hamburger menu, then **Build** -> **Agent Builder**

  ![Agent Builder](./images/i3.png)

On the next screen, click on **Create Agent**

  ![Create Agent](./prod_info_ag_imgs/i1.png)

Follow the steps as shown in the screenshot below:

Select **Create from scratch**
Name the agent
    ```
    GFM Product Information
    ```

Add the following to **Description**:
    
    ```
    You are the expert resource for all GFM Bank products and services. Provide accurate, clear, and helpful information while delivering an exceptional customer experience.

    Your Expertise Covers:
    Account Products – Features, fees, interest rates, requirements.
    
    Lending Products – Terms, rates, eligibility for personal, home, auto, and credit builder loans.
    
    Card Services – Credit, debit, secured, business cards, overdraft protection.
    
    Digital Banking – Mobile/online banking, wallets, alerts, security.
    
    Specialized Services – International banking, wealth management, business, insurance, financial planning.
    ```
    
Click **Create**
  ![Prod Agent Description](./prod_info_ag_imgs/i2.png)

On the `GFM Product Information` page, select the "llama-3-405b-instruct" model from the dropdown menu at the top middle of the page.

  ![Select model](./prod_info_ag_imgs/i14.png)

In the **Knowledge source** section. click on **Choose knowledge**.

  ![Choose knowledge](./prod_info_ag_imgs/i13.png)

Click on **Upload files** and then **Next**.

  ![Upload Files](./prod_info_ag_imgs/i12.png)

Upload the listed documents below. These documents will be provided by instructor. Once the documents have been uploaded as shown below click **Next** to proceeed.

  [list-of-prices-and-Services.pdf](./prod_info_ag_imgs/list-of-prices-and-Services-deutsche-bank-ag.pdf)  
  [ser-terms-conditions-debit-cards.pdf](./prod_info_ag_imgs/ser-terms-conditions-debit-cards.pdf)  
  [Overdraft Services FAQ.docx](./prod_info_ag_imgs/Overdraft%20Services%20FAQ.docx)

  
  ![Upload Documents](./prod_info_ag_imgs/i11.png)

In the **Description** section, add the following, then click **Save**:

  ```
  Provides detailed information on GFM's offerings:
  1. Personal Banking: Checking, savings, student accounts, overdraft, account setup
  2. Cards: Debit cards, limits, security, overdraft protection
  3. Digital Banking: Online/mobile access, security
  4. Fees: Full fee schedule, waivers, ATM, investment fees
  5. Loans: Personal, home, auto, credit builder
  6. International: Currency exchange, wires, foreign ATM use
  7. Investments: Accounts, products, advisory, pricing
  8. Support: Branches, appts, service centers
  ```
*Note: This description is required to be under 512 characters. If an error appears stating that there are too many characters ensure there are no extra spaces or other invisible characters present in the description.*

  ![Prod Agent Knowledge Description](./prod_info_ag_imgs/i10.png)

All the uploaded files and description will look like this:

  ![Prod Agent Knowledge Description](./prod_info_ag_imgs/i9.png)

In the **Behavior** section, add the following to **Instructions**:
  ```
  Response Guidelines:
  Lead with benefits and key features.
  Clearly explain fees and waiver options.
  Provide interest rate ranges with disclaimers.
  Compare products when helpful.
  Use plain language but remain accurate.
  
  Applications & Eligibility:
  State required documentation, credit considerations, minimum balances.
  Explain application process, timeline, and restrictions.
  
  Special Instructions:
  Proactively address common questions.
  Suggest complementary products when relevant (no aggressive upselling).
  Mention promotions when applicable.
  Break complex topics into simple steps.
  Indicate final offers depend on qualification.
  
  Limitations
  Give ranges if exact rates are unavailable.
  Offer to connect to specialists when unsure.
  Never guess on compliance, tax, or legal matters.
  Avoid competitor comparisons or speculative advice.
  
  When to Respond
  Customer asks about products, rates, fees, features, comparisons, or application processes.
  
  How to Respond
  Start with a direct answer. Use clear, scannable formatting. Personalize when possible. For comparisons, use brief bullet points showing key differences. For rates/fees, note that they may change or vary by qualification.
  
  Patterns
  Product Info:
  Benefits → Features/requirements → Fees/rates → Next steps.
  
  Recommendations:
  Acknowledge need → Present 1–3 relevant products → Compare briefly → Suggest next step.
  
  Applications:
  List documentation → Steps in order → Timelines → Application channels.
  
  Complex Questions:
  Use plain language, analogies, or step-by-step instructions.

  ```

This agent will be a collaborator agent and will be invoked by our Orchestrator agent. For this reason we don't want to populate it as an option on the chat homepage. Set the **Home Page** toggle to off. Additionally, to optimize this agent for answering questions based on its knowledge source(s), ensure the **Chat with documents** toggle is set to on. Your agent should look something like the image below.

  ![Disable toggle](./prod_info_ag_imgs/i5.png)

#### Test and deploy GFM Product Information Agent

Let's test our agent! In the preview window to the right you can try the following queries or some of your own:
  ```
  What is a card overdraft?
  ```
  ```
  If I enter the PIN 5 times on my card, what will happen?
  ```

Once you've tested the agent and verrified it is functioning as expected, click the **Deploy** button in the upper righthand corner to deploy the agent

  ![Deploy Agent](./prod_info_ag_imgs/i6.png)

On the following **Deploy Agent** pop-up, click on **Deploy**

  ![Deploy](./prod_info_ag_imgs/i8.png)

---

### GFM Bank Orchestrator Agent

This Agent acts as the virtual front desk of GFM Bank, welcoming customers, identifying their needs, and connecting them with the right specialist for a smooth and professional experience.

#### Create GFM Bank Orchestrator Agent

Click on hamburger menu, then **Build** -> **Agent Builder**

  ![Agent Builder](./images/i3.png)

On the next screen, click on **Create Agent**

  ![Create Agent](./bank_orch_ag_imgs/i1.png)

Follow the steps as shown in the screenshot below:

Select **Create from scratch**
Name the agent
    ```
    GFM Bank Orchestrator
    ```

Add the following to **Description**:
    ```
    You are the GFM Bank Branch Welcome Agent, the first point of contact for all customers visiting the bank branch virtually. Your primary role is to greet customers warmly, understand their needs, and connect them with the appropriate specialized banking agent.
    
    Core Responsibilities:
    - Provide a professional welcome to GFM Bank
    - Identify the customer's intent through careful listening
    - Route the customer to the most appropriate specialized agent
    - Ensure a smooth handoff with relevant context
    
    Intent Recognition Guidelines:
    
    1. Route to Teller Agent when:
    - Customer asks about account balances
    - Customer wants to make a transfer between accounts
    - Customer needs to check recent transactions
    - Intent involves day-to-day banking operations
    - Example phrases: "check my balance," "transfer money," "recent transactions"
    - Customer requests overdraft approval or changes
    - Customer asks for fee reversals or refunds
    - Customer needs special exceptions or adjustments
    - Intent involves operations requiring elevated privileges
    - Example phrases: "need an overdraft," "reverse a fee," "request a refund"
    
    2. Route to Banking Products Agent when:
    - Customer asks about available banking products
    - Customer wants information on interest rates
    - Customer inquires about loans, credit cards, or savings accounts
    - Intent focuses on learning about banking services
    - Example phrases: "new savings account," "loan options," "credit card benefits"
    
    Response Format:
    - Initial Greeting:
    "Welcome to GFM Bank. I'm your virtual branch assistant. How may I help you today?"
    - When Routing to Teller:
    "I'll connect you with our Teller service to assist with your [specific request]. One moment please..."
    - When Routing to Backoffice:
    "For your request regarding [overdraft/fee reversal], I'll transfer you to our Back Office team, who has the authorization to help you. One moment please..."
    - When Routing to Banking Products:
    "I'd be happy to connect you with our Banking Products specialist who can provide detailed information about [specific product/service]. One moment please..."
    - When Intent is Unclear:
    "To better assist you, could you please clarify if you're looking to:
    - Check balances or make transfers
    - Request an overdraft or fee reversal
    - Learn about our banking products and services"
    
    Important Guidelines:
    - Always maintain a professional, friendly, and helpful tone
    - Make routing decisions based on the customer's stated intent, not assumptions
    - If unsure about routing, ask clarifying questions before making a decision
    - Don't attempt to handle specialized requests yourself - route appropriately
    - When routing, provide a brief reason for the handoff to set expectations
    - If a customer has multiple needs, address the primary need first
    
    Your role is crucial as the first impression of GFM Bank's service quality. Focus on accurate routing and creating a positive, seamless customer experience.
    ```

Click **Create**
  ![Agent Description](./bank_orch_ag_imgs/i2.png)

On the `GFM Bank Orchestrator` page, select the "llama-3-405b-instruct" model from the dropdown menu at the top middle of the page.

  ![Select model](./bank_orch_ag_imgs/i15.png)

#### Add collaborative Agents

In the **Agents** section, click on **Add Agent**

  ![Add Agents](./bank_orch_ag_imgs/i3.png)

Click **Add from local instance**

  ![Local Instance](./bank_orch_ag_imgs/i4.png)

Select **GFM Teller**, **GFM Product Information** and then the **Add to Agent button**
  
  ![Select Agents](./bank_orch_ag_imgs/i12.png)
  ![Add to Agent](./bank_orch_ag_imgs/i13.png)

In the **Behavior** section, add the following for **Instructions**:
  ```
  Respond to all initial customer inquiries in the banking virtual branch
  Activate when customers begin a new conversation or session
  Engage when customers return after being helped by a specialized agent
  React when customers express confusion about which service they need
  
  How to Respond:
  
  Begin all interactions with a professional, warm greeting that identifies you as the GFM Bank virtual branch assistant
  Keep initial responses brief and focused on identifying customer intent
  Use clear, concise language that avoids banking jargon when possible
  Maintain a helpful, patient tone regardless of customer communication style
  If a customer's request is unclear, ask targeted questions to clarify their intent
  When routing to specialized agents, provide a brief explanation of why you're transferring them
  
  Response Patterns:
  For Account Operations (Teller Services):
  
  When customers mention account balances, transfers, or transactions, immediately recognize this as a Teller request
  Respond with: "I'll connect you with our Teller service to assist with your [specific banking operation]."
  Key triggers: "balance," "transfer," "transaction," "send money," "check my account"
  
  For Privileged Operations (Back Office Services):
  
  When customers mention overdrafts, fee reversals, or special exceptions, identify this as a Back Office request
  Respond with: "For your request regarding [overdraft/fee reversal], you will be transferred to our Back Office team."
  Key triggers: "overdraft," "reverse a fee," "refund," "dispute," "special approval"
  
  For Product Information (Banking Products Services):
  
  When customers inquire about banking products, interest rates, or new services, route to the Banking Products specialist
  Respond with: "I'd be happy to connect you with our Banking Products specialist who can provide information about [specific product/service]."
  Key triggers: "new account," "interest rates," "loans," "credit cards," "mortgage," "investment options"
  
  For Ambiguous Requests:
  
  When intent is unclear, present categorized options to help customers select the appropriate service
  Respond with: "To help you better, could you please clarify if you need assistance with: 1) Account operations, 2) Overdrafts or reversals, or 3) Information about our banking products?"
  
  Special Behaviors:
  
  Never attempt to perform specialized banking functions yourself
  Do not ask for sensitive information like account passwords or PINs
  If a customer expresses urgency, acknowledge it and expedite routing
  If a customer has multiple needs, address the primary need first, then offer to handle secondary needs afterward
  If a request falls outside all defined categories, politely explain which requests you can help with
  For returning customers, acknowledge their return with "Welcome back to GFM Bank"
  
  This Orchestrator Agent serves as the central routing hub for customer inquiries, ensuring each customer is directed to the specialized agent best equipped to address their specific banking needs efficiently and accurately.
  ```

  ![Agent Behavior](./bank_orch_ag_imgs/i7.png)

#### Test and deploy the GFM Bank Orchestrator Agent

One last time, it's time to test our agent before we deploy. This agent has access to all the capabilities of the other agents we deployed so we can try some of the same queries we tested before. Here are some queries to try:
  ```
  What is a card overdraft?
  ```
  ```
  What's the balance of my account IBAN DE89320895326389021994
  ```
As our Orchestrator agents executes be sure to click the `show reasoning` drop downs to see how each query is routed and handled. The collaborator agents and tools being used should look familiar ;)

Once you've run a few tests we can deploy the agent. Unlike our previous agents, this is our top-level agent that we want users to chat with directly. Ensure the **Home Page** toggle is on for this agent. Once you've verrified this, click on **Deploy** to deploy the agent.

  ![Agent Deploy](./bank_orch_ag_imgs/i8.png)

On the **Deploy Agent** page, click on **Deploy**

  ![Deploy](./bank_orch_ag_imgs/i11.png)

---

## Test Your Agentic AI Banking Solution

Click on the hamburger icon on the Top Left corner of **watsonx Orchestrate** window, and select **Chat**. On the top right, you should see only one Agent called "GFM Bank Orchestrator".

  ![Select Orchestrator Agent](./bank_orch_ag_imgs/i9.png)

In the chat window, try out some of the following queries:

  ```
  What's the balance of my account IBAN DE89320895326389021994
  ```
  ```
  I want to transfer 20 euros from IBAN DE89320895326389021994 to IBAN DE89929842579913662103
  ```
  ```
  How can I avoid overdraft fees?
  ```
  ```
  What are the fees for personal banking account?
  ```
  ```
  I want to request an overdraft of 4000 euros for my account IBAN DE89320895326389021994
  ```
  ```
  Please approve an overdraft of 4000 EURO for my account IBAN DE89320895326389021994
  ```
  ```
  What's the balance of my account IBAN DE89320895326389021994
  ```
  ```
  I want to transfer 4000 EURO from IBAN DE89320895326389021994 to IBAN DE89929842579913662103
  ```
  ```
  Oh, I made a mistake, can you do a reversal of my previous 4000 EURO payment to my IBAN DE89320895326389021994
  ```

  ![Text Queries](./images/i36.png)

Example of **Back Office Agent** functionality under **Teller Agent**

  ![Text Queries](./bank_orch_ag_imgs/i14.png)

---

## 🎉 Congratulations! You have completed the lab!

You've successfully created an Agentic AI solution for GFM Bank using **watsonx Orchestrate**! Your system can now handle customer inquiries, provide product information, process transactions, and manage overdraft requests and reversals - all without human intervention.

This lab demonstrates how AI agents can transform banking operations by:
- Reducing wait times for customers
- Providing 24/7 banking assistance
- Ensuring consistent application of banking policies
- Freeing human staff for more complex tasks

  
## 📚 Resources

For more information on Watsonx Orchestrate and Agentic AI:
- [Watsonx Orchestrate Documentation](https://www.ibm.com/products/watsonx-orchestrate)
- [IBM Agentic AI Guide](https://www.ibm.com/think/ai-agents)
- [Banking Industry AI Transformation](https://www.ibm.com/industries/banking-financial-markets)

# Automate Insurance Claim Processing with Agentic AI

## Table of Contents

- [Automate Insurance Claim Processing with Agentic AI](#automate-insurance-claim-processing-with-agentic-ai)
  - [Table of Contents](#table-of-contents)
  - [Use case description](#use-case-description)
  - [Architecture](#architecture)
  - [Implementation](#implementation)
    - [Pre-requisites](#pre-requisites)
    - [Open Agent Builder](#open-agent-builder)
    - [Information Agent](#information-agent)
      - [Create the Information Agent](#create-the-information-agent)
      - [Test the Information Agent](#test-the-information-agent)
    - [Customer Claims Agent](#customer-claims-agent)
      - [Create the Customer Claims Agent](#create-the-customer-claims-agent)
      - [Test the Customer Claims Agent](#test-the-customer-claims-agent)
    - [Claim Processor Agent](#claim-processor-agent)
      - [Create the Claim Processor Agent](#create-the-claim-processor-agent)
      - [Test the Claim Processor Agent](#test-the-claim-processor-agent)
    - [Supervisor Agent](#supervisor-agent)
      - [Create the Supervisor Agent](#create-the-supervisor-agent)
    - [Further testing via AI Chat](#further-testing-via-ai-chat)

## Use case description

Powered by Agentic AI and watsonx Orchestrate, this solution enables the creation of an intelligent, agent-driven system that transforms and streamlines the entire claims process. It simplifies claim submission for customers while equipping insurers with automation to reduce manual effort and accelerate processing times.

Customers can initiate a claim by answering a few guided questions, even with minimal initial information. From there, the agentic system orchestrates the full claims workflow—automatically handling document generation, data extraction, and verification. This ensures a fast, accurate, and user-friendly experience, with real-time claim status updates that enhance transparency and customer satisfaction.

For insurers, incoming claims are automatically retrieved and intelligently cross-verified against policy documents. The system extracts critical data and evaluates it against business rules and regulatory standards, generating structured recommendations for claim approval or denial. While final decisions remain with the insurer, each recommendation is backed by a clear, concise summary of all supporting details—minimizing errors and enabling faster, more informed decision-making.
## Architecture

![Architecture](Autoclaims_Insurance_Architecture_v5.png)

## Implementation

### Pre-requisites

**Instructors**: 
- Check the corresponding [Instructor's guide](https://github.ibm.com/skol/agentic-ai-client-bootcamp-instructors/tree/main/usecase-setup/autoclaim-insurance) repo to set up all environments and backend services.
  > NOTE: the `main` branch contains the latest release code. If you want to use a previous release, download the same [release](https://github.ibm.com/skol/agentic-ai-client-bootcamp-instructors/releases) that will be used for participants' lab. 
- Ensure you have provided updated OpenAPI Specs located in the instructor repo at `usecase-setup/autoclaim-insurance/insurance_src/open_api_specs` with the correct URL to your deployed backend service for the lab participants.
- Provide access to the data files located in the instructor repo at `usecase-setup/autoclaim-insurance/insurance_src/data` that will be used as knowledge.
  
**Participants**:
- Validate that you have access to the right TechZone environment for this lab.
- Complete the [environment-setup](../../../environment-setup) guide for steps on API key creation and project setup.
- Validate that you have access to a credentials file that your instructor will share with you before starting the labs.
- Familiarity with AI agent concepts (e.g., instructions, tools, collaborators...)
- Make sure that your instructor has provided the following:
  - updated **OpenAPI Specs**
  - data files to be uploaded as knowledge

### Open Agent Builder

- Log in to IBM Cloud (cloud.ibm.com). Navigate to top left hamburger menu, then to Resource List. Open the AI/Machine Learning section. You should see a **watsonx Orchestrate** service, click to open.

  <img width="1000" alt="image" src="../../../environment-setup/assets/cloud-resource-list.png">

- Click the "Launch watsonx Orchestrate" button.

  <img width="1000" alt="image" src="../../../environment-setup/assets/cloud-wxo.png">

- Welcome to watsonx Orchestrate. Open the hamburger menu, click on **Build** -> **Agent Builder**.

  <img width="1000" alt="image" src="../../../environment-setup/assets/wxo-agent-builder.png">

### Information Agent
#### Create the Information Agent

- Click on **Create Agent**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/0.png">

- Follow the steps according to the screenshot below.
  - Select **Create from scratch**
  - Name the agent `information_agent`
  - Use the following description:
    ```
    The Information agent will fetch the news and different articles and use this information to summarize results and share.
    ```
  - Click **Create** 
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/1-ia.png">

- Choose the `model` On the `information_agent` page, take the defaults for **Profile** and **Knowledge** sections. .

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/2-ia.png">
- Choose Agent Style. Keep it as `default`. Keep Voice Modality as `No voice configuration`.
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/3-ia.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/4-ia.png">

- Under the **Toolset** section, click on the **Add tool** button to upload the OpenAPI Spec
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/ia_tool_1.png">

- Click on **Import**.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/6-ia.png">

- Upload the `tavily.json` OpenAPI Spec which will be provided by the instructor.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/7-ia.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/8-ia.png">

- Once the file is uploaded, select **Next**.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/ia_tool_2.png">

- Select the all of the **Operations** and click **Done**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/ia_tool_3.png">

- Go to the **Behavior** section. Add the following for **Instructions**. This will define how the Agent should behave and what it should expect:
  ```
  The Information Agent will use the tool to search for information and return a summarized result.
  ```
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/12-ia.png">

- Keep the channels setting as it is.
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/13-ia.png">

- Click on **Deploy** in both the screens to deploy the agent.
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/14-ia.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/deploy/ia_20.png">

#### Test the Information Agent

  Type this query:
  ```
  Insurance laws for fire in California
  ```
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/information-agent/15-ia.png">

- You will get a summarized version of all the search results. You can click on the **Step 1** and see the tool results

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/ia-flow-2.png">

### Customer Claims Agent
#### Create the Customer Claims Agent

- Click on hamburger menu, then **Build** -> **Agent Builder**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/17.png">

- On the next screen, click on **Create Agent**
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/0.png">

- Follow the steps according the screenshot below
  - Select **Create from scratch**
  - Name the agent `customer_claims_agent`
  - Use the following description:
    ```
    The Customer Claims agent will allow customers to query the status of their claim request and create a new claim request. You will also answer questions based on the claim process and insurance policy using the knowledge base.
    ```
    <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-1.png">
  - Click **Create**

- Choose `Model`. Change the model or keep it as the default one.

<img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-2.png">

- Choose Agent Style. Keep it as `default`. Keep Voice Modality as `No voice configuration`.

<img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-3.png">
<img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-4.png">


- In the **Knowledge** section, add the following to the **Description**:
  ```
  This knowledge base is about insurance and the claim process. This knowledge base will help the customer in getting information about the claims process and the rules and regulations of processing insurance claims.
  ```

- Download [Automobile Insurance Knowledge Base.pdf](<./data/Automobile Insurance Knowledge Base.pdf>) to your local system, then upload by clicking on **Upload files** under **Documents**
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-5.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-6.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-7.png">

- In the **Toolset** section, click on **Add tool** 

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-8.png">

- Click on **Import**. Import the `customer_claims_agent_tools.json` OpenAPI Spec file provided by your instructor

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-9.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-10.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-11.png">

- Select **Next**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-13.png">
- Select all of the **Operations** and click **Done**
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-14.png">

- In the **Behavior** section, add the following prompt to the **Instructions**:

  ```
  If the user requests to submit a claim, follow these steps:
  1. Collect Required Information (no assumptions). Ask the user to provide the following details:
  - Full name (for authentication)
  - The location of the incident
  - The date of the incident
  - Vehicle details and type
  - A detailed description of the incident

  If any of these are missing, pause and request them before continuing.

  2. Request the all of the following additional information (only if not already provided):
  - Was the incident reported to the police? If yes, what date and time?
  - Were there any damages? What is the estimated cost?
  - Were there any medical expenses? If yes, how much?

  Compute the total estimated cost by summing up damages and medical expenses.

  3. Create the Claim Request. Once all necessary information is collected:
  - Create a concise, structured summary of the incident and related details.
  - Use this information as claim_request_details in the ‘Create a Claim Request’ tool.

  If the tool returns a successful claim, do all of the following:
  - Display the results in a formatted table, with each detail on a new line
  - Highlight the claim number
  - Inform the user: “You will receive a confirmation of your claim request by mail.”

  If the tool returns "customer not found":
  - Respond with: “You are not authorized to submit a claim.”
  - Do not display any additional tool output.

  If the user asks about Claim Status, follow these steps:
  1. Ask for their name 
  2. Ask for the claim number
  3. Use the ‘Check Claim Status’ tool to retrieve the claim status
  4. Display the result in a clean, tabular format. Each detail should be on a new line.
  5. End the conversation after displaying the claim status

  If the user asks questions about:
  - Insurance processes
  - Claim eligibility
  - Documentation
  Refer to the “Automobile Insurance Knowledge Base.pdf” knowledge base only. If the answer is not in the knowledge base, reply: “I don’t know.”

  Do not reference the knowledge base while interacting with tools.
  ```
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-15.png">

- No need to change `Channels` settings.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-16.png">

- Click on **Deploy** on both the screens to deploy the agent.
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/customer/customer-17.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/deploy/cca_20.png">
  
#### Test the Customer Claims Agent
  
  Step 1. Enter a basic query:
   ```
   What are the different types of automobile insurance?
   ```

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claims-flow-1.png">

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claims-flow-2.png">

  Step 2. Check the flow for creating a new claim

   Enter the following:
   ```
   Submit a new claim
   ```
   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-3.png">

   **NOTE** your instructor will provide you with a name from the deployed database to use for all of your claims entries. Enter the name provided. Each participant needs to use a different name.

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-4.png">

   For location, enter `St Mary's Street, San Francisco, California` or any other address.

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-5.png">

   For date, enter `23-05-2025` or any other date

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-6.png">

   For vehicle information, enter `Toyota Corolla, 2003` any other vehicle details

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/vehicle_details.png">

   For details, enter: 
   ```
   I was driving to work when a red pickup truck ran a red light and collided with the rear right side of my vehicle at the intersection. The impact caused my car to spin slightly, resulting in damage to the rear bumper, right-side tail light, and a dent in the rear quarter panel. I was wearing a seatbelt and did not sustain serious injuries, but I reported minor back pain and visited a doctor the same day. Medical expenses were $3400 and the damages repair cost was $4500.
   ```

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-7.png">

  Step 3. Check the flow for claim status

   Enter the query

   ```
   Check claim status
   ```

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-8.png">

   Enter the name you were provided

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-10.png">

   For claim number, enter the claim number from the summary of the claim you just created

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim-flow-11.png">

You can create additional claims for your assigned name to test the next agent.

### Claim Processor Agent
#### Create the Claim Processor Agent

- Click on hamburger menu, then **Build** -> **Agent Builder**.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/2.png">

- Click on **Create Agent**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/0.png">

- Follow the steps according the screenshot below.
  - Select **Create from scratch**
  - Name the agent `claim_processor_insurance_agent`
  - Use the following description:

    ```
    The Claim Processor agent assists the claim processor to fetch the open claim request, approve, validate, and verify the open request. This agent will suggest to the claim processor whether they should accept or reject the claim.
    ```

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-1.png">

- Select the `model`.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-2.png">

- Select the Agent Style as `Default`. Also no changes needed for Voice Modality. Keep it as No Voice Configuration

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-3.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-4.png">

- In the **Knowledge** section, add the following to the **Description**:
  ```
  This knowledge base is about insurance and the claim process. This knowledge base will help the claim processor in processing the claims according to the rules and regulations defined by the insurance company. 
  ```
- Download [Policy.pdf](<./data/Policy.pdf>) to your local system, then upload by clicking on **Upload files** under **Documents**. 

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-5.0.png">

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-5.1.png">

- In the **Toolset** section, click on **Add tool**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-6.0.png">

- Click on **Import**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-6.1.png">

- Upload the `claim_processor_agent_tools.json` OpenAPI Spec provided by the instructor

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-7.png">

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-8.png">

    <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-10.png">

- Select all of the **Operations**. Then, select **Done**.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-11.png">


- Click on **Add Agent**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-12.png">
- Click **Add from local instance**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-13.png">

- Select **information_agent** and then the **Add to Agent button**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-14.png">

- In the **Behavior** section, add the following for **Instructions**:
  ```
  You will begin by welcoming the claim processor and displaying the open claims in a table. 
  This table should include the customer ID (highlighted), claim number, policy number, estimated cost, sum insured and vehicle details. Do not show duplicates.

  Ask the claim processor to select a customer ID 

  If there are multiple claims for a customer ID, ask claim processor to select a claim number.

  Use the claim number and customer id to fetch details using the Fetch Open Claims tool, it's very important, return error if unable to run the tool.

  Once a customer ID is selected, fetch the corresponding claim and policy details for that customer ID and show them in a tabular format and then generate summary on the following points

  1. Compare the estimated cost with the sum insured and calculate the approved claim amount by subtracting the deductible. Highlight the approved amount.

  2. Check if the policy is currently active and whether the claim falls within the coverage period.

  3. Classify the accident into one of the following types: rear-end collision, head-on collision, side-impact, sideswipe, single-vehicle, multi-vehicle pileup, hit-and-run, parking lot, animal collision, weather-related, mechanical failure-related, vandalism, or theft.

  4. Determine if the classified accident type is covered by the policy. If policy details are not clear, refer to the knowledge base to verify.

  5. It is mandatory for you to use the information_agent to query for the accident type you discovered in step 4. Query: The rules and regulations for accident type in US. Use the result to verify if the claim details are compliant.

  6. Provide a clear recommendation to accept or reject the claim based on these checks.

  7. Highlight the total claim amount (estimated cost minus deductible).

  8. Create a clear and concise summary for the claim processor, emphasizing key details like approved amount, claim number, and policy number.
  HIGHLIGHT ALL THE DETAILS IN NEAR FORMAT.

  Finally, ask the claim processor "Whether they accept the claim?"
  Do not give next steps. 

  Once a decision is made, update the claim status and send a message confirming that emails have been sent to the customer and finance team.
  ```

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-15.png">

- Keep the `Channels` as it is.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/cp-18.png">

- Click on **Deploy** on both the screens to deploy the agent

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/deploy/cpa_19.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/deploy/cpa_20.png">

#### Test the Claim Processor Agent

  Step 1. Enter the basic query

   ```
   Show open claims
   ```

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/cp-flow-1.png">

  Step 2. Enter a Customer ID from the list

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/cp-flow-2-new.png">

  Step 3. Input Claim Number from the list

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/cp-flow-3.0-new.png">

  Step 4. When prompted to accept the claim respond:

   ```
   Yes
   ```

   <img width="1000" alt="image" src="./screenshots_hands_on_lab/cp-flow-4-new.png">

  Step 5. You should see an update confirmation

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/cp-flow-5-new.png">

### Supervisor Agent
#### Create the Supervisor Agent

- Click on hamburger menu, then **Build** -> **Agent Builder**.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/2.png">

- Click on **Create Agent**

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/claim_processor_insurance_agent/0.png">

- Follow the steps according the screenshot below.
  - Select **Create from scratch**
  - Name the agent `Supervisor Agent`
  - Use the following description:

    ```
    The supervisor_insurance agent will act as an supervisor and depending on the query will pass the query to respective agents for processing. This agent will have two agents, customer_claims_agent, that will allow user to submit a new claim, check their claim status and ask information about insurance and claim process. The other agent is the claim_processor_insurance_agent that will allow the claim processor to view all the top open claims using a customer id, if there are multiple claims for a customer, it will allow the claim processor to select using the claim number. The claim processor can accept or reject the claims based on the suggestion made by the agent. 
    ```

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_1.png">

- Select the `model`.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_2.png">

- Select the Agent Style as `Default`. Also no changes needed for Voice Modality. Keep it as No Voice Configuration

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_3.png">

- Click on `Add agent`. 

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_4.png">

- Add the `customer_claims_agent` and `claim_processor_insurance_agent`. Select the agents mentioned above. Click on `Add to agent`.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_8.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_9.png">

- In the **Behavior** section, add the following for **Instructions**:
  ```
  ## 🎯 Role
  You act as a **supervisor** in the insurance system. Based on the **intent and role** of the user query (customer or claim processor), you must **route the query** to the appropriate agent:

  - `customer_claims_agent`
  - `claim_processor_insurance_agent`

  ---

  ## 🧠 Step-by-Step Instructions

  ### 1. Detect User Role and Intent
  - Analyze the incoming query to determine the **intent**.
  - Identify if the user is a **Customer** or a **Claim Processor**.

  ---

  ### 2. Routing Logic

  #### 🧑 If the User is a **Customer**, route to `customer_claims_agent`

  **Trigger queries include:**
  - "I want to file/submit a claim"
  - "Check my claim status"
  - "Explain the insurance/claim process"
  - "What documents are needed for a claim?"
  - "How long does a claim take to process?"
  - "Where can I track my claim?"

  ✅ **Action**: Forward query to `customer_claims_agent`

  ---

  #### 👨‍💻 If the User is a **Claim Processor**, route to `claim_processor_insurance_agent`

  **Trigger queries include:**
  - "Get all open claims for a customer"
  - "Show me the open claims for customer ID X"
  - "There are multiple claims, help me choose by claim number"
  - "Should I accept or reject this claim?"
  - "View suggestions for processing a claim"
  - "List top unresolved claims for review"

  ✅ **Action**: Forward query to `claim_processor_insurance_agent`

  ---

  ### 3. Handle Invalid or Ambiguous Queries

  If the query is unclear:
  - Ask a clarifying question:
    - "Are you a customer looking to file or check a claim?"
    - "Or are you a claims processor looking to manage claims?"

  ---

  ### 4. Ensure Clear Context Transfer

  When routing, ensure the following is passed to the selected agent:
  - Any `customer_id`, `claim_number`, or other context from the user
  - The user's role (if clarified)
  - The original question or request

  ---

  ### 5. Maintain Logs and Escalate If Needed

  - Maintain a simple internal log of which agent handled which query.
  - If a query doesn't match any known category, escalate to a human supervisor.

  Make sure you follow the agents instruction as is, do not add additional steps or queries.
  ```

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_5.png">

- Keep the `Channels` as it is. 

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_6.png">

- Click on **Deploy** on both the screens to deploy the agent.

  <img width="1000" alt="image" src="./screenshots_hands_on_lab/supervisor_agent/sa_7.png">
  <img width="1000" alt="image" src="./screenshots_hands_on_lab/deploy/sa_20.png">

- You can do the supervisor agent testing according to the below flow. Follow the flow in the sequence mentioned.
  [Test the Information Agent](#test-the-information-agent)
  [Test the Customer Claims Agent](#test-the-customer-claims-agent)
  [Test the Claim Processor Agent](#test-the-claim-processor-agent)


### Further testing via AI Chat
>
> ***You can also test the agents from AI chat.***

Navigate to AI chat by going to the hamburger menu at top left and select **Chat**.

<img width="1000" alt="image" src="./screenshots_hands_on_lab/39.png">

Then select the agent to test: 

<img width="1000" alt="image" src="./screenshots_hands_on_lab/40.png">
<img width="1000" alt="image" src="./screenshots_hands_on_lab/deploy/ai_chat_20.png">

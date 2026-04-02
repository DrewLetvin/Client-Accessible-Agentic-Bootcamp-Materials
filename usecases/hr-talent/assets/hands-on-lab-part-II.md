
# 🧑‍💼 Automating Talent Acquisition with Agentic Workflows

## Table of Contents

- [Use Case description](#use-case-description)
- [Pre-requisites](#pre-requisites)
- [Talent acquisition agent with agentic workflows](#-talent-acquisition-agent-with-agentic-workflows)
     - [Create a Talent Agent](#create-a-new-agent)
     - [Step 1: Create an agentic workflow and configure inputs and outputs](#step-1-create-an-agentic-workflow-and-configure-inputs-and-outputs)
     - [Step 2: User activity to collect number of candidates](#step-2-user-activity-to-collect-number-of-candidates)
     - [Step 3: Code block to store number of candidates](#step-3-code-block-to-store-number-of-candidates)
     - [Step 4: For each loop to upload candidate resumes](#step-4-for-each-loop-to-upload-candidates-resumes)
     - [Step 5: Display message to upload a resume](#step-5-display-message-to-upload-a-resume)
     - [Step 6: Resume file upload](#step-6-file-upload)
     - [Step 7: Document extractor for resumes](#step-7-document-extractor-for-resumes)
     - [Step 8: Store candidate's name and skills](#step-8-store-candidates-name-and-skills-for-later)
     - [Step 9: Display a message to upload a job description](#step-9-display-a-message-to-upload-a-job-description)
     - [Step 10: Upload the job description](#step-10-upload-the-job-description)
     - [Step 11: Document extractor for job skills](#step-11-document-extractor-for-job-skills)
     - [Step 12: Generative prompt - match candidates to job](#step-12-generative-prompt---match-candidates-skills-to-job-skills)
     - [Step 13: Display match summary](#step-13-display-match-summary---output-of-generative-prompt)
     - [Update the agent behavior](#update-agent-behavior)
     - [Test the agent](#test-the-agent)
- [Pulling it all together](#pulling-it-all-together)


## Use Case Description

In the [first part of the HR Talent lab](./hands-on-lab-hr-manager.md) you used the **Chat with documents** feature to upload several resumes and a job description.  You then prompted the agent to generate a table comparing candidates' skills to job required skills. In this case the agent's internal LLM does all the work, all that is required from the user is providing the right prompt/query.  However, sometimes it may not be obvious what the right prompt is as HR Managers are not prompt engineers.  Additionally, we may want to program the agent to run some additional steps, e.g. automatically reach out to the selected candidate, ask them to select an interview time, automatically process the response and add it to the calendar. In this case we may want to create an **agentic workflow**. 

An agentic workflow represents a sequence of steps that utilizes conditional controls and activities. Agentic workflows allow us to create sequences of tasks, as well as conditions, branches and loops.  We can use a variety of nodes, including small code blocks, user input, document processing nodes to extract data from documents, and generative prompts to create and configure LLM prompts with inputs and outputs.

Rather than handling each step individually, agents can start an angetic workflow to manage the entire process from beginning to end. Agentic workflows are ideal for tasks that require coordination across systems or multiple decision points.

For example, an agentic workflow can be created to handle employee onboarding: collecting information, creating accounts, sending welcome emails, and notifying internal teams. Once built, this agentic workflow can be reused across departments, triggered by agents whenever a new employee joins —- no need to manually coordinate each step.

By using agentic workflows, business users gain:

- Confidence that tasks are completed correctly and consistently.
- Speed through automation of repetitive steps.
- Visibility into how processes run and where bottlenecks occur.
- Scalability to apply the same logic across teams, regions, or products.

## Pre-requisites

If you haven't yet as part of the earlier steps of the HR Manager lab, download the following files: 

[Candidate 1.pdf](../data/Candidate%201.pdf)

[Candidate 2.pdf](../data/Candidate%202.pdf)

[Candidate 3.pdf](../data/Candidate%203.pdf)

[Job Description.pdf](../data/Job%20Description.pdf)

## 🥇 Talent Acquisition Agent with agentic workflows 

In this part of the lab we will implement the following workflow: 

![alt text](./hands-on-lab-assets/flow_to_build.jpeg)

We will now walk you through creating the above workflow step by step.  We will first create a separate agent to experiment. 

### Create a new agent

1. Open the Agent Builder in watsonx Orchestrate, if you aren't there already -- click on **Build** in the main hamburger menu. 

![alt text](./hands-on-lab-assets/open_agent_builder.png)

2. Create a new agent:

![alt text](./hands-on-lab-assets/create_new_agent.png)

3. Select **Create from scratch**, name it **Talent Agent**, and give it a short description. Descriptions are used to route a user query to the right agent. You can use the description below:
Name:
```
Talent Aquisition Workflow Agent
```
Description:
```
When asked to match a candidate to a job—or to recommend the best candidate for a given role—always call the Match Candidates tool. This tool contains all available information about candidates and job descriptions, so you should rely entirely on it without requesting clarification or additional details from the user. Always use the Match Candidates tool for any task involving candidate–job alignment.
```
![Add Tool](../assets/hands-on-lab-assets/createfromscratch.png)

4. Click **Create**

5. For this agent, we will use the **GPT OSS 120B** model. You can select it in the **Model** drop-down:

![Add Tool](../assets/images/i16.png)

6. We will leave all the other settings at default values for now.

7. Scroll down to the **Toolset** section. This is where we will be adding our flow (agentic workflow).  Click on **Add Tool**:

![Add Tool](../assets/images/i17.png)

8. Select **Create an agentic workflow**:

![Test Q](../assets/images/i18.png)

### Step 1: Create an agentic workflow and configure inputs and outputs

1. Name the agentic workflow, then clikc **Start building**

![Name Workflow](../assets/images/i19.png)

2. First, we will edit the flow description, input, and outputs.  Click on the pencil next to the name of the flow in the top left corner: 

![Name Workflow](../assets/images/i20.png)

Change description to: 
```
Extracts skills from candidates' resumes, extracts skills from a job description, and generates a summary table showing which candidates have which skills required and preferred for the job.
```
![Name Workflow](../assets/images/i21a.png)

3. Click on **parameters**

![Name Workflow](../assets/images/i21.png)

4. Scroll down and select the **Add output** button to specify the output of the flow: 

![Add Output](../assets/images/i22.png)

This is where we will configure the variable that will store the output of the whole flow, returned to the agent after the flow is done running.  Select **String** for the type of variable: 

![Add Output](../assets/images/i23.png)

Give it a name e.g. **match_summary** and click **Add**: 

![alt text](./hands-on-lab-assets/match_summary_var.png)

After you click on **Add**, your flow show look similar to: 

![alt text](./hands-on-lab-assets/flow_start.png)

The flow has two nodes only for now - the start node with 0 inputs and 0 variables configured, and the end node with 1 variable configured. You can validate that your output variable was added successfully by clicking on the end node: 

![alt text](./hands-on-lab-assets/output_node.png)


We will next configure a couple flow variables that we can use througout our flow.  We will need two: 

- *num_candidates* - a list that represents a range of integers *0* to *n* where *n* is the number of candidates To upload and process multiple candidate resumes, we will use a **For each** node.  In order to do this, we can iteratate over *num_candidates*
- *candidates* - this is a string variable that will hold extracted candidates' names and corresponding skills. We will need it so we can use it in a generative prompt node

Select the icon to add a **flow variable**

![Flow variable](../assets/images/i24.png)

**Add** flow variable: 

![Flow variable](../assets/images/i25.png)

and select **Integer**: 

![Flow variable](../assets/images/i26.png)

Enter following into the variable:
Name:
```
num_candidates
```
Description:
```
list of candidates, enum
```

Check the **List of Integer** option since we will have a list, and click on **Add** to add the variable.

![Flow variable](../assets/images/i27.png)

Next we will add another variable, select **Flow Variable** again

![Flow variable](../assets/images/i24.png)

Select **Add**, then select **String**

![Add Variable](./hands-on-lab-assets/addstring.png)

Enter following into the variable:
Name:
```
candidates
```
Description:
```
candidate names and skills
```

Specify the default (starting) value: "" and click **Add**:

![alt text](./hands-on-lab-assets/candidatesadd.png)


### Step 2: User activity to collect number of candidates

We will now add our first user activity.  The first activity we are going to create will be to ask the user how many candidates they would like to evaluate for the job. 

Hover over the arrow connecting the start node to the end node and click on the **Add +** sign: 

![Add Variable](./hands-on-lab-assets/add+step2.png)

Under User Activities, hover over **Collect from User** and select **Numbber**:

![Add Variable](./hands-on-lab-assets/collectfromusernumber.png)


Click on **Number 1**, then on the pencil icon to edit the question to display to the user: 

![Add Variable](../assets/images/i35.png)

```
How many candidates would you like to evaluate?
```

![Add Variable](../assets/images/i36.png)

Your flow should now look like this: 

![Add Variable](../assets/images/i37.png)

### Step 3: Code block to store number of candidates

We will now define a node to update the *num_candidates* variable: 

Hover over the arrow connecting the user activity to the end node. Click on the **+** sign and hover over **Add a flow activity** and click on on **Logic block**: 

![alt text](./hands-on-lab-assets/flowlogicblock.png)

Click on the new logic block node, and open code editor: 

![alt text](./hands-on-lab-assets/logicblockopencode.png)

Enter the folowing code into the editor: 

```
numc = flow["User activity 1"]["How many candidates would you like to evaluate?"].output.value
flow.private.num_candidates = list(range(0, numc))
```

And click on the **X** to close the editor: 

![alt text](./hands-on-lab-assets/enter_code.png)

Click on the logic block again and rename it using the Edit button (pencil). Name it **store candidate list** and click anywhere outside the box to save.  
![alt text](./hands-on-lab-assets/renamelogicblock.png)


Your flow should now look like the following: 

![alt text](./hands-on-lab-assets/flow_with_code_block.png)

### Step 4: For each loop to upload candidates resumes

We will next create a **for-each loop** to upload each resume, extract the name of the candidate and their skills, and store all this info in the *candidates* variable. 

Hover over the arrow connecting the code block to the end node and click on the **+** sign.
Hover over **Add a flow control** then select **For each**: 

![alt text](./hands-on-lab-assets/addflowcontrolforeach.png)

### Step 5: Display message to upload a resume

Select the **Add** button between Start and End

![Add Variable](../assets/images/i44.png)

Hover over **Present to User** and Select **Message**

![Add Variable](./hands-on-lab-assets/hoveroverpresentmessage.png)


Next click on **Message 1** and edit the **Output message** to:

```
Please upload a candidate's resume
```

This is what will be displayed to the user to ask them to upload a resume.

At the same time change the node name to (to do this, click on the pencil icon): 

```
Prompt user to upload resume
```

![alt text](./hands-on-lab-assets/changedisplayandoutput.png)


### Step 6: File upload

Also within the **For each 1** loop, below **User activity 2**, hover where the red square is in the image.
Hover over **Collect from user**, and select **File Upload**:

![alt text](./hands-on-lab-assets/alsowithinthe.png)


Click on the new *File upload** node and rename it to **Upload resume**: 

![alt text](./hands-on-lab-assets/rename_file_upload.png)

### Step 7: Document extractor for resumes

Next we will create a document extraction node to extract the candidate's name and skills from their resume. 

Still inside the **For each** loop, under the **User activity 3** block, hover over the last arrow (where the red square is) and click on **+**. 
Hover over **Add a flow control** and select **Document extractor**: 

![alt text](./hands-on-lab-assets/lastforeachactivity.png)

Click on the **Document extractor** node and then **Unstructured**: 

![Add Variable](../assets/images/i46.png)

We will now upload one of the resumes as a sample to train the document extractor.  Drag and drop the [Candidate2.pdf](../data/Candidate%202.pdf) file you downloaded earlier in the lab: 

![Add Variable](./hands-on-lab-assets/dragdrop.png)

Once the document is done uploading, you will see the following screen. Click on **Add field** to start adding fields we want to extract and train the document extractor on: 

![FIELDS](../assets/images/i48.png)

Enter the following fields:
```
name
```
```
skills
```

Enter **Name** for the name of the field and hit Enter.  The document extractor will try to extract the name from the resume and will display it once ready: 

![alt text](./hands-on-lab-assets/candidate_name.png)

Next we need to add another field **Skills**. Add one more field and name it **Skills**. Once you hit Enter, the document extractor will populate the field from the document: 

![FIELDS](../assets/images/i49.png)

You can now **x** out of this screen

Rename the document extractor node to **Resume extractor** by clicking on it and editing it's name

Lastly, let's edit the data mapping to ensure that the uploaded resume is passed correctly. Click on **Resume extractor** -> **Edit data mapping**.

<img width="859" alt="image" src="https://github.ibm.com/user-attachments/assets/2d3d4772-4ebd-4e71-b66b-b59377205ced" />

Now, click the **variable** icon next to **document_ref** and find & click on **value** under **Upload Resume** under **User activity 3** as shown below.

<img width="1215" alt="image" src="https://github.ibm.com/user-attachments/assets/f7a4838e-a5aa-4e0c-9730-76be57a50c04" />


Your **For each** loop should now look like this: 

![alt text](./hands-on-lab-assets/for_each_after_extractor.png)

### Step 8: Store candidate's name and skills for later

The last activity we need to create in the **For each** loop is another code block that stores the candidate's name and skills after each iteration.
In the same way you did before, add a Logic Block:

![alt text](./hands-on-lab-assets/anotherlogicblock.png)

Click on the  **Logic block 2** and open the code editor. Enter the following in the code editor: 

```
flow.private.candidates += "Name: " + str(flow["For each 1"]["Resume extractor"].output.name) + "\n\nSkills: " + str(flow["For each 1"]["Resume extractor"].output.skills) + "\n\n"
```

![alt text](./hands-on-lab-assets/logicblock.png)

Rename the code block to **Update candidates**. 

![alt text](./hands-on-lab-assets/updatescandidatescodeblock.png)


The **For each** should now look like this: 

![alt text](./hands-on-lab-assets/for_each_final.png)

### Step 9: Display a message to upload a job description

Next we will ask the user to upload a job description.  First we will display a message to the user, then we will add a file upload activity. 

**Below** the **For each** loop, click on the arrow connecting to the end node: 

![alt text](./hands-on-lab-assets/addarrowplace.png)

Hover over **Present to User** and Select **Message**

![alt text](./hands-on-lab-assets/displaymessagetouser.png)

Double click on the Message node and update the **Output message** to: 
```
Please upload the job description
```
And change the **Display message** (name of the node in the flow) to: 
```
Prompt user to upload job description
```

![alt text](./hands-on-lab-assets/configure_display_to_user_job_upload.png)

### Step 10: Upload the job description

Add another **User activity** right before the end node, under **User activity 4**. 
Hover over **Collect from user** and select **File upload**: 

![alt text](./hands-on-lab-assets/makeitoftypefileupload.png)

Click on the newly created file upload node and change its' name to: 

```
Upload job description
```

![alt text](./hands-on-lab-assets/change_file_upload_job_node_name.png)

### Step 11: Document extractor for job skills

**Under** the user activity 5 node, select the **plus** button

![Add Variable](../assets/images/i54.png)

Hover over **Add a flow activity*, then select the **Document extractor** node.

![alt text](./hands-on-lab-assets/docextractoragain.png)

Select **Unstructured**

![Add Variable](../assets/images/i56.png)

Upload the **job description file**

![Upload file](../assets/images/i57.png)

Once the document has been processed, you will see the following screen: 

![Upload file](../assets/images/i58.png)

Add two fields, similar to what you did for the resume extractor. This time, however, add fields **required** and **preferred** to extract required and preferred skills: 
```
required
```
```
preferred
```

![Upload file](../assets/images/i59.png)

Close the extractor node once done. 

Rename your Document Extractor to **Extract job skills**

### Step 12: Generative prompt - match candidates' skills to job skills

We are finally almost at the end of the flow. We still need to implement a Generative prompt.  This prompt will take as input the value of *candidates* variable, which is a string that contains by now all candidate names and their skills.  It will also take as input the required and preferred skills just extracted from the job description. The prompt will compare the skills of each candidate to the skills required by the job and generate a table which summarizes how well candidate skills map to the job description.

Add a **Generate prompt** node at the end of the flow (before the end node). To do this, hover over **Add a flow activity**, then select **Generative Prompt**: 

![alt text](./hands-on-lab-assets/generativepromptadd.png)


For system prompt enter the following: 

```
You are a helpful assistant who can match candidates skills to job requirements.
```

For user prompt enter: 

```
Make a table where each row is a candidate and each column is a skill in the job description. Do not invent any candidates. Have the check emoji if the candidate does have the corresponding skill. Mark columns for required job skills with *. Include the candidate's name in each row.

Candidate names and skills: 
Required job skills: 
Preferred job skills:
```

Change the model type to **GPT-OSS 120b**

![Upload file](../assets/images/i60.png)

In order to work, our generative prompt will need to take **as input** a string that contains candidate names and skills extracted earlier in the flow. It will also need two strings for skills (required and preferred) from the job description itself. Therefore, we need to create three _String_ input varilables that will hold these values and that we can reference in the user prompt as variables. 

We can also provide a sample test value for each variable so we can run the prompt directly in the generative prompt editor and double check that the output is as expected, without having to quit and run the whole flow. 

Add the following _String_ input variables: *candidates*, *job_required*, and *job_preferred* and assign some test values e.g.: 

![alt text](./hands-on-lab-assets/create_new_var_gp.png)

Fill in the name of the var and add a simple description: 

```
candidates
```
```
candidate name and skills
```

![alt text](./hands-on-lab-assets/create_candidates_var_gp.png)

Edit the var to add a test value: 

![alt text](./hands-on-lab-assets/add_test_value.png)

Paste the following text to add the value: 

```
Name: Jane Smith
Skills: Java, Javascript

Name: John Doe
Skills: Java, Python, Javascript, ML
```

Your _candidates_ variable show now look like this:

![alt text](./hands-on-lab-assets/prompt_candidates_var.png)

Add two more variables, **Job Required** and **Job Preferred**
```
job_required
```
```
job_preferred
```

![Job Vars](../assets/images/i61.png)

Finally reference these variables in your prompt by clicking the **{x}** sign in the user prompt area: 

![Job Vars](../assets/images/i62.png)
![Job Vars](../assets/images/i63.png)

Repeat this until the prompt looks as follows:

![Job Vars](../assets/images/i65.png)

Edit the job_required to add a test value: 

Paste the following text to add the value to input variable of job_required: 

```
Java, Javascript, Python, ML
```

Click on **Generate preview** to run the prompt on the test values you provided and observe the results returned: 

![Job Vars](../assets/images/i64.png)

As you can see, the result is a table which compares each candidate's skills with the job requirements.  This is exactly what we were looking for, so we have validated that our generative prompt works and can move on to the next step.

![Job Vars](../assets/images/i66.png)

Close the prompt definition now.
Click on the Generative prompt node you just created and rename it to **Match candidate skills to job skills**. Then click **Edit data mapping**: 

![alt text](./hands-on-lab-assets/theneditdatamapping.png)

We now need to map data collected earlier in the flow to the inputs of the generative prompt.

 Click on the **variable** icon in the *candidates* row: 

![Job Vars](../assets/images/i67.png)

In the editor select **Flow variables -> candidates**: 

![Job Vars](../assets/images/i68.png)

For *job_preferred*, also select the **variable icon** and choose **Extract job skills -> preferred**

![Job Vars](../assets/images/i69.png)

![Job Vars](../assets/images/i70.png)

Similarly, for *job_required* select the variable icon and chooose **Extract job skills -> required**

![Job Vars](../assets/images/i71.png)

![Job Vars](../assets/images/i72.png)

### Step 13: Display match summary - output of generative prompt

Finally, create one last **Message** node to display the output of the generative prompt. To do this hover over **Present to user** and select **Message**: 

![alt text](./hands-on-lab-assets/presentmessage.png)

Update the node name to **Show summary** and click on **Select variable** to select the output message: 

![alt text](./hands-on-lab-assets/edit_output_node.png)

In the editor select the generative prompt node name, then select the corresponding output variable *value*:

![alt text](./hands-on-lab-assets/select_prompt_output_var.png)

We are finally done defining the flow.  Click on **Done** to close the flow. 

![User Activity 6](../assets/images/i75.png)

### Update Agent Behavior

Before testing the agent, let's complete the **Behavior** section. Use the following instructions: 

```
When asked to match a candidate to job or to recommend the best candidate for a job, call the 'Match candidates' tool.  All other questions should be answered based on the context in the chat.
```

![alt text](./hands-on-lab-assets/behavior.png)

### Test the agent

Test your agent by providing two candidate resumes.  Enter the following query in chat: 

```
recommend a candidate for a job
```

The agent will ask you how many candidates you would like to evaluate.  Answer: 2

You will then be asked to upload a candidate's resume. You can upload any candidate's resume, for example [Candidate 3.pdf](../data/Candidate%203.pdf).  Note you may be asked to review the extraction results - if the extractor's confidence is below 95%, human validation will be required.  This behavior can be easily configured within the document extractor node. The same is true for any other uploaded documents.

You will then be asked to upload the second resume.  You can upload another candidate's resume, for exmaple [Candidate 1.pdf](../data/Candidate%201.pdf). 

You will finally be asked to upload a job description.  You can use [Job Description.pdf](../data/📄%20Job%20Description.pdf). 

The results should look similar to the following: 

![alt text](./hands-on-lab-assets/table_output.png)

As you can see, the columns marked with * are skills required by the job.  Other skills are preferred.
Each candidate row shows which skills the candidate has.

The agent summarizes by telling us who the recommended candidate is: 

![alt text](./hands-on-lab-assets/recommended_candidate.png)

## Pulling it all together

In this part of the lab we automated the process of extracting skills from resumes and the job description and summarizing how well the candidates' skills match the skills required and preferred for the job.  We used **document processing** nodes to define the fields to be extracted from documents and to train the document processor. We then fed the output of the document processing nodes as input into the **generative prompt** node which composed the right prompt for the LLM to summarize how well candidate skills match the job requirements.
We could easily expand this workflow with additional nodes and branches, for example to send an email to the highest-ranked candidates, to ask them to pick an interview slot, and to confirm their response was received. Running these tasks as a workflow allows for a more deterministic way to handle repetitive tasks, so that the agent can drive the process and involve the HR Manager know whenever their input is needed.

As you noticed when you tested the flow, depending on how the confidence thresholds are set up in the document processing nodes, human verification can be requested to make sure field data is extracted correctly.  

Combining agentic workflows with regular tools and individual tasks in an agent provides the greatest flexibility. A user can chat with the agent and invoke individual tasks as needed.  For more complex, multi-step processes, agentic workflows are a powerful tool that can manage the entire process from beginning to end.



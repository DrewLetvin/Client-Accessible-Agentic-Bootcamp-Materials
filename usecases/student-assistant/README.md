# Student Assistant

This use case demonstrates how to build an AI-powered Student Assistant using IBM watsonx Orchestrate. The assistant helps students navigate institutional policies, access campus resources, and get answers to common questions about Vassar College.

## 🤔 The Problem

Students at Vassar College face several challenges when trying to navigate institutional information:

1. **Complex Policy Language** - Academic policies, student conduct guidelines, and administrative procedures are often written in formal language that can be difficult to understand
2. **Scattered Resources** - Important campus resources (VPN access, JobX portal, CIS service status) are distributed across multiple platforms
3. **Information Overload** - Finding specific information among hundreds of pages of policies, blogs, and web content is time-consuming
4. **Limited Support Hours** - Students need answers outside of regular office hours when administrative staff may not be available

These challenges lead to:
- Confusion about policies and procedures
- Missed opportunities due to lack of awareness of available resources
- Increased burden on administrative staff answering repetitive questions
- Student frustration and decreased satisfaction

## 🎯 Objective

The primary objective is to design and implement an Agentic AI-enabled Student Assistant that:

1. **Translates Policy Language** - Converts complex institutional policies into clear, student-friendly explanations
2. **Clarifies Common Processes** - Provides step-by-step guidance for common procedures (registration, financial aid, housing, etc.)
3. **Directs to Resources** - Intelligently routes students to appropriate campus resources and platforms
4. **Provides Institutional Clarity** - Answers general questions about Vassar College using verified information

The system leverages watsonx Orchestrate's multi-agent architecture to ensure accurate, trustworthy responses while maintaining transparency in how information is sourced and processed.

## 📈 Business Value

The Student Assistant delivers significant value to both students and the institution:

**For Students:**
- **24/7 Availability** - Get answers anytime, not just during office hours
- **Instant Responses** - No waiting in queues or navigating complex websites
- **Clear Communication** - Policy language translated into understandable terms
- **Personalized Guidance** - Directed to the right resources for their specific needs

**For the Institution:**
- **Reduced Administrative Burden** - Fewer repetitive inquiries to staff
- **Improved Student Satisfaction** - Better access to information and support
- **Consistent Information** - All students receive accurate, up-to-date guidance
- **Scalability** - Handle unlimited concurrent student queries
- **Data Insights** - Understand common student questions and pain points

**Trust and Governance:**
- **Transparency** - Students can see how answers are sourced
- **Accuracy** - Responses grounded in official institutional documents
- **Privacy** - Student queries handled securely
- **Auditability** - All interactions logged for quality assurance

## 🏛️ Architecture

The Student Assistant uses a multi-agent architecture within watsonx Orchestrate:

![Student Assistant Architecture](./assets/images/student-asssistant-architecture.png)

### Architecture Components:

**User Interface Layer:**
- watsonx Orchestrate Chat Interface - Natural language interaction point for students

**Agent Layer:**
1. **Orchestrate Agent** (Router)
   - Routes student queries to the appropriate specialized agent
   - Coordinates responses from multiple agents when needed
   
2. **Policy Agent**
   - Specializes in interpreting and explaining institutional policies
   - Connected to Policy Elastic Index containing Vassar policy documents
   
3. **Resources Agent**
   - Directs students to appropriate campus platforms and services
   - Uses Redirect Glossary Tool for platform links
   - Maintains knowledge base of resource descriptions
   
4. **General Knowledge Agent**
   - Answers general questions about Vassar College
   - Connected to Policy Elastic Index with general institutional information

**Data Layer:**
- **Vassar Policy Data** - Academic policies, student conduct guidelines, administrative procedures
- **Platform Redirect Links** - URLs and access information for VPN, JobX, CIS service status, etc.
- **General Vassar Info** - Public webpage data, blogs, key institutional information

## 🛡️ Pillars of Trust

This bootcamp emphasizes IBM's Pillars of Trust throughout the implementation:

1. **Transparency** - Students can see which agent and data sources were used to answer their questions
2. **Explainability** - The system provides reasoning for its responses and recommendations
3. **Fairness** - All students receive equal access to information regardless of background
4. **Robustness** - The system handles edge cases and unclear queries gracefully
5. **Privacy** - Student queries are handled securely and not used for unintended purposes
6. **Accountability** - All interactions are logged and can be audited for quality assurance

## 📄 Step-by-step Hands-on Instructions

You can find comprehensive step-by-step instructions in the following documents:

- **[Lab Overview](./hands-on-lab-overview.md)** - Introduction and table of contents
- **[Part I: Building Specialized Agents](./hands-on-lab-part-I.md)** - Create Policy, Resources, and General Knowledge agents
- **[Part II: Building the Orchestrator](./hands-on-lab-part-II.md)** - Create the main Student Assistant agent that routes queries

## 🎓 Learning Objectives

By completing this bootcamp, participants will:

1. Understand how to design multi-agent systems for institutional use cases
2. Learn to configure agents with appropriate knowledge sources
3. Implement agent routing logic for complex query handling
4. Apply Trust principles to AI system design
5. Test and validate agent behavior for accuracy and reliability
6. Deploy and monitor production-ready AI assistants

## 📚 Prerequisites

**Participants should have:**
- Access to IBM watsonx Orchestrate instance
- Completed the [environment-setup](../../environment-setup) guide
- Basic understanding of AI agent concepts
- Familiarity with institutional policies and resources (helpful but not required)

**Instructors should:**
- Review the instructor's guide for environment setup
- Prepare sample Vassar policy documents
- Configure access to policy data sources
- Set up monitoring and analytics dashboards

## Demo Video

[Placeholder for demo video showing the Student Assistant in action]

## Additional Resources

- [Agent Monitoring Guide](./agent-monitoring.md) - Learn to monitor and evaluate agent performance
- [Agentic Flow Inspector](./agentic-flow-inspector.md) - Debug and optimize agent workflows
- [Vassar College Policies](https://www.vassar.edu/policies) - Official policy repository
- [IBM watsonx Orchestrate Documentation](https://www.ibm.com/docs/en/watsonx/watson-orchestrate)
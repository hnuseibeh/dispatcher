

# **The Reasoning-Centric SDLC: A Framework for Classifying, Routing, and Scaling AI in Software Engineering**

## **Executive Summary**

The integration of Artificial Intelligence (AI) into the Software Development Lifecycle (SDLC) presents a dual-faced opportunity. On one side, it promises unprecedented gains in productivity by automating repetitive tasks and accelerating code generation.1 On the other, unstructured and naive adoption of these powerful tools risks introducing subtle, systemic flaws, increasing technical debt, and degrading long-term code maintainability.3 The central challenge for technology leadership is to harness AI's potential while systematically managing its inherent complexities and risks. This report introduces a comprehensive framework designed to address this challenge by moving beyond ad-hoc AI usage toward a structured, quality-driven integration strategy.

At the core of this framework is a four-tier reasoning taxonomy that classifies AI-driven coding tasks not by their superficial description, but by the depth of cognitive work required for their successful completion. These tiers—Shallow, Procedural, Architectural, and Strategic—represent a progressive escalation in reasoning complexity, task scope, and the necessary level of AI autonomy. This classification provides a robust conceptual model for understanding the capabilities and limitations of current and future AI systems in the context of software engineering.

The operational heart of this framework is the Reasoning-to-Agent Routing Guide. This guide provides a blueprint for an intelligent system that analyzes incoming development tasks, classifies them according to the reasoning taxonomy, and routes them to the most appropriate AI model, tool, or agentic system. The guide is presented as a detailed matrix complete with quantifiable thresholds, clear escalation paths for handling failures, and success metrics for each tier. This system is designed to match task complexity with the appropriate level of AI capability, thereby maximizing efficiency while proactively mitigating the risks of misapplication.

Ultimately, this report argues that a reasoning-centric approach is the essential next step in the evolution of software development. It provides a strategic roadmap for technology leaders to transition from isolated experiments with AI coding assistants to a fully integrated, scalable, and quality-controlled ecosystem. By systematically classifying tasks, routing them to appropriate agents, and continuously monitoring performance, organizations can build a resilient and adaptive SDLC that not only leverages AI for immediate productivity gains but also fosters long-term code health and prepares for the next generation of autonomous software engineering capabilities.

---

## **Section 1: The Spectrum of AI Reasoning in Code Generation: A Foundational Taxonomy**

To effectively manage AI in software development, it is imperative to first establish a foundational understanding of how AI "thinks" about code. The capabilities of modern AI systems extend far beyond simple pattern matching; they involve a spectrum of reasoning processes that are uniquely cultivated by the logical nature of programming. This section introduces a taxonomy that deconstructs this spectrum, providing the conceptual model that underpins the entire routing framework.

### **1.1 The Symbiotic Relationship Between Code and Reasoning**

The interaction between Large Language Models (LLMs) and computer code is not a one-way street of generation; it is a virtuous, reinforcing cycle. The abstract, modular, and logic-driven structure of programming languages provides a unique and powerful "training ground" for strengthening an LLM's general reasoning capabilities. Conversely, as an LLM's reasoning abilities improve, it becomes more adept at complex coding tasks, such as task decomposition, code comprehension, and debugging.4

This bidirectional relationship explains a critical phenomenon: when LLMs gain proficiency in coding, they demonstrate significantly enhanced performance in seemingly unrelated domains like mathematical deduction and logical inference.4 The rigorous structure of code forces the model to develop a more disciplined and logical mode of token prediction, which translates into a more general problem-solving ability. This symbiotic dynamic is the foundational premise for using AI in software engineering. It suggests that code-specialized models are not merely static databases of code snippets but are systems that can develop emergent, flexible problem-solving skills. The core function of reasoning in this context is to translate high-level, often ambiguous human goals into the smaller, discrete, and executable steps required to produce functional code.4 Understanding this cycle is the first step toward building systems that can leverage it effectively.

### **1.2 A Taxonomy of Reasoning in AI Systems**

AI systems do not rely on a single form of logic. Instead, they employ a combination of reasoning strategies, drawing upon different approaches depending on the task at hand.5 For the domain of software engineering, several types of reasoning are particularly relevant:

* **Deductive and Inductive Reasoning:** These are the most fundamental forms of logic for code. Deductive reasoning involves applying a general rule to a specific instance—for example, knowing that a language requires semicolons at the end of every statement (a general principle) and deducing that a specific line of code is syntactically incorrect because it lacks one. Inductive reasoning works in reverse, inferring a general rule from specific examples. By analyzing thousands of well-written functions, a model can induce the common patterns and best practices for that language.6 These two forms are the bedrock of basic code generation and comprehension.  
* **Abductive Reasoning:** This is the process of formulating the most likely explanation for a given set of observations. In software development, this is the essence of debugging. When faced with an error message and a stack trace, a developer (or an AI agent) uses abductive reasoning to infer the most probable cause of the failure from a wide range of possibilities.5  
* **Causal Reasoning:** A more advanced cognitive task, causal reasoning involves understanding the intricate cause-and-effect relationships within a system. This goes beyond correlation to predict the downstream consequences of a change. For example, understanding not just that modifying a function will fix a bug, but also predicting how that change might impact performance or affect other dependent modules. Most LLMs still struggle with deep causal reasoning, though the integration of tools like a code interpreter has been shown to enhance this capability by allowing the model to execute code and observe its effects directly.7  
* **Agentic Reasoning:** This is the capability that enables an AI to move from being a passive tool to an autonomous actor. Agentic reasoning allows an AI to formulate a plan, select tools, and execute a sequence of actions to achieve a specified goal.5 Simple agents may rely on preset rules, but more advanced, goal-based agents can dynamically plan and adapt their actions to navigate complex, multi-step tasks. This form of reasoning is the cornerstone of the more advanced tiers of the coding taxonomy, enabling the transition from simple code completion to end-to-end software development.8

### **1.3 The Four-Tier Classification of AI Coding Tasks**

Building upon this understanding of AI reasoning, we can construct a hierarchical classification of coding tasks. This framework organizes tasks based on the depth of reasoning required, which correlates directly with the task's scope, complexity, and the necessary level of AI autonomy.

* **Tier 1: Shallow:** Tasks at this level require minimal reasoning, relying primarily on pattern recognition and deductive inference based on learned syntax. The scope is highly localized, often limited to a single line or a small block of code.  
* **Tier 2: Procedural:** These tasks demand algorithmic and localized causal reasoning. The AI must understand control flow, data structures, and the logic within a self-contained unit, such as a single function or file.  
* **Tier 3: Architectural:** This tier requires the AI to reason across multiple files, modules, and system components. It involves systemic and analogical reasoning to understand dependencies, API contracts, and the broader implications of code changes.  
* **Tier 4: Strategic:** The highest level of complexity, these tasks necessitate collaborative and recursive reasoning. They are typically too large or multifaceted for a single agent and require a team of specialized AI agents to decompose the problem, delegate sub-tasks, and integrate the results.

It is crucial to recognize that this classification is not based on the superficial name of a task (e.g., "bug fix") but on the intrinsic cognitive process required to complete it. A simple typo fix is a Shallow task, while a bug caused by a race condition between two microservices is an Architectural or even Strategic task. This nuanced distinction is essential for effective routing.

A significant challenge in applying this framework arises from the nature of LLM cognition itself. Extensive research reveals that even frontier models can achieve high scores on benchmarks while failing on slightly modified versions of the same problems.10 This indicates that their success often stems from sophisticated pattern matching—essentially replicating reasoning steps observed in their vast training data—rather than from genuine, abstract logical deduction.11 This creates an "illusion of reasoning," where a model can produce code that appears correct and passes simple tests but is logically brittle or contains subtle flaws that manifest only under specific edge cases. The primary risk in an AI-driven SDLC is therefore not outright failure, but success for the wrong reasons. Consequently, any robust routing system must not only classify the apparent complexity of a task but also assess the required

*robustness* of the reasoning. Tasks that demand high logical consistency and generalization, such as the design of a novel algorithm, must be routed to systems with built-in validation and iterative refinement loops, rather than relying on a single, unverified generation.

To make this classification system practical and quantifiable, it is necessary to move beyond abstract labels like "easy" or "hard." A powerful emerging metric for this purpose is the "50%-task-completion time horizon." This metric quantifies task complexity by measuring the time it would typically take a human expert to complete a task that an AI system can complete with a 50% success rate.12 Recent studies show that current frontier models have a time horizon of approximately 50 minutes, and this capability has been doubling roughly every seven months.13 This provides a continuous, empirical scale for task complexity that can bridge the gap between human and AI capabilities. This quantifiable metric serves as the cornerstone for the thresholds in the routing guide presented later in this report, allowing the system to be both precise and adaptive to the rapid evolution of AI technology.

### **Table 1: The Reasoning-Based Taxonomy for AI Coding Tasks**

| Reasoning Tier | Primary Reasoning Type | Task Scope | Core Function | AI's Role | Human Effort Horizon (Proxy) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Shallow** | Pattern Matching & Deductive Inference | Single line/block | Code Completion & Linting | Augmentative Assistant | \< 5 minutes |
| **Procedural** | Algorithmic & Local Causal Reasoning | Single function/file | Function Implementation & Testing | Competent Implementer | 5 minutes \- 2 hours |
| **Architectural** | Systemic & Analogical Reasoning | Multiple files/modules | System Refactoring & Design | System Architect | 2 hours \- 1 day |
| **Strategic** | Collaborative & Recursive Reasoning | Entire codebase/system | End-to-End Feature Development | Autonomous Team | 1 day \- 1 week |

---

## **Section 2: A Multi-Tiered Analysis of AI Coding Tasks: Models, Failures, and Best Practices**

This section provides a detailed analysis of each reasoning tier, outlining the specific task types, preferred AI tools and models, common failure modes that arise from mis-routing, and the intermediate steps required to ensure successful outcomes. This granular examination forms the evidence base for the operational routing guide.

### **2.1 Tier 1: Shallow Reasoning (Pattern Recognition & Syntactic Correction)**

#### **Definition and Task Examples**

Shallow reasoning tasks are the most common and immediate application of AI in coding. They operate at a highly localized level, typically within a single line or a small, contiguous block of code. These tasks do not require a deep understanding of the program's overall logic or semantics; instead, they rely on the AI's vast knowledge of syntactic rules and common coding patterns learned from its training data.6 The AI's role here is that of an advanced, context-aware autocomplete and linter, augmenting the developer's workflow rather than automating it.14

These tasks fall primarily into the PL-PL (Programming Language to Programming Language) or simple NL-PL (Natural Language to Programming Language) categories.15 Concrete examples include:

* **In-line code completion:** Suggesting the remainder of a line or a small block of code as the developer types.  
* **Variable and function renaming:** Applying a name change consistently within a limited scope.  
* **Syntax error correction:** Identifying and fixing common errors like missing parentheses, commas, or semicolons.  
* **Boilerplate generation:** Creating the basic structure for a class, function, or file based on a simple command (e.g., generating an empty \_\_init\_\_ method in Python).  
* **Docstring generation:** Adding documentation to a simple, self-contained function with clear inputs and outputs.

#### **Preferred AI Models and Tools**

The primary requirements for tools operating at this tier are low latency and seamless integration into the developer's existing environment. The goal is to provide instantaneous feedback without disrupting the flow of coding. Therefore, the preferred models are typically lightweight, decoder-only architectures that are specifically optimized for speed and responsiveness.15

The most effective tools are those embedded directly within the Integrated Development Environment (IDE) or command-line interface. Prominent examples include:

* **GitHub Copilot:** One of the most widely adopted tools, providing real-time, in-line suggestions within editors like VS Code.16  
* **Amazon CodeWhisperer:** A similar tool that offers code suggestions and security scans.  
* **Claude Code CLI:** A command-line interface tool that can be used for quick, conversational coding assistance, suitable for generating small snippets or commands.14

These tools are designed to be augmentative, acting as a "pair programmer" that handles the most repetitive and syntactically predictable parts of coding, freeing up the developer's cognitive resources for more complex problem-solving.1

#### **Failure Modes if Misrouted**

The primary danger of Shallow-tier tools lies in their misapplication to tasks that require deeper reasoning. When a developer attempts to use a simple autocomplete tool to generate a complex logical block (a Procedural task), the model is forced to operate beyond its capabilities. The result is often code that is syntactically correct but logically flawed, inefficient, or insecure.

This failure mode is a primary driver of what has been termed "AI-induced tech debt".3 The AI, relying on superficial pattern matching, may generate a solution that looks plausible but does not correctly handle edge cases or integrate properly with the surrounding code. This leads to a high "code churn" rate, a metric that tracks the percentage of code that is rewritten or deleted within a short period (e.g., two weeks) of being committed. Studies have shown that as AI assistant usage has grown, so has code churn, suggesting that while code is being written faster, it requires significantly more revision to become production-ready.3 The composition of this AI-generated code often resembles "copy/pasted" snippets, lacking the thoughtful integration that a human developer would provide, further exacerbating long-term maintenance burdens.3

#### **Suggested Intermediate Steps for Success**

Mitigating the risks of Shallow-tier tools requires a combination of human vigilance and organizational policy.

* **Human Oversight as a Mandate:** Developers must be trained to treat AI suggestions as *proposals* to be critically evaluated, not as infallible final code. The human developer's reasoning is the ultimate quality gate.  
* **Clear Policies and Guardrails:** Leadership must establish and enforce clear guidelines on the appropriate use cases for these assistants. For example, policies might state that AI assistants are approved for boilerplate and syntax correction but require explicit human review for any block of code containing business logic.1  
* **Integration with Traditional Quality Tools:** All AI-generated code, no matter how trivial it seems, should be immediately subjected to automated linting and static analysis. These traditional tools are effective at catching many of the stylistic and syntactical errors that can be introduced by pattern-matching AI.

### **2.2 Tier 2: Procedural Reasoning (Algorithmic Implementation & Local Logic)**

#### **Definition and Task Examples**

Procedural reasoning tasks represent a significant step up in cognitive complexity. They require the AI to understand and correctly implement a self-contained algorithm or a complete logical procedure. This involves reasoning about variables, data structures, control flow (loops, conditionals), and the cause-and-effect relationships within the scope of a single function or file. The AI is no longer just an assistant; it acts as a competent implementer capable of translating a well-defined specification into functional code.

These tasks are the focus of many popular code generation benchmarks like HumanEval and MBPP, which test a model's ability to solve small, well-defined programming challenges.12 Examples of Procedural tasks include:

* **Function generation from a detailed specification:** Taking a natural language description, often in the form of a detailed docstring or comment, and generating the complete, executable function body (a core NL-PL task).  
* **Unit test generation:** Reading an existing function and generating a comprehensive suite of unit tests that cover its primary logic, edge cases, and potential failure modes.  
* **Algorithm implementation:** Implementing a standard algorithm (e.g., binary search, quicksort) based on a high-level request.  
* **Language translation:** Converting a function from one programming language to another (e.g., Python to JavaScript), which requires understanding the semantics of both languages (a PL-PL task).  
* **Complex loop or logic refactoring:** Rewriting a dense or inefficient block of code to be more readable, performant, or idiomatic, without changing its functional output.

#### **Preferred AI Models and Tools**

Tasks at this tier demand more than just pattern matching; they require genuine reasoning ability. Therefore, they are best handled by state-of-the-art, frontier foundation models known for their strong logical and coding capabilities, such as models from the GPT-4 series, Claude 3 family, or Google's Gemini Advanced.16

Success at this tier is less about the IDE plugin and more about the prompting techniques used to elicit the model's reasoning capabilities. Effective strategies include:

* **Chain-of-Thought (CoT) and Program-of-Thoughts (PoT):** These techniques instruct the model to externalize its thinking process. With CoT, the model is prompted to "think step-by-step," breaking down the problem into a logical sequence before writing the final code. PoT takes this a step further, asking the model to generate the entire reasoning process as an executable program itself, which can improve accuracy on numerical or highly logical tasks.4  
* **Chain-of-Simulation (CoSm):** For tasks that involve predicting program behavior, CoSm is a powerful technique. It prompts the model to perform a line-by-line simulation of the code's execution, tracking the state of variables at each step. This forces a deeper level of semantic understanding and helps the model avoid shallow pattern recognition.6  
* **Retrieval-Augmented Generation (RAG):** To prevent the AI from generating code in a vacuum, RAG is used to provide it with relevant context from the existing codebase. Before generating a new function, the system can retrieve and include related data models, utility functions, or examples of similar functions in the prompt. This grounds the AI's output in the project's specific conventions and architecture.20

#### **Failure Modes if Misrouted**

The danger at the Procedural tier arises when a single-function agent is given a multi-component, system-level problem (an Architectural task). For instance, if a developer asks a Procedural-level agent to "implement our new user authentication system," the agent will likely interpret this as a request to generate a single, large block of code.

The resulting failure is one of scope and abstraction. The agent might produce a syntactically correct and locally functional script that handles user login. However, it will almost certainly fail to consider critical cross-cutting concerns. It will likely hardcode database connections instead of using a configuration service, neglect to add proper logging or metrics instrumentation, ignore security best practices like password hashing and salting, and fail to define a clean API contract for other services to use. It solves the immediate, local problem of "logging a user in" but creates a massive, systemic problem of poor design, insecurity, and unmaintainability. This leads to a situation where the initial "productivity gain" is completely erased by the extensive rework required to properly architect the solution.3

#### **Suggested Intermediate Steps for Success**

To use Procedural-level agents effectively, the human developer must perform the higher-level reasoning first, breaking down the problem into appropriate chunks.

* **Human-Led Task Decomposition:** The developer's primary role is to act as the architect. They must take the large, architectural goal (e.g., "build an auth system") and decompose it into a series of well-defined, self-contained procedural sub-tasks (e.g., "write a function to securely hash a password," "write a function to generate a JWT," "write a set of unit tests for the password hashing function").  
* **Test-Driven Development (TDD) as a Specification:** One of the most effective ways to guide a Procedural agent is to provide it with a set of failing unit tests. The tests serve as a clear, executable, and unambiguous specification of the required behavior. The agent's goal then becomes simply "make these tests pass."  
* **Iterative Refinement and Feedback Loops:** The most robust workflows involve a tight feedback loop. The AI generates code, which is then automatically compiled and run against the provided tests. The output, including any compiler errors or test failures, is then fed back into the prompt, instructing the AI to correct its mistakes. This iterative process, where the agent learns from execution feedback, dramatically improves the reliability of the final output.4

### **2.3 Tier 3: Architectural Reasoning (System-Level Design & Abstraction)**

#### **Definition and Task Examples**

Architectural reasoning tasks require the AI to operate across a broader scope, reasoning about the interactions and dependencies between multiple files, modules, or even microservices. This level of complexity demands more than just understanding a single algorithm; it requires a grasp of software architecture principles, system design patterns, API contracts, and the long-term consequences of structural changes. The AI must employ systemic reasoning (understanding the whole system) and analogical reasoning (applying known solutions to similar new problems). Here, the AI transitions from an implementer to a system architect's assistant or even a junior architect itself.

The human effort horizon for these tasks typically ranges from a few hours to a full day.12 Examples include:

* **Large-scale refactoring:** Proposing and executing a plan to refactor a monolithic application into a set of communicating microservices.  
* **New API design:** Designing the endpoints, request/response schemas, and data contracts for a new public-facing or internal API.  
* **Database schema generation:** Creating a normalized database schema based on a high-level description of the application's data requirements.  
* **Cross-component bug resolution:** Diagnosing and fixing a complex bug whose root cause lies in the interaction between two or more distinct services.  
* **Feature implementation planning:** Given a new feature request, generating a detailed technical plan that outlines the necessary changes across the frontend, backend, and database components.

#### **Preferred AI Models and Tools**

Tasks at this tier are too complex for a simple prompt-response interaction. They require a persistent, stateful process that can plan, act, and learn over an extended period. This necessitates the use of **single, highly-capable agentic systems**. These are not just models but frameworks that equip an LLM with essential capabilities like planning, tool use, and memory.

Key frameworks and their roles include:

* **LangChain and LangGraph:** LangChain provides the fundamental building blocks for creating custom agents: chains for sequencing calls, tool integrations for interacting with the environment (e.g., reading files, executing shell commands), and memory modules for maintaining context.21 LangGraph extends this with a graph-based architecture, which is ideal for the complex, often cyclical workflows of architectural tasks. It allows the agent to create a plan, execute a step, evaluate the result, and then decide whether to proceed, retry, or ask for human input, making it perfect for stateful operations.22  
* **Microsoft Semantic Kernel:** This framework excels at orchestrating a combination of LLM calls ("prompts") and traditional code ("skills"). Its built-in planner can take a high-level goal and automatically compose a sequence of skills to achieve it. This makes it particularly well-suited for integrating AI reasoning into existing enterprise applications and legacy systems, where much of the logic is already encapsulated in native code.21

The core capabilities these frameworks enable are **tool use** (the ability to interact with the file system, run tests, call APIs, etc.) and **memory** (the ability to retain context, remember past actions, and learn from previous errors throughout a long-running task).

#### **Failure Modes if Misrouted**

The failure mode for an Architectural-level agent occurs when it is assigned a task of overwhelming scope and ambiguity, a Strategic-level problem. For example, if a single agent, no matter how capable, is given the prompt, "Build our new e-commerce platform from scratch," it is being set up for failure.

The agent may successfully generate a high-level architectural plan. However, it will inevitably become a bottleneck during execution. A single agent cannot effectively manage the parallel development, specialized knowledge, and distinct debugging cycles required for the frontend UI, the backend order processing logic, the database management, and the cloud deployment infrastructure all at once. It lacks the parallel processing and diverse expertise of a human team. As the complexity and duration of the task increase, the probability of the agent getting stuck in a loop, losing critical context, or failing to resolve conflicting requirements grows exponentially. Research on AI task completion shows a sharp drop-off in success rates for tasks that take humans more than a few hours to complete, which is precisely the boundary between Architectural and Strategic complexity.13

#### **Suggested Intermediate Steps for Success**

Successfully deploying Architectural-level agents requires a fundamental shift in the developer's role from a hands-on coder to a manager and overseer of an AI workforce of one.

* **Human as "The Architect":** The developer's primary responsibility is to define the strategic goal, review and approve the agent's proposed technical plan, and monitor its execution. They provide the high-level direction and critical judgment that the agent lacks.  
* **Provide Clear, Executable Feedback:** AI agents struggle to improve without clear feedback signals.12 The development environment must be instrumented to provide this feedback automatically. For example, a suite of integration tests that the agent can run at any time provides an unambiguous measure of progress and correctness.  
* **Implement Human-in-the-Loop (HIL) Gates:** For irreversible or high-impact decisions, the workflow must include explicit HIL checkpoints. The agent should be required to pause and request human approval before making changes to a public API contract, modifying the database schema, or merging code into the main branch. LangGraph and other frameworks provide built-in support for these crucial oversight mechanisms.22

### **2.4 Tier 4: Strategic Reasoning (Autonomous Collaboration & Goal-Oriented Planning)**

#### **Definition and Task Examples**

Strategic reasoning tasks represent the current frontier of AI in software engineering. These tasks are so large, complex, or multifaceted that they exceed the capabilities of any single agent. Their successful completion requires a team of specialized AI agents that can collaborate, decompose the problem, delegate sub-tasks, and synthesize their individual contributions into a coherent whole. This process mirrors the workflow of a human software development team and requires a sophisticated orchestration layer that manages the agents' interactions. The reasoning involved is collaborative (managing communication and shared goals) and recursive (breaking a problem down into smaller versions of itself).

Examples of Strategic tasks include:

* **End-to-end feature development:** "Implement a 'real-time document collaboration' feature, including the frontend UI components, backend WebSocket logic, and database updates."  
* **Large-scale codebase migration:** "Migrate our entire 500,000-line Python 2 codebase to Python 3, ensuring all 5,000 unit and integration tests pass after the migration."  
* **Automated security vulnerability remediation:** "A critical remote code execution vulnerability has been discovered in our logging library. Find all affected repositories in our organization, develop a patch, test it against each repository's test suite, and open a pull request with the fix."  
* **Building a simple application from scratch:** "Create a complete weather application with a React frontend and a Node.js backend that calls a public weather API."

#### **Preferred AI Models and Tools**

This tier is exclusively the domain of **Multi-Agent Systems (MAS)** and the orchestration frameworks designed to manage them. These frameworks provide the structure for defining agent roles, facilitating communication, and managing the overall workflow.

Leading frameworks include:

* **CrewAI:** This framework is ideal for establishing clear, role-based collaboration. A developer can define specialized agents like a "Product Manager Agent" to clarify requirements, an "Architect Agent" to design the system, "Frontend" and "Backend Agents" to write the code, and a "QA Agent" to write and run tests. CrewAI manages the handoff of tasks between these agents in a structured process.21  
* **Microsoft AutoGen:** AutoGen is a powerful and highly customizable framework for creating complex, conversational workflows between multiple agents. It is particularly well-suited for building robust, enterprise-grade automation systems where agents may need to engage in extended, event-driven interactions.9  
* **Specialized Research Frameworks:** Academic and research-led projects have demonstrated highly effective multi-agent patterns. **AgentCoder**, for example, proposes a team of three agents: a "Programmer," a "Test Designer," and a "Test Executor," which creates a robust cycle of generation and validation.26  
  **MapCoder** implements a four-agent pipeline that mimics the human development process: "Retrieval" (finding similar past problems), "Planning," "Coding," and "Debugging".28 These demonstrate the power of functional specialization in a multi-agent context.

#### **Failure Modes if Misrouted**

The primary failure mode for Strategic-level systems is not under-powering, but over-application. Multi-agent systems are extremely powerful but also incredibly resource-intensive. They can consume a vast number of tokens as the lead agent plans, the sub-agents execute, and they communicate back and forth.30 Using a multi-agent system to fix a simple typo (a Shallow task) is computationally and financially wasteful.

Furthermore, even when applied to an appropriately complex task, these systems can fail if the orchestration is poor. If the lead agent does not decompose the task effectively, sub-agents may duplicate work, perform redundant searches, or create components that have conflicting interfaces. Without clear boundaries and objectives, the "team" can descend into chaos, failing to integrate their work and leaving critical gaps in the final solution.30

#### **Suggested Intermediate Steps for Success**

The human's role at this tier elevates to that of a "Project Manager" or "Team Lead." Their focus is on high-level strategy, process, and oversight, rather than on the code itself.

* **"Teach the Orchestrator" via Prompt Engineering:** The initial prompt given to the lead or orchestrator agent is the single most critical factor for success. This prompt must be meticulously engineered to teach the agent how to be an effective manager. It should include explicit instructions on how to decompose complex tasks, how to define clear roles and responsibilities for sub-agents, what output formats to expect, and the specific boundaries of each sub-task.30  
* **Scale Effort to Complexity:** To manage costs and prevent over-engineering, the orchestrator's prompt should include rules for resource allocation. For example, it can be instructed that simple fact-finding tasks should only spawn one sub-agent, while complex feature development can spawn a full team. This helps the system allocate resources efficiently.30  
* **Human as "Project Manager" and Reviewer:** The developer monitors the multi-agent system's progress, often through a shared planning document or a dedicated tracing tool like LangSmith.17 Their role is to intervene only when the team gets stuck, resolves deadlocks between agents, or makes a strategic decision that deviates from the project's goals. They are the final backstop for quality and direction.

The progression through these four tiers reveals a fundamental transformation in the nature of software development work. At the Shallow level, the developer is a direct creator of code, merely augmented by AI. By the Procedural level, their role shifts to that of a curator, responsible for validating and integrating discrete, AI-generated components. At the Architectural level, the developer becomes a conductor, orchestrating a single, powerful AI agent to execute a pre-approved plan. Finally, at the Strategic level, the developer is a manager, overseeing a team of autonomous AI agents and guiding them toward a high-level objective. This trajectory indicates that the integration of AI into the SDLC is not a simple act of replacement but a profound reshaping of the developer's role. The most valuable human skills are rapidly shifting away from the rote mechanics of writing code and toward the higher-order cognitive tasks of problem decomposition, critical thinking, systems architecture, and strategic oversight.1 Consequently, organizations must recognize that traditional productivity metrics, such as lines of code written, are becoming obsolete and even counterproductive. Such metrics would incentivize the generation of voluminous, low-quality AI code, directly contributing to the high code churn and technical debt that effective AI strategies aim to prevent.3 The future requires new KPIs focused on solution quality, system reliability, and the overall efficiency of the human-AI collaborative unit.

This evolution also highlights the growing importance of the underlying agentic frameworks. The tools required for Architectural and Strategic tasks—such as LangChain, CrewAI, and AutoGen—provide more than just model access. They offer a suite of foundational services: memory management for maintaining context, tool integration for interacting with the outside world, state persistence for long-running tasks, and standardized protocols for inter-agent communication.21 These are the same core services that a traditional computer operating system provides for software applications. It is therefore useful to view these agentic frameworks not merely as libraries, but as the emerging

*de facto* operating systems for building the next generation of intelligent software. The choice of which framework to adopt is a long-term strategic decision, analogous to the historic choice between Windows, macOS, or Linux. This decision will shape an organization's entire development ecosystem, determining the availability of pre-built tools and agents, the skill sets their developers must cultivate, and their ability to interoperate with other systems. As this ecosystem matures, standards for interoperability, such as those proposed by FIPA, will become increasingly critical for avoiding vendor lock-in and enabling seamless communication across different agentic platforms.22

---

## **Section 3: An Operational Guide to Reasoning-to-Agent Routing: Implementation and Governance**

The theoretical framework of the reasoning taxonomy becomes actionable through the creation of an operational routing system. This system acts as an intelligent dispatcher, analyzing incoming development tasks and directing them to the appropriate AI capability level. This section provides a technical blueprint for designing, implementing, and governing such a system.

### **3.1 The Task Classification Engine: Using an LLM-as-a-Judge**

The first component of the routing system is a classification engine responsible for analyzing a developer's request and assigning it to one of the four reasoning tiers. While traditional machine learning classifiers like decision trees or SVMs could be used, LLMs themselves have proven to be exceptionally powerful and flexible classifiers, capable of understanding the nuance and context of natural language requests with minimal feature engineering.31 This "LLM-as-a-Judge" approach is ideal for this use case.32

The implementation of this classifier follows a clear, multi-step process:

1. **Prompt Ingestion:** The system captures the developer's request, which is typically a natural language prompt (e.g., "Refactor the UserService to use the new caching library and add integration tests.").  
2. **Contextual Feature Extraction:** A powerful frontier model (e.g., GPT-4o, Claude 3 Opus) is used to analyze the prompt. This is not a simple keyword search. The classifier LLM is given a specific meta-prompt that instructs it to act as an expert software engineering manager and extract key features from the request, including:  
   * **Action Verbs:** Identifying keywords that suggest complexity (e.g., "fix," "add," "complete" suggest lower complexity, while "design," "refactor," "architect," "migrate" suggest higher complexity).  
   * **Scope Identifiers:** Determining the scope of the request by looking for terms like "variable," "function," "file," "class," "service," "module," or "application."  
   * **Dependency Analysis:** Assessing whether the task is self-contained or requires knowledge of other parts of the codebase. Phrases like "across the system," "integrate with," or mentions of multiple component names are strong indicators of higher complexity.  
   * **Complexity Estimation:** Directly asking the classifier model to estimate the "human-completion time horizon" for the task, leveraging the quantifiable metric discussed in Section 1\. This provides a numerical anchor for the classification.  
3. **RAG for Improved Accuracy:** To ensure consistency and improve accuracy over time, the classifier's prompt should be augmented using Retrieval-Augmented Generation (RAG). The system should maintain a knowledge base of previously classified tasks and their outcomes. When a new request comes in, the system can retrieve a few examples of similar, successfully classified tasks and include them in the prompt as a few-shot learning guide.20  
4. **Enforced Structured Output:** To ensure the classifier's output can be reliably used by downstream automation, the model must be forced to respond in a structured format, such as JSON. The meta-prompt should explicitly require an output like: {"reasoning\_tier": "Architectural", "confidence\_score": 0.92, "estimated\_human\_hours": 3.5, "required\_tools": \["file\_system\_read", "run\_tests"\]}. This structured output eliminates the need for complex parsing and makes the integration with the routing logic seamless and robust.31

### **3.2 The AI Task Routing Matrix**

The core logic of the routing system is encapsulated in the AI Task Routing Matrix. This matrix serves as a comprehensive, single-page reference guide that operationalizes all the analysis from the preceding sections. It is a playbook for both human developers and the automated routing engine, connecting task types to the appropriate tools, metrics, and escalation paths.

### **Table 2: AI Coding Task Routing Matrix**

| Reasoning Tier | Task Examples | Key Indicators (for Classifier) | Recommended Agent/Framework | Primary Success Metric (Quantitative) | Primary Quality Metric | Default Escalation Path |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Shallow** | Autocomplete, fix typo, rename local variable, generate getter/setter. | Keywords: "complete", "fix". Scope: single line, variable. Dependencies: none. Horizon: \< 5 min. | IDE Plugin (e.g., GitHub Copilot, CodeWhisperer) | Code compiles without errors. | Low Code Churn (\<15%). Static analysis passes. | On failure, flag for human review (no auto-escalation). |
| **Procedural** | Write function from docstring, generate unit tests, implement sorting algorithm, translate function. | Keywords: "create function", "implement", "add tests". Scope: single file/function. Horizon: 5 min \- 2 hr. | Single Model API (e.g., GPT-4, Claude 3\) \+ RAG & CoT Prompting | All provided unit tests pass (\>95% pass rate). | Cyclomatic Complexity below threshold. Adheres to style guide. | Failure \-\> Escalate to Architectural Agent with failure logs. |
| **Architectural** | Refactor module, design new API, resolve multi-component bug, plan new feature. | Keywords: "design", "refactor", "architect". Scope: \>1 file/module. Dependencies: explicit cross-component. Horizon: 2 hr \- 1 day. | Single Agent Framework (e.g., LangGraph, Semantic Kernel) with tool use. | All integration tests pass. | Security scan passes. Human architect approves plan/PR. | Failure \-\> Escalate to Multi-Agent System with full context. |
| **Strategic** | End-to-end feature dev, large-scale migration, build simple app from scratch. | Keywords: "build", "migrate", "create app". Scope: entire system/repo. Ambiguous goal. Horizon: \> 1 day. | Multi-Agent Framework (e.g., CrewAI, AutoGen) | End-to-end user acceptance test (UAT) passes. | Human project manager approves final deliverable. | Failure \-\> Decompose problem further and re-assign to a new agent team or escalate to human team. |

### **3.3 Implementation: Thresholds, Escalation, and Feedback Loops**

With the classifier and the logic matrix in place, the final step is to define the specific rules that govern the automated routing engine's behavior.

#### **Thresholds**

Thresholds are the quantitative rules that trigger specific routing decisions:

* **Confidence Score Threshold:** The LLM classifier must return a confidence score of greater than 90% for a classification to be routed fully automatically. If the confidence is between 70% and 90%, the system can proceed but should flag the task for passive human review. Below 70%, the task should be held in a queue for mandatory human classification.  
* **Complexity Score Thresholds:** The estimated "human-completion time horizon" is a primary input for routing, using the boundaries defined in the taxonomy: \<5min \-\> Shallow; \<2hr \-\> Procedural; \<1day \-\> Architectural; \>1day \-\> Strategic.  
* **File Scope Threshold:** As a simple but effective heuristic, any task request that explicitly mentions or is determined to affect more than five files is automatically classified as at least an Architectural-level task, regardless of other indicators.

#### **Escalation Rules**

Escalation rules define how the system handles failure, creating a resilient workflow that can recover from errors.

* **Rule 1 (Automated Retry & Escalation):** If a task fails its Primary Success Metric at a given tier (e.g., a Procedural agent generates code that fails its unit tests), the system should first attempt one automated retry by feeding the failure logs back to the same agent. If it fails a second time, the system must automatically package the original prompt, the full conversation history, and the final failure logs, and escalate the entire context to the next-highest reasoning tier.  
* **Rule 2 (Quality-Based Re-evaluation):** The system should integrate with the organization's version control system to monitor metrics like code churn.3 If a piece of code generated by an AI agent is associated with a high churn rate in the weeks following its submission, the system should flag the original task's classification as potentially inaccurate. This data is used to refine the classifier over time.  
* **Rule 3 (Manual Override and Logging):** A developer must always have the ability to manually override the classifier's decision and select a different agent tier. However, every override must be logged, and the developer should be prompted to provide a brief reason. This provides a valuable data stream for identifying weaknesses in the automated classification logic.

#### **Feedback Loops**

A static routing system will quickly become obsolete. The system must be designed to learn and evolve.

* **Continuous Data Collection:** The outcomes of all AI-assisted tasks—pass/fail rates, number of retries, final code quality metrics, code churn, and human satisfaction scores—must be systematically collected and stored.  
* **Periodic Fine-Tuning:** This collected data forms a "golden dataset" that can be used to periodically fine-tune the classifier LLM. This process, which mirrors Reinforcement Learning from Human Feedback (RLHF), allows the classifier to become progressively more accurate and aligned with the organization's specific needs and coding patterns.33  
* **Dynamic Threshold Adjustment:** The thresholds themselves must not be static. As the underlying foundation models become more capable, the "human-completion time horizon" for what constitutes a Procedural vs. an Architectural task will shrink.13 The governance team responsible for the routing system should review and adjust these thresholds on a regular basis (e.g., quarterly) to ensure the system continues to route tasks to the most efficient and capable level.

This routing system should not be viewed merely as a dispatcher for improving developer velocity. Its most critical function is that of a proactive quality and cost management gate. The significant risks associated with AI in software development—such as the accumulation of technical debt and the high cost of running powerful models—stem directly from the misapplication of tools to tasks they are not suited for.3 By forcing a structured, automated evaluation of every task's complexity

*before* any code is generated, the router acts as a crucial risk mitigation layer. It prevents developers from naively using a simple autocomplete for complex logic and prevents the wasteful application of an expensive multi-agent system to a simple bug fix. The small computational cost of running the classifier LLM is therefore not overhead; it is a strategic investment to prevent the exponentially larger downstream costs of debugging, refactoring, and maintaining low-quality, AI-generated code. This operationalizes the strategic advice to "start smart" and adopt a "gradual, holistic approach" to AI implementation.1

Furthermore, the long-term evolution of this system provides a powerful strategic advantage. The measurable, exponential improvement in the AI's task-completion time horizon is a clear trend line pointing toward increasingly autonomous systems.12 Today, the boundary between a Procedural and an Architectural task might be a task that takes a human two hours. In two years, that same two-hour task may become routine for a Procedural-level agent. The ultimate trajectory of this trend points toward a future where a Strategic-level multi-agent team can autonomously handle a project that would currently take a human team weeks or even months to complete. By implementing this routing framework, an organization is not just creating an operational tool; it is building a living benchmark that provides a real-time, quantifiable measure of progress toward this future state. This data-driven understanding of the AI capability curve will allow leadership to anticipate disruptions, plan for the evolution of developer roles, and know precisely when and how to deploy new, more powerful AI systems to maintain a significant competitive advantage.14

## **Conclusion and Future Outlook**

The framework presented in this report—encompassing a four-tier reasoning taxonomy and an operational routing guide—offers a strategic pathway for navigating the complexities of AI in software engineering. It advocates for a fundamental shift away from the current state of chaotic, ad-hoc adoption of AI tools toward a structured, managed, and scalable ecosystem. By classifying coding tasks based on their intrinsic reasoning requirements, organizations can deploy the right level of AI capability for each job, maximizing productivity while proactively mitigating the risks of poor quality and escalating technical debt.

This reasoning-centric approach has profound implications for the software development workforce. The analysis clearly shows that the developer's role is evolving from that of a direct creator of code to a high-level curator, conductor, and manager of AI systems. The most critical skills for the future will be those of problem decomposition, architectural design, critical evaluation of AI-generated outputs, and strategic oversight of autonomous agent teams. Acknowledging this shift is paramount; organizations must invest in retraining their engineering talent and fundamentally rethink performance metrics to align with this new paradigm, moving away from "lines of code" and toward measures of solution quality and system reliability.

Looking forward, the trajectory of AI capabilities in software engineering is clear and steep. The exponential improvement in the length and complexity of tasks that AI can reliably automate suggests that the boundaries between the reasoning tiers will continue to blur and shift upwards.13 Tasks that are considered "Architectural" today may well become "Procedural" for the frontier models of tomorrow. The framework detailed in this report is designed to be adaptive, with dynamic thresholds and feedback loops that allow it to co-evolve with the technology.

The ultimate vision is one of a deeply integrated human-AI partnership, where developers set strategic goals and provide high-level oversight, while teams of autonomous agents handle the vast majority of the implementation, testing, and even deployment. While the prospect of fully autonomous development for certain classes of projects is on the horizon, the role of human judgment, creativity, and strategic direction will remain indispensable. The most successful organizations will be those that embrace this collaborative future.

The recommended path forward is a phased implementation of the routing guide. Organizations should begin by implementing the classification engine to gather data and provide advisory guidance to developers. The next phase involves enabling the automated routing and escalation rules in a controlled environment. By starting with a focus on classification and monitoring before moving to full automation, technology leaders can build a robust, intelligent, and quality-driven SDLC that not only harnesses the power of AI today but is also prepared for the transformative capabilities of tomorrow.

#### **Works cited**

1. Reducing software development complexity with AI \- GitLab, accessed June 14, 2025, [https://about.gitlab.com/the-source/ai/reducing-software-development-complexity-with-ai/](https://about.gitlab.com/the-source/ai/reducing-software-development-complexity-with-ai/)  
2. Breaking Down Complexity: AI's Role in Simplifying Software Development \- @VMblog, accessed June 14, 2025, [https://vmblog.com/archive/2024/12/12/breaking-down-complexity-ai-s-role-in-simplifying-software-development.aspx](https://vmblog.com/archive/2024/12/12/breaking-down-complexity-ai-s-role-in-simplifying-software-development.aspx)  
3. AI in Software Development: Productivity at the Cost of Code Quality? \- DevOps.com, accessed June 14, 2025, [https://devops.com/ai-in-software-development-productivity-at-the-cost-of-code-quality/](https://devops.com/ai-in-software-development-productivity-at-the-cost-of-code-quality/)  
4. Code to Think, Think to Code: A Survey on Code-Enhanced Reasoning and Reasoning-Driven Code Intelligence in LLMs \- arXiv, accessed June 14, 2025, [https://arxiv.org/html/2502.19411v1](https://arxiv.org/html/2502.19411v1)  
5. What Is Reasoning in AI? \- IBM, accessed June 14, 2025, [https://www.ibm.com/think/topics/ai-reasoning](https://www.ibm.com/think/topics/ai-reasoning)  
6. Assessing Code Reasoning in Large Language Models: A Literature Review of Benchmarks and Future Directions \- Preprints.org, accessed June 14, 2025, [https://www.preprints.org/manuscript/202411.1147/v1](https://www.preprints.org/manuscript/202411.1147/v1)  
7. Evaluating Causal Reasoning Capabilities of Large Language Models: A Systematic Analysis Across Three Scenarios \- MDPI, accessed June 14, 2025, [https://www.mdpi.com/2079-9292/13/23/4584](https://www.mdpi.com/2079-9292/13/23/4584)  
8. www.ibm.com, accessed June 14, 2025, [https://www.ibm.com/think/insights/top-ai-agent-frameworks\#:\~:text=Agentic%20frameworks%20are%20the%20building,and%20capabilities%20of%20agentic%20AI.](https://www.ibm.com/think/insights/top-ai-agent-frameworks#:~:text=Agentic%20frameworks%20are%20the%20building,and%20capabilities%20of%20agentic%20AI.)  
9. Top Agentic AI Frameworks You Need in 2025 \- TestingXperts, accessed June 14, 2025, [https://www.testingxperts.com/blog/top-agentic-ai-frameworks/](https://www.testingxperts.com/blog/top-agentic-ai-frameworks/)  
10. The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity \- Apple Machine Learning Research, accessed June 14, 2025, [https://machinelearning.apple.com/research/illusion-of-thinking](https://machinelearning.apple.com/research/illusion-of-thinking)  
11. Evaluating the thinking process of reasoning LLMs : r/datascience \- Reddit, accessed June 14, 2025, [https://www.reddit.com/r/datascience/comments/1imkowl/evaluating\_the\_thinking\_process\_of\_reasoning\_llms/](https://www.reddit.com/r/datascience/comments/1imkowl/evaluating_the_thinking_process_of_reasoning_llms/)  
12. Measuring AI Ability to Complete Long Tasks \- arXiv, accessed June 14, 2025, [https://arxiv.org/html/2503.14499v1](https://arxiv.org/html/2503.14499v1)  
13. Measuring AI Ability to Complete Long Tasks \- METR, accessed June 14, 2025, [https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)  
14. Anthropic Economic Index: AI's impact on software development, accessed June 14, 2025, [https://www.anthropic.com/research/impact-software-development](https://www.anthropic.com/research/impact-software-development)  
15. Code LLMs: A Taxonomy-based Survey \- arXiv, accessed June 14, 2025, [https://arxiv.org/html/2412.08291v1](https://arxiv.org/html/2412.08291v1)  
16. Guide to Large Language Models \- Scale AI, accessed June 14, 2025, [https://scale.com/guides/large-language-models](https://scale.com/guides/large-language-models)  
17. How I Built a Multi-Agent Orchestration System with Claude Code Complete Guide (from a nontechnical person don't mind me) \- Reddit, accessed June 14, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how\_i\_built\_a\_multiagent\_orchestration\_system/](https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how_i_built_a_multiagent_orchestration_system/)  
18. LLM Reasoning \- Prompt Engineering Guide, accessed June 14, 2025, [https://www.promptingguide.ai/research/llm-reasoning](https://www.promptingguide.ai/research/llm-reasoning)  
19. \[2401.09074\] Code Simulation Challenges for Large Language Models \- arXiv, accessed June 14, 2025, [https://arxiv.org/abs/2401.09074](https://arxiv.org/abs/2401.09074)  
20. ClassifAI – Exploring the use of Large Language Models (LLMs) to assign free text to commonly used classifications | Data Science Campus, accessed June 14, 2025, [https://datasciencecampus.ons.gov.uk/classifai-exploring-the-use-of-large-language-models-llms-to-assign-free-text-to-commonly-used-classifications/](https://datasciencecampus.ons.gov.uk/classifai-exploring-the-use-of-large-language-models-llms-to-assign-free-text-to-commonly-used-classifications/)  
21. Top 7 Free AI Agent Frameworks \- Botpress, accessed June 14, 2025, [https://botpress.com/blog/ai-agent-frameworks](https://botpress.com/blog/ai-agent-frameworks)  
22. Agentic Frameworks: A Guide to the Systems Used to Build AI Agents \- Moveworks, accessed June 14, 2025, [https://www.moveworks.com/us/en/resources/blog/what-is-agentic-framework](https://www.moveworks.com/us/en/resources/blog/what-is-agentic-framework)  
23. AI Agent Frameworks: Choosing the Right Foundation for Your Business | IBM, accessed June 14, 2025, [https://www.ibm.com/think/insights/top-ai-agent-frameworks](https://www.ibm.com/think/insights/top-ai-agent-frameworks)  
24. Top 5 Agentic AI Frameworks You Should Know in 2025 \- Hyperstack, accessed June 14, 2025, [https://www.hyperstack.cloud/blog/case-study/top-agentic-ai-frameworks-you-should-know](https://www.hyperstack.cloud/blog/case-study/top-agentic-ai-frameworks-you-should-know)  
25. Agentic AI Frameworks in 2025 | Plivo Guide, accessed June 14, 2025, [https://www.plivo.com/blog/agentic-ai-frameworks/](https://www.plivo.com/blog/agentic-ai-frameworks/)  
26. AgentCoder: Multiagent-Code Generation with Iterative Testing and Optimisation \- arXiv, accessed June 14, 2025, [https://arxiv.org/html/2312.13010v2](https://arxiv.org/html/2312.13010v2)  
27. AgentCoder: Multi-Agent Code Generation with Effective Testing and Self-optimisation, accessed June 14, 2025, [https://arxiv.org/html/2312.13010v3](https://arxiv.org/html/2312.13010v3)  
28. MapCoder: Multi-Agent Code Generation for Competitive Problem Solving \- GitHub, accessed June 14, 2025, [https://github.com/Md-Ashraful-Pramanik/MapCoder](https://github.com/Md-Ashraful-Pramanik/MapCoder)  
29. MapCoder: Multi-Agent Code Generation for Competitive Problem Solving \- ACL Anthology, accessed June 14, 2025, [https://aclanthology.org/2024.acl-long.269.pdf](https://aclanthology.org/2024.acl-long.269.pdf)  
30. How we built our multi-agent research system \- Anthropic, accessed June 14, 2025, [https://www.anthropic.com/engineering/built-multi-agent-research-system](https://www.anthropic.com/engineering/built-multi-agent-research-system)  
31. LLMs are machine learning classifiers \- Wandb, accessed June 14, 2025, [https://wandb.ai/gladiator/LLMs-as-classifiers/reports/LLMs-are-machine-learning-classifiers--VmlldzoxMTEwNzUyNA](https://wandb.ai/gladiator/LLMs-as-classifiers/reports/LLMs-are-machine-learning-classifiers--VmlldzoxMTEwNzUyNA)  
32. LLM Evaluation Metrics: The Ultimate LLM Evaluation Guide \- Confident AI, accessed June 14, 2025, [https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation)  
33. Large language model \- Wikipedia, accessed June 14, 2025, [https://en.wikipedia.org/wiki/Large\_language\_model](https://en.wikipedia.org/wiki/Large_language_model)
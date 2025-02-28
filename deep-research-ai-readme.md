# Deep Research AI

An AI-powered research system that combines web search capabilities with large language models (LLMs) to produce high-quality, evidence-based answers. The implementation follows an agentic architecture with four specialized components working in sequence, orchestrated through LangGraph's state graph.

## Architecture Diagram
[Research Agent] → [Answer Drafting] → [Review Agent] → [Refinement Agent]

## Key Components

### 1. Research Agent
**Responsibility**: Web research using Tavily Search API  
**Implementation**:
- Takes user query as input
- Performs web search using TavilySearchResults
- Returns structured search results
- Error handling for API failures

### 2. Answer Drafting Agent
**Responsibility**: Initial answer generation  
**Features**:
- Uses Groq's Mixtral-8x7b model (32k context)
- Structured prompt with formatting requirements
- Evidence-based response generation

**Prompt Structure**:
- Clear and concise
- Well-organized with headings
- Evidence-supported
- Accessible language

### 3. Review Agent
**Responsibility**: Quality assurance  
**Evaluation Criteria**:
- Clarity/Coherence
- Information accuracy
- Logical flow
- Readability

### 4. Refinement Agent
**Responsibility**: Final improvement  
**Process**:
- Incorporates review feedback
- Makes targeted improvements
- Maintains original evidence base
- Final quality check

## Workflow Management

### LangGraph Configuration
```python
workflow = StateGraph(dict)
workflow.add_node("research", research_agent)
workflow.add_node("draft_answer", answer_drafting_agent)
workflow.add_node("review_answer", review_agent)
workflow.add_node("refine_answer", refinement_agent)

workflow.set_entry_point("research")
workflow.add_edge("research", "draft_answer")
workflow.add_edge("draft_answer", "review_answer")
workflow.add_edge("review_answer", "refine_answer")
```

### Execution Flow
- Asynchronous invocation pattern
- State passing between nodes
- Error propagation handling
- Final output compilation

## Technical Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| Search | Tavily API | Web research aggregation |
| LLM | Groq/Mixtral-8x7b | High-speed inference |
| Orchestration | LangGraph | Stateful workflow management |
| Async Processing | Python asyncio | Concurrent API operations |
| Environment | python-dotenv | Secure credential management |

## Error Handling Strategy
- Per-agent try/catch blocks
- Error state propagation
- Graceful degradation:
  - Empty research handling
  - Failed review fallthrough
  - Draft preservation on refinement failure

## Usage Example
```python
async def main():
    query = "What are the impacts of AI on the world"
    output = await research_system.ainvoke({"query": query})  
    print("\n=== Final Answer ===\n", output["final_answer"])
```

## Performance Considerations
- Asynchronous threading for API calls
- Groq's LPU inference engine optimization
- Tavily's pre-processed search results
- LangGraph's efficient state management

## Customization Points
### Prompt Engineering: Modify agent prompts in:
```python
# In each agent:
prompt = f"""Custom template..."""
```

### Model Selection: Change Groq model:
```python
model="llama2-70b-4096"  # Alternative model
```

### Workflow Modifications: Add nodes/edges:
```python
workflow.add_node("new_agent", custom_agent)
workflow.add_edge("review_answer", "new_agent")
```

## Setup Requirements
### Environment variables (.env):
```
TAVILY_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
```

### Python dependencies:
```bash
pip install tavily-python langchain groq langgraph python-dotenv
```

## Limitations & Future Improvements
### Current Limitations:
- Linear workflow without branching
- Single search engine dependency
- Basic error recovery mechanisms

### Planned Enhancements:
- Multi-search engine aggregation
- Parallel research threads
- Human-in-the-loop review
- Automated quality scoring
- Feedback iteration loops

This implementation demonstrates a robust research pipeline combining current AI capabilities with systematic quality control mechanisms. The agentic architecture allows for targeted improvements while maintaining operational stability through error-resistant design.

## Example Use
input query :: What are the impacts of AI on the world

output :: Research Data start
---------------------------------------------------
Research Results: [{'url': 'https://www.gate39media.com/the-global-impact-of-artificial-intelligence/', 'content': 'The rapid advancement of AI systems presents a significant risk of economic disruption and job displacement across industries. It is paramount'}, {'url': 'https://www.3dbear.io/blog/the-impact-of-ai-how-artificial-intelligence-is-transforming-society', 'content': 'AI-powered technologies are also being used to improve the user experience and to offer more personalized recommendations and services. AI has the potential to revolutionize education, offering personalized and individualized teaching, and improved learning outcomes. AI-powered technologies can provide students with real-time feedback, help them to stay on track with their studies, and offer a more personalized and engaging learning experience. AI has the potential to bring about numerous positive changes in society, including enhanced productivity, improved healthcare, and increased access to education. From revolutionizing the healthcare industry to providing personalized learning experiences, AI has the potential to improve our lives in countless ways. By doing so, we can ensure that AI continues to play a positive role in our world, improving our lives and creating a better future for generations to come.'}, {'url': 'https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity', 'content': 'In a new analysis, IMF staff examine the potential impact of AI on the global labor market. In advanced economies, about 60 percent of jobs may be impacted by AI. To help countries craft the right policies, the IMF has developed an AI Preparedness Index that measures readiness in areas such as digital infrastructure, human-capital and labor-market policies, innovation and economic integration, and regulation and ethics. The findings reveal that wealthier economies, including advanced and some emerging market economies, tend to be better equipped for AI adoption than low-income countries, though there is considerable variation across countries. June 25, 2024New AI Preparedness Index Dashboard tracks 174 economies based on their digital infrastructure, human capital, labor policies, innovation, integration and regulation'}, {'url': 'https://www.brookings.edu/articles/how-artificial-intelligence-is-transforming-the-world/', 'content': 'In China, for example, companies already have “considerable resources and access to voices, faces and other biometric data in vast quantities, which would help them develop their technologies.”26 New technologies make it possible to match images and voices with other types of information, and to use AI on these combined data sets to improve law enforcement and national security. Opening access to that data will help us get insights that will transform the U.S. economy.”53 Through its Data.gov portal, the federal government already has put over 230,000 data sets into the public domain, and this has propelled innovation and aided improvements in AI and data analytic technologies.54 The private sector also needs to facilitate research data access so that society can achieve the full benefits of artificial intelligence.'}, {'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7605294/', 'content': 'Facing this challenge, new principles of AI bioethics must be considered and developed to provide guidelines for the AI technology to observe so that the world will be benefited by the progress of this new intelligence. Artificial intelligence (AI) has many different definitions; some see it as the created technology that allows computers and machines to function intelligently. The new development of the long-term goal of many researchers is to create strong AI or artificial general intelligence (AGI) which is the speculative intelligence of a machine that has the capacity to understand or learn any intelligent task human being can, thus assisting human to unravel the confronted problem.'}]
---------------------------------------------------
Research Data end

=== Final Answer ===
 Artificial Intelligence (AI) is rapidly evolving and has the potential to significantly impact various aspects of society and the economy. Here are some key takeaways from recent research:

Economic Disruption and Job Displacement
----------------------------------------

* **Risk of economic disruption:** AI could cause substantial economic disruption and job displacement across industries, as reported by Gate39Media. It is crucial to address this risk to mitigate its negative impact.
* **Global labor market impact:** The International Monetary Fund (IMF) estimates that about 60% of jobs in advanced economies could be affected by AI (<https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity>).

AI Preparedness Index
--------------------

* **Variation in AI readiness:** IMF's AI Preparedness Index indicates that wealthier economies, both advanced and emerging market economies, are generally better prepared for AI adoption than low-income countries. However, there is considerable variation across countries (<https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity>).
* **AI Preparedness Index Dashboard:** The IMF has developed an AI Preparedness Index Dashboard that tracks 174 economies based on their digital infrastructure, human capital, labor policies, innovation, integration, and regulation (<https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity>).

AI-Powered Technologies in Society
--------------------------------

* **Improved user experiences:** AI-powered technologies are being utilized to enhance user experiences and offer personalized recommendations and services (<https://www.3dbear.io/blog/the-impact-of-ai-how-artificial-intelligence-is-transforming-society>).    
* **Transforming education:** AI has the potential to revolutionize education by providing personalized and individualized teaching, improved learning outcomes, real-time feedback, and a more engaging learning experience (<https://www.3dbear.io/blog/the-impact-of-ai-how-artificial-intelligence-is-transforming-society>).
* **Positive societal changes:** AI could bring about numerous positive changes in society, including enhanced productivity, improved healthcare, and increased access to education (<https://www.3dbear.io/blog/the-impact-of-ai-how-artificial-intelligence-is-transforming-society>).

Facilitating Research Data Access
--------------------------------

* **Sharing data for innovation:** Providing access to data will help the U.S. economy transform by offering insights that can aid improvements in AI and data analytic technologies (<https://www.brookings.edu/articles/how-artificial-intelligence-is-transforming-the-world/>).
* **Principles of AI bioethics:** New principles of AI bioethics should be established to provide guidelines for AI technology so that the world benefits from its progress (<https://pmc.ncbi.nlm.nih.gov/articles/PMC7605294/>).

In summary, AI has the potential to transform society and the economy. Addressing the risks of economic disruption and job displacement is crucial. Preparedness indices can help countries assess their readiness for AI adoption, while opening access to data can facilitate innovation. Establishing new principles of AI bioethics is also essential to ensure that the world benefits from the advancements in AI technology. It is important to stay informed about the latest research and developments in AI to understand its impact and ensure its benefits are harnessed responsibly.


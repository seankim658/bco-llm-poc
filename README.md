# BCO LLM Proof of Concept

- [Approach Justification and Background](#approach-justification-and-background)
- [Contraints](#contraints)
- [Tech Stack](#tech-stack)
    - [LlamaIndex](#llamaindex)
- [Workflow](#workflow)

---

## Approach Justification and Background 

The Biocompute Object (BCO) LLM will assist users in automatically creating specific BCO domains from papers. This proof of concept uses a **retrieval augmented generatation** (RAG) approach rather than a standalone LLM or fine tuned LLM approach. A traditional standalone LLM suffers from multiple drawbacks in this problem context. Recent studies ([Lost in the Middle](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf)) have shown that LLM's struggle with long contexts:

> ... performance can degrade significantly when
> changing the position of relevant information, indicating that current language models
> do not robustly make use of information in long input contexts. 

LLMs also are known to extrapolate when the facts aren't available, resulting in confident, but false output. These two issues are especially present with our specific goal: uploading potentially multi-page papers to be ingested by the LLM, and then asking for the LLM to extract specific information relating to the purpose and schema of a specific BCO domain. 

Retrieval augmented generation can help to address both of these issues. By allowing us to intelligently chunk embed the PDF information, we can utilize intelligent retrieval to only obtain the relevant information the LLM needs for the specific domain. By sending more focused prompts, we hypothesize better performance and more specific responses.  

## Contraints

1. Users have to have a PDF of the paper they want to build a BCO for. 
    - Many websites, including PubMed Central, have specific settings to prevent automated systems and bots from scraping or reading from their website. 
2. Users will have to get each domain separately. 
    - This will allow for more focused responses, which is beneficial for a couple reasons. 
        - Some papers will not have direct mappings to the information required for the specifically requested domain. The more specific inquiries allow the LLM to provide more context to the user that the JSON provided might not be complete and/or that the user might have to manually edit or decide on whether the answer is acceptable or not. 
        - A per-domain approach is more engaging for the user, and they are more likely to check and make sure each step provides good data instead of the LLM returning a large JSON response (that is highly likely to have mistakes in schema compliance, content, etc.) that the user is more likely to skim or accept without parsing the entire thing. 
3. Even though a LLM is used as the core engine, the user cannot free text chat with the model. Because the domain of each problem is a constrained, specific problem, we can achieve more consistent results with standardized under the hood prompts to the LLM.
    - The user will interact with buttons that they can press for each domain generation. 

## Tech Stack 

### LlamaIndex

## Workflow 

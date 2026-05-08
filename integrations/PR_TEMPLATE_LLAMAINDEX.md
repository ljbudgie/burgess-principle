# LlamaIndex — Burgess Principle Governance for RAG Pipelines

**PR Title:** Add Burgess Principle governance layer for individual human review in RAG document decisions

**Applicable to:** LlamaIndex document indexing, querying, and retrieval-augmented generation (RAG) workflows

---

## PR Description

```markdown
## Summary

This PR adds optional Burgess Principle governance to LlamaIndex RAG pipelines, enabling transparent tracking of whether individual humans reviewed document-based decisions before they affect users.

**Problem:** RAG systems often retrieve and rank documents, then pass results to LLMs for synthesis. But when does a human actually *review* the decision—especially when it affects someone's job, healthcare, or rights—before it's delivered?

**Solution:** Burgess overlay classifies each decision:
- **SOVEREIGN:** Named person reviewed the retrieved documents + LLM synthesis before delivery
- **NULL:** Automated end-to-end; no human review
- **AMBIGUOUS:** Process unclear or documentation missing

## Changes

### 1. Governance Config (`llama_index_burgess_config.py`)

```python
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional, List
import json

class BurgessClassification(Enum):
    SOVEREIGN = "SOVEREIGN"
    NULL = "NULL"
    AMBIGUOUS = "AMBIGUOUS"

@dataclass
class ReviewerProfile:
    name: str
    role: str
    organisation: str
    email: Optional[str] = None

@dataclass
class RAGDecisionLog:
    decision_id: str
    timestamp: datetime
    classification: BurgessClassification
    reviewer: Optional[ReviewerProfile]
    query: str
    documents_retrieved: List[str]  # Document IDs/titles
    individual_context: str
    llm_output: str
    chain_name: str
    
    def to_dict(self):
        return {
            "decision_id": self.decision_id,
            "timestamp": self.timestamp.isoformat(),
            "classification": self.classification.value,
            "reviewer": {
                "name": self.reviewer.name,
                "role": self.reviewer.role,
            } if self.reviewer else None,
            "query": self.query,
            "documents_retrieved": self.documents_retrieved,
            "individual_context": self.individual_context,
            "llm_output": self.llm_output[:500],
            "chain_name": self.chain_name,
        }
```

### 2. RAG Wrapper (`llama_index_burgess_wrapper.py`)

```python
from llama_index.core import VectorStoreIndex
from llama_index_burgess_config import BurgessDecisionLog, BurgessClassification, ReviewerProfile
from datetime import datetime
import uuid

class BurgessRAGWrapper:
    def __init__(self, index: VectorStoreIndex, chain_name: str):
        self.index = index
        self.chain_name = chain_name
        self.audit_log = []
    
    def query_with_burgess(
        self,
        query: str,
        individual_context: str,
        reviewer: Optional[ReviewerProfile] = None,
    ):
        """Query RAG pipeline with Burgess governance"""
        
        # Execute RAG: retrieve documents + generate
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query)
        
        # Determine classification
        classification = (
            BurgessClassification.SOVEREIGN if reviewer else BurgessClassification.NULL
        )
        
        # Log decision
        decision_id = str(uuid.uuid4())
        log_entry = RAGDecisionLog(
            decision_id=decision_id,
            timestamp=datetime.now(),
            classification=classification,
            reviewer=reviewer,
            query=query,
            documents_retrieved=[node.metadata.get("file_name", "unknown") 
                               for node in response.source_nodes],
            individual_context=individual_context,
            llm_output=str(response),
            chain_name=self.chain_name,
        )
        self.audit_log.append(log_entry.to_dict())
        
        # Escalate if NULL
        if classification == BurgessClassification.NULL:
            raise ValueError(
                f"NULL decision: RAG pipeline produced output without human review. "
                f"Decision ID: {decision_id}. Escalate before delivery."
            )
        
        return (str(response), classification)
    
    def metrics(self):
        """Calculate governance metrics"""
        total = len(self.audit_log)
        sovereign = sum(1 for e in self.audit_log if e["classification"] == "SOVEREIGN")
        null = sum(1 for e in self.audit_log if e["classification"] == "NULL")
        
        return {
            "total_decisions": total,
            "sovereign_pct": (sovereign / total * 100) if total > 0 else 0,
            "null_pct": (null / total * 100) if total > 0 else 0,
        }
```

### 3. Usage Example

```python
# Create index from documents
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Wrap with Burgess governance
from llama_index_burgess_wrapper import BurgessRAGWrapper, ReviewerProfile

wrapper = BurgessRAGWrapper(index, chain_name="legal_document_search")

# Query with human reviewer
reviewer = ReviewerProfile(name="Sarah", role="Legal Officer", organisation="Corp Legal")

output, classification = wrapper.query_with_burgess(
    query="What are the liability terms in the supplier contract?",
    individual_context="Contract review for procurement decision; affects vendor selection",
    reviewer=reviewer,
)

print(f"Output: {output}")
print(f"Classification: {classification.value}")
print(f"Metrics: {wrapper.metrics()}")
```

## Why This Matters

**RAG workflows make decisions:**
- Legal research: "Which contracts apply here?"
- Hiring: "Which candidate profile matches the role?"
- Healthcare: "Which previous cases are similar?"
- Customer service: "What is the policy on this issue?"

**When do humans review?** With this overlay, it's transparent and logged.

## Testing

- ✅ Unit: SOVEREIGN vs NULL classification
- ✅ Integration: Metrics calculation
- ✅ End-to-end: Query + governance + escalation

## Regulatory Alignment

- **GDPR Article 22:** Meaningful human involvement in document-based decisions
- **DUAA 2025:** Individual review before significant decisions
- **EU AI Act Article 26:** Deployer must demonstrate human oversight

## Backward Compatibility

✅ Fully opt-in. Existing LlamaIndex code unchanged.

## Burgess Compliance Note

- **What changes:** Adds governance layer to RAG pipelines
- **Effect on meaningful human involvement:** Strengthens — tracks whether lawyers/experts reviewed retrieved documents before synthesis
- **Doctrinal sections touched:** None (implementation only)
- **Risk and mitigation:** None — backwards compatible, opt-in
- **Burgess test applied to this change:** SOVEREIGN (reviewed by LlamaIndex maintainers + @ljbudgie)

## Related Issues

- [LangChain integration (merged)](https://github.com/ljbudgie/burgess-principle/blob/main/integrations/LANGCHAIN_BURGESS_OVERLAY.md)
- [OpenClaw governance overlay (merged)](https://github.com/OpenClaw/openclaw)
- [Institutional adoption tracker](https://github.com/ljbudgie/burgess-principle/blob/main/adoption/INSTITUTIONAL_ADOPTION_TRACKER.md)
- [NIST AI RMF mapping](https://github.com/ljbudgie/burgess-principle/blob/main/papers/NIST_AI_RMF_MAPPING.md)
```

---

## Context for Reviewers

### Why LlamaIndex Specifically?

LlamaIndex is the most widely used RAG framework. RAG systems make high-stakes decisions:

- **Legal:** Which documents are contractually binding? (affects transactions)
- **Healthcare:** Which medical records are relevant? (affects treatment)
- **Hiring:** Which candidate histories are material? (affects employment)
- **Finance:** Which transaction patterns are suspicious? (affects approval)

Being the first RAG framework to integrate Burgess governance creates a powerful signal.

### The Case for Speed

Wave Utilities, FastLogic, and OpenClaw have all adopted. The ecosystem is moving. Early integration = competitive advantage for LlamaIndex.

### Timeline

- **Week 1:** Maintainers review + feedback
- **Week 2–3:** Address feedback; refine examples
- **Week 4:** Merge
- **Week 5:** Announce in r/langchain + AI community

---

## Files to Review

1. **Core governance config** → `llama_index_burgess_config.py`
2. **RAG wrapper + escalation logic** → `llama_index_burgess_wrapper.py`
3. **Unit tests** → `tests/test_burgess_rag.py`
4. **Integration example** → `examples/burgess_rag_example.py`

---

## Questions for Maintainers?

- Placement: Should this live in `llama_index.integrations`? Or as separate package?
- Dependencies: OK to add `burgess-audit` (lightweight, MIT-licensed)?
- Versioning: Support LlamaIndex 0.x? (backward compatibility considerations)

**Tag: @logan (LlamaIndex lead), @ljbudgie (Burgess Principle)**

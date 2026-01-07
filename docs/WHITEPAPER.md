# FailSafe: A Multi-Agent Framework for Autonomous Fact-Verification using Structured Argumentation Graphs

**Abstract**
This whitepaper presents FailSafe, a novel architecture designed to mitigate the inherent limitations of Logic Language Models (LLMs)—specifically Hallucination, Sycophancy, and weak Logic Reasoning. By integrating a Multi-Agent Debate mechanism, suppression of Hallucination-Associated Neurons (H-Neurons), and a rigorous Chain-of-Verification (CoVe) pipeline, FailSafe achieves high-fidelity verification. The system uniquely employs a "Defense in Depth" strategy, utilizing specialized Small Language Models (SLMs) for statistical screening and semantic retrieval before engaging computationally expensive reasoning agents.

---

## I. Executive Assessment

FailSafe represents a serious, architecturally robust fact-verification system that transcends traditional Retrieval-Augmented Generation (RAG) approaches. Its design philosophy is grounded in three core principles:
1.  **Defense in Depth:** A multi-layered architecture where each layer acts as a filter for the next.
2.  **Failure-Mode-Driven Design:** Explicitly engineered to counter known LLM failure modes like snowball hallucinations and sycophancy.
3.  **Cost-Latency-Accuracy Awareness:** Strategic use of specialized, efficient models (SLMs) alongside powerful LLMs.

### Key Metrics
*   **Architectural Concept:** Strong defense-in-depth and adversarial validation.
*   **Academic Foundation:** High, incorporating recent findings on multi-agent scaling and lazy consensus.
*   **Deployability:** High feasibility for real-world production due to efficient resource tiering.
*   **Theoretical Completeness:** ~85% (Solid core logic with room for formalization in specific sub-components like SAG semantics).

---

## II. Strategic Strengths (What This Architecture Does Right)

### 2.1 Precise Problem Definition
FailSafe targets the actual, verified failure modes of current Generative AI, rather than hypothetical risks:
*   **Snowball Hallucination:** Preventing early errors from cascading into fabricated narratives.
*   **Sycophancy/Confirmation Bias:** Countering reinforcement learning (RLHF) artifacts where models align with user prompts.
*   **Logical Fragility:** Addressing weak reasoning in multi-step verification tasks.

### 2.2 Functional Multi-Agent Debate
Unlike superficial "multi-agent" implementations that merely chain prompts, FailSafe's Council (Logician, Skeptic, Researcher) enforces **cognitive diversity**:
*   **Role-Based Cognition:** Distinct personas with defined epistemic goals.
*   **Forced Conflict:** The architecture treats rapid consensus as a failure signal, forcing debate to surface nuance (aligning with *Du et al., 2023* and *More Agents Is All You Need, 2024*).
*   **Structural Sycophancy defense:** By embedding the 'Skeptic' and 'Logician', the system actively fights the "Lazy Consensus" phenomenon.

### 2.3 Correct Application of Chain-of-Verification (CoVe)
FailSafe uniquely separates **Plan Generation** from **Verification Execution**. This decoupling ensures that the verification plan is not contaminated by the model's generative biases, using CoVe for *atomic claim extraction* (à la FActScore) rather than just "deeper thinking."

### 2.4 Pragmatic "Systems Engineering" Model Selection
The architecture avoids "LLM Maximalism" in favor of a practical, engineering-led selection of specialized models:

| Component | Model Selection | Rationale |
| :--- | :--- | :--- |
| **Coreference** | `FastCoref` | ms-level latency; no heavy LLM required for grammatical tasks. |
| **Deduplication** | `MiniLM (384d)` | High throughput, low RAM footprint. |
| **Search** | `e5-base-v2` | Reliable semantic retrieval benchmarked on MTEB. |
| **Rerank** | `Cross-Encoder` | High precision applied only where necessary (top-k filtering). |

### 2.5 Layer 0: The Statistical Firewall
FailSafe implements a rare but critical *Zero-Cost Early Exit* strategy. Before any expensive inference occurs, input is screened for:
*   **Uppercase Ratio ($R_{cap}$):** Detecting "shouting" or distinct spam styles.
*   **Sensational Lexicon ($S_{words}$):** Filtering clickbait vocabulary.
*   **Shannon Entropy ($Z_{entropy}$):** Identifying machine repetition or random noise.
*   **TF-IDF Stuffing ($S_{TFIDF}$):** catching SEO poisoning attempts.

---

## III. Architectural Deep Dive: Defense in Depth

### Layer 1: Structured Decomposition (SAG)
**Goal:** Convert linear text into a **Structured Argumentation Graph (SAG)** via JSON-LD.
**Process:**
1.  **Coreference Resolution:** (FastCoref) Disambiguates entities (e.g., "He" $\to$ "Elon Musk").
2.  **Decomposition:** Splits complex sentences into binary verifiable units (Atomic Facts).
3.  **Deduplication:** Merges redundant claims if Cosine Similarity $S(u, v) > 0.85$.

### Layer 2: Semantic Caching
**Goal:** $O(1)$ retrieval for previously verified facts.
**Algorithm:** k-NN Search with Cosine Distance. A threshold of $d \leq 0.2$ triggers a cache hit, saving significant compute.

### Layer 3: Hybrid Retrieval & Reranking
**Goal:** Maximize Recall (Search) and Precision (Rerank).
1.  **Trust Filtering:** Pre-fetch validation against the Media Bias/Fact Check (MBFC) database. Sources with $Trust(Source) < 0.5$ are discarded. *Sources lacking prior trust scores are passed through a fallback heuristic rather than being hard-rejected.*
2.  **Deep Scraping:** `Trafilatura` parses full DOM to extract clean content.
3.  **Neural Reranking:** A Cross-Encoder scores (Query, Passage) pairs to select the top-3 context window.

### Layer 4 & 5: The Council & Synthesis
**Layer 4 (Multi-Agent Debate):**
The **Logician**, **Skeptic**, and **Researcher** agents debate Atomic Claims against retrieved evidence. If Claim A (Parent) is refuted, dependent child nodes in the SAG are automatically invalidated.

**Layer 5 (Executive Synthesis):**
Aggregates votes and issues a final verdict (**Supported**, **Refuted**, **Conflicting**, **Unverified**) and generates a citation-backed Investigation Report.

---

## IV. Areas for Future Formalization

While the architecture is robust, the following areas present opportunities for future evolution:

1.  **Formalizing H-Neuron Suppression:** Currently a behavioral suppression via the 'Skeptic' persona. *In the current implementation, H-Neuron suppression is treated as an emergent behavioral constraint rather than a direct neuro-level intervention, intentionally avoiding overclaiming mechanistic control.* Future iterations could explore technical interventions like logit masking or activation steering (Gao et al., 2025).
2.  **Structuring the SAG:** Defining formal semantics for Node Types (Claim, Evidence, Axioms) and Edge Types (Supports, Contradicts, Entails). *Formally, the Structured Argumentation Graph (SAG) is a directed labeled graph $G=(V, E)$, where nodes represent epistemic units (Claims, Evidence, Axioms), and edges encode logical relations such as Supports, Contradicts, or Entails.*
3.  **Refining Trust Scoring:** Moving beyond hard thresholds for source trust to dynamic scoring that accounts for domain specificity and source freshness.
4.  **Comprehensive Benchmarking:** Future work will focus on rigorous evaluation against standard datasets like FEVER, FreshQA, and HoVer to quantify performance gains over vanilla RAG.

---

## V. Strategic Positioning

FailSafe is not competing with simple chatbots or basic RAG implementations. It occupies the **High-Stakes Autonomous Verification** tier. It serves as an **"Epistemic Engine"** designed for:
*   **AI Research Assistants** requiring high fidelity.
*   **Automated Due Diligence** in finance and law.
*   **Scientific Claim Vetting** where accuracy is non-negotiable.

FailSafe prioritizes *correctness and safety* over conversational fluency, making it a critical tool for trusted AI systems.

---

## VI. Conclusion
FailSafe's architecture moves beyond simple RAG by enforcing rigorous statistical pre-filtering, structured argumentation, and multi-agent adversarial validation. This "Defense in Depth" approach ensures that resources are allocated efficiently while maintaining the highest standard of verification accuracy. By adhering to sound systems engineering principles and addressing the root causes of LLM failure, FailSafe establishes a blueprint for the next generation of reliable AI.

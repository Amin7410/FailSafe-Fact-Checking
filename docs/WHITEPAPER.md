# FailSafe: A Multi-Agent Framework for Autonomous Fact-Verification using Structured Argumentation Graphs

**Abstract**
This whitepaper presents FailSafe, a novel architecture designed to mitigate the inherent limitations of Logic Language Models (LLMs)—specifically Hallucination, Sycophancy, and weak Logic Reasoning. By integrating a Multi-Agent Debate mechanism, suppression of Hallucination-Associated Neurons (H-Neurons), and a rigorous Chain-of-Verification (CoVe) pipeline, FailSafe achieves high-fidelity verification. The system uniquely employs a "Defense in Depth" strategy, utilizing specialized Small Language Models (SLMs) for statistical screening and semantic retrieval before engaging computationally expensive reasoning agents.

---

## I. Theoretical Framework & Problem Solving

### 1.1 Overcoming Sycophancy & Confirmation Bias
**The Problem:** RLHF-tuned models exhibit *sycophancy*—biasing answers to align with user prompts—and *conflict avoidance*, which compromises objective verification.
**The Solution: Multi-Agent Debate**
FailSafe abandons the "Single Agent" paradigm for a dialectical Council.
*   **Cognitive Diversity:** Drawing on *Du et al. (2023)* and *More Agents Is All You Need (2024)*, we demonstrate that accuracy scales with the diversity of viewpoints, not just model size.
*   **The Persona Triad:**
    1.  **The Logician:** Detects formal fallacies.
    2.  **The Skeptic:** Designed to suppress "H-Neurons" (Gao et al., 2025) by applying *Occam's Razor*.
    3.  **The Researcher:** Validates evidence consensus.
*   **Mechanism:** Sycophancy serves as a failure mode; forced conflict in the debate layer breaks the "lazy consensus" (Wei et al., Google DeepMind, 2024).

### 1.2 Addressing "Snowball Hallucinations"
**The Problem:** LLMs suffer from *self-consistency hallucination*, where early errors cascade into fabricated narratives.
**The Solution:** Modified Chain-of-Verification (CoVe).
*   **Decoupling:** Based on *Dhuliawala et al. (2023)*, we separate **Plan Generation** from **Verification Execution**. Layer 1 (Decomposition) uses CoVe to extract atomic claims without verifying them, acting as the first "Safety Valve".

---

## II. Architectural Logic & Model Selection

FailSafe optimizes the **Accuracy-Cost-Latency** trade-off by offloading tasks to specialized local models.

### 2.1 Contextual Disambiguation: `FastCoref`
*   **Challenge:** Pronoun ambiguity (e.g., "He said") degrades retrieval precision.
*   **Model:** **FastCoref** (DistilRoBERTa-based).
*   **Justification:** Achieves **81.5% F1-score** on OntoNotes 5.0 benchmarks. Unlike multi-GB LLMs, FastCoref resolves coreferences in milliseconds, adhering to the principle of *Task Decomposition*.

### 2.2 Vector Space Efficiency: `all-MiniLM-L6-v2` & `intfloat/e5-base-v2`
*   **Challenge:** Real-time deduplication and caching require thousands of comparisons per second.
*   **Model:** `all-MiniLM-L6-v2` (384d) for deduplication; `e5-base-v2` (768d) for semantic search.
*   **Justification:**
    *   **Speed:** MiniLM performs batch inference at **14,200 sentences/sec**.
    *   **Cost:** 384-dimensional vectors reduce index size and RAM usage exponentially compared to 1024d+ vectors, while maintaining "Good Enough" MTEB scores for fact retrieval.

---

## III. The Pipeline: Defense in Depth

### Layer 0: Statistical Screening (The Zero-Cost Firewall)
**Goal:** Reject spam/clickbait before expensive LLM inference (Early Exit).
**Logic:** A weighted score (S) triggers hard rejection if high.

$$ Score = 1.5 \cdot R_{cap} + 3.0 \cdot S_{words} + 1.0 \cdot Z_{entropy} + 0.35 \cdot S_{TFIDF} $$

1.  **$R_{cap}$ (Uppercase Ratio):** Detects "shouting" style ($R_{cap} = \frac{Caps}{TotalChars}$).
2.  **$S_{words}$ (Sensationalism):** Frequency of emotive lexicon (e.g., "SHOCKING", "EXPOSED").
3.  **$Z_{entropy}$ (Shannon Entropy):** Detects machine repetition or random noise.
    *   $$ H(X) = - \sum p(x_i) \log p(x_i) $$
    *   Normalized against *ag_news* baseline ($\mu \approx 4.5\text{-}6.0$ bits/word).
4.  **$S_{TFIDF}$ (Keyword Stuffing):** Penalizes SEO spam.

### Layer 1: Structured Decomposition (SAG)
**Goal:** Convert linear text into a **Structured Argumentation Graph (SAG)** using **JSON-LD**.
**Process:**
1.  **Coreference Resolution:** Resolve "He" -> "Elon Musk".
2.  **Decomposition (Atomic Facts):** Adhering to *FActScore* (Min et al., 2023), splitting complex sentences into binary verifiable units.
3.  **Deduplication:** Merge claims if Cosine Similarity $S(u, v) > 0.85$.

### Layer 2: Semantic Caching
**Goal:** $O(1)$ retrieval for previously verified facts.
**Algorithm:** k-NN Search.
*   **Metric:** Cosine Distance $d = 1 - \frac{A \cdot B}{\|A\|\|B\|}$.
*   **Threshold:** If $d \leq 0.2$, trigger **CACHE HIT** (Return stored verdict). Else, **CACHE MISS** (Proceed to search).

### Layer 3: Hybrid Retrieval & Reranking
**Goal:** Maximize Recall (Search) and Precision (Rerank).
1.  **Query Generation:** LLM expands query to fix vocabulary mismatch.
2.  **Trust Filtering:** Pre-fetch check against Media Bias/Fact Check (MBFC) database.
    *   If $Trust(Source) < 0.5 \rightarrow$ Discard.
3.  **Deep Scraping:** `Trafilatura` parses full DOM to remove boilerplate/ads.
4.  **Neural Reranking (Cross-Encoder):**
    *   Unlike Bi-Encoders, Cross-Encoders process (Query, Passage) simultaneously.
    *   $$ Score(q, p) = \sigma(W \cdot BERT(q, [SEP], p) + b) $$
    *   Selects Top-3 context window.

### Layer 4 & 5: The Council & Synthesis
**Layer 4 (Multi-Agent Debate):**
*   The **Logician**, **Skeptic**, and **Researcher** debate the Atomic Claims against the Retrieved Evidence.
*   **Causal Tracing:** If Claim A is refuted, child nodes relying on A are invalidated in the SAG.

**Layer 5 (Executive Synthesis):**
*   Aggregates votes and issues a specific verdict: **Supported**, **Refuted**, **Conflicting**, or **Unverified**.
*   Generates a human-readable Investigation Report with precise citations.

---

## Conclusion
FailSafe's architecture moves beyond simple RAG by enforcing rigorous statistical pre-filtering, structured argumentation, and multi-agent adversarial validation. This "Defense in Depth" approach ensures that resources are allocated efficiently while maintaining the highest standard of verification accuracy.

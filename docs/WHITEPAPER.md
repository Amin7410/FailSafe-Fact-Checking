# FailSafe: A Multi-Agent Framework for Autonomous Fact-Verification using Structured Argumentation Graphs

**Abstract**
FailSafe is an autonomous "Epistemic Engine" designed to mitigate the fundamental failure modes of Large Language Models (LLMs)—specifically Hallucination, Sycophancy, and Logical Inconsistency. Unlike traditional RAG pipelines that prioritize retrieval recall, FailSafe prioritizes **epistemic integrity** through a "Defense in Depth" architecture. This whitepaper details the scientific basis, architectural decisions, and the "Expertocracy" consensus mechanism that powers the system.

---

## PART 1: SOLVING HALLUCINATION, SYCOPHANCY, AND LAZY CONSENSUS

This section addresses the core psychological and structural failures of current Generative AI systems.

### 1. The Problem: Sycophancy & Confirmation Bias
**The Reality:** Modern LLMs are trained using RLHF (Reinforcement Learning from Human Feedback) to be "helpful" and "harmless." This creates a dangerous side effect: models tend to agree with the user's worldview (**Sycophancy**) or avoid conflict rather than stating uncomfortable truths.

**FailSafe's Solution: Multi-Agent Debate Architecture**
Instead of a single "Generalist" model, we employ a Council of adversarial agents.
*   **Why avoiding Single Agent?** A single model, no matter how large, possesses a "single stream of thought." It is prone to **Mode Collapse**, quickly converging on a conclusion without considering outlier perspectives.

**Scientific Basis:**
*   **"Improving Factuality and Reasoning in Language Models through Multiagent Debate" (Du et al., 2023)** & **"More Agents Is All You Need" (2024)**: These studies prove that factual accuracy does not scale linearly with model size, but rather with **Cognitive Diversity**.
*   **"Sycophancy in Large Language Models" (Wei et al., Google DeepMind, 2024)**: Demonstrates that the only way to eliminate sycophancy is to decouple the "Evaluator" role from the "Generator" role.

**Application:** 
FailSafe forces conflict between three distinct personas:
1.  **The Logician:** Checks for formal fallacies.
2.  **The Researcher:** Provides raw data.
3.  **The Skeptic:** Explicitly designed to suppress **"H-Neurons"**.
    *   *Reference:* **"H-Neurons: On the Existence, Impact, and Origin of Hallucination-Associated Neurons in LLMs" (Gao et al., Tsinghua University, 12/2025)**. This research found that specific neurons (<0.1%) are responsible for hallucinations. The "Skeptic" persona acts as a behavioral inhibition mechanism to suppress these neurons.

### 2. The Problem: Snowball Hallucination
**The Reality:** When an LLM makes a small error early in a generation, it tends to fabricate further details to rationalize that error (**Self-consistency hallucination**).

**FailSafe's Solution: Modified Chain-of-Verification (CoVe)**
*   **Why CoVe over CoT?** Chain-of-Thought (CoT) happens in a single pass. If step 1 is wrong, step 2 will be wrong. CoVe splits the process into independent "Plan" and "Execute" phases.

**Scientific Basis:**
*   **"Chain-of-Verification Reduces Hallucination in Large Language Models" (Dhuliawala et al., Meta AI, 2023)**: The seminal paper establishing that decoupling verification planning from execution reduces pressure on the model to "save face."
*   **"Self-Refine: Iterative Refinement with Self-Feedback" (Madaan et al., 2024)**.

**Application:**
In Layer 1 (Decomposition), FailSafe uses CoVe not to answer, but to **extract**. We create a "Safety Valve" by breaking complex narratives into **Atomic Facts** before any verification occurs.

### 3. The Problem: Poor Logical Reasoning
**The Reality:** LLMs are linguistic experts but formal logic novices. They struggle with temporal reasoning (e.g., recognizing that "King Quang Trung using a smartphone" is impossible).

**FailSafe's Solution: Role-Based Reasoning (Persona Prompting)**
Assigning specific roles acts as **Attention Masking**, directing the model's focus to a single aspect (Logic or Evidence) and ignoring noise.

**Scientific Basis:**
*   **"Unleashing Cognitive Synergy in Large Language Models" (2024)**: Specialized personas activate different regions in the model's latent space.

---

## PART 2: SYSTEM OPTIMIZATION WITH SPECIALIZED LOCAL MODELS

To solve the "Performance vs. Cost" dilemma, FailSafe integrates specialized Deep Learning models (SLMs) locally, avoiding the wastefulness of using LLMs for every micro-task.

### 1. Contextual Ambiguity from Coreferences
**The Problem:** LLMs misinterpret "He", "It", "They" when sentences are extracted out of context.
**Solution:** **FastCoref** (DistilRoBERTa-based).
**Rationale:**
*   **Performance:** OntoNotes 5.0 F1-score of **81.5%**.
*   **Efficiency:** Processing text takes milliseconds. Using an LLM for this is computational overkill. This follows the **Task Decomposition** principle.

### 2. Performance of Semantic Search & Deduplication
**The Problem:** The system must perform thousands of semantic comparisons per second for Deduplication (Layer 1) and Caching (Layer 2).
**Solution:** **all-MiniLM-L6-v2** and **intfloat/e5-base-v2**.
**Rationale:**
*   **Speed is King:** MiniLM handles batch inference at **14,200 sentences/sec**.
*   **Cost:** 384-dimensional vectors reduce RAM/CPU usage exponentially compared to 1024d+ vectors.
*   **"Good Enough":** Based on **MTEB (Massive Text Embedding Benchmark)**, verified trade-offs show that a 5% accuracy gain from larger models is not worth a 10x latency penalty.

### 3. Objective Truth Measurement (Atomic Facts)
**The Problem:** How do we measure if a claim is verifiable?
**Solution:** **FActScore** (Min et al., 2023).
**Application:** FailSafe defines an "Atomic Fact" as a binary unit of information (True/False). This concept acts as the API contract between the Decomposition Layer and the Verification Layer.

### 4. Noise Filtering (Reranking)
**The Problem:** Search engines return top-10 results, but often only 1-2 are relevant.
**Solution:** Two-Step Reranking.
1.  **Bi-Encoder (MiniLM):** Fast Retrieval (High SCALL).
2.  **Cross-Encoder:** Precise Reranking (High PRECISION).
**Rationale:** Cross-Encoders (scoring Query-Passage pairs together) achieve MRR@10 of 0.39 on MS MARCO, significantly outperforming simple embeddings.

---

## PART 3: DEFENSE IN DEPTH VIA STATISTICAL STYLOMETRY

**The Goal:** A "Zero-Cost Early Exit" strategy to reject spam/clickbait before expensive inference.

### 1. Shannon Entropy (Information Theory)
**Metric:** $H(X) = - \sum p(x) \log p(x)$
**Rationale:** Spam and bot-generated text often exhibit low entropy (high repetitiveness). This is an objective, mathematical measure of text complexity independent of semantic bias.

### 2. TF-IDF & Benchmarking
**Rationale:** By benchmarking input against the **ag_news** dataset (120k+ articles), we establish a baseline for "normal" journalistic writing.
**Application:** Inputs triggering high "Keyword Stuffing" scores (via TF-IDF outliers) are flagged as SEO spam and rejected immediately.

---

## PART 4: KNOWLEDGE REPRESENTATION (SAG)

### 1. Limits of Linear Text
**The Problem:** LLMs struggle to maintain logical consistency across long contexts (Linear processing).
**Solution:** **Structured Argumentation Graph (SAG)** using **JSON-LD**.
**Scientific Basis:** Argumentation Mining & Knowledge Graphs.
**Application:**
*   **JSON-LD:** W3C standard for Linked Data (compatible with Google/Bing).
*   **Graph Logic:** Allows Causal Tracing. If Claim A (Support) is refuted, Claim B (Conclusion) collapses. This enables **Chain-of-Reasoning** that linear text cannot support.

### 2. Semantic Similarity (Cosine Similarity)
**Rationale:** Standard metric for vector space density.
**Application:** Ensures that "The earth is round" and "Our planet is spherical" are treated as the same node in the SAG, preventing redundant verification cycles.

---

## Conclusion
FailSafe is not a patchwork of tools; it is a **systems engineering approach** to AI safety. By combining statistical rigour (Layer 0), specialized SLMs (Layer 1-3), and adversarial Agents (Layer 4), it creates a verification engine that is structurally resistant to the most common failures of modern Artificial Intelligence.


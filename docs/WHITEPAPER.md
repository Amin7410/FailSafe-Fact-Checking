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
    *   *Parsimony Integration:* The Skeptic operates on **Occam's Razor**, rejecting complex conspiracies in favor of simpler explanations.

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

## PART 2: DETAILED TECHNICAL ARCHITECTURE (LAYERS 0-5)

This section details the rigorous engineering implementation of FailSafe's "Defense in Depth" strategy, specifically isolating the Logic of each layer, the specialized models used, and the mathematical principles applied.

### LAYER 0: THE STATISTICAL FIREWALL
**Core Objective:** "Early Exit".
The system rejects processing if the input satisfies the logical AND condition:
`Source Trust == LOW` **AND** `Sensationalism Score > 0.5`.

#### Module A: Metadata Analysis (Source Integrity)
*   **File:** `factcheck/core/Screening.py` (Class `MetadataAnalyzer`)
*   **Workflow:**
    1.  **Domain Extraction:** Regex parsing (e.g., `cnn.com` from URL).
    2.  **Allow/Blocklist Check:** Immediate filtering for known government/educational sites (High Trust) or known phishing sites (Block).
    3.  **O(1) Fast Lookup:** Queries local SQLite (`data/sources.db`) populated with *Media Bias/Fact Check (MBFC)* data.
        *   `SELECT credibility, bias FROM sources WHERE domain = ?`
    4.  **Fallback:** Calls Gemini Flash for on-the-fly evaluation if domain is unknown.
*   **Output:** Trust Label (High, Mixed, Low).

#### Module B: The Screening Advisor (Semantic Memory)
*   **File:** `factcheck/core/Screening.py` (Class `ScreeningAdvisor`)
*   **Workflow:**
    1.  **Vector Embedding:** Encodes input using `intfloat/e5-base-v2` into vector $V_{new}$ (768d).
    2.  **Memory Query:** Compares $V_{new}$ against ChromaDB (containing previously verified fake news $V_{old}$).
    3.  **Cosine Similarity Calculation:**
        $$ Similarity = \cos(\theta) = \frac{V_{new} \cdot V_{old}}{\|V_{new}\| \|V_{old}\|} $$
        *   Standard Threshold: Distance $< 0.5$.
    4.  **Decision:** If Similarity $> 0.85$ (Distance $< 0.15$), the Advisor identifies an exact match to a known scam.
*   **Action:** Immediate **SKIP**. Returns `FAKE` verdict.

#### Module C: Stylometry Analysis (Statistical Engine)
*   **File:** `factcheck/core/Screening.py` (Class `StylometryAnalyzer`)
*   **Objective:** Detect "fake news style" via statistical linguistics without deep semantic parsing.
*   **Scoring Formula:**
    $$ Score = 1.5(R_{cap}) + 3.0(S_{words}) + 1.0(Z_{Entropy}) + 0.35(S_{TFIDF}) $$

    *   **1. Uppercase Ratio ($R_{cap}$):** Detects "shouting" style.
        $$ R_{cap} = \frac{\text{Count(Uppercase)}}{\text{Count(Total Letters)}} $$
    *   **2. Sensationalism ($S_{words}$):** Frequency of trigger words (e.g., "shocking", "exposed", "miracle"). Weighted highest (3.0).
    *   **3. Shannon Entropy ($Z_{entropy}$):** Based on Information Theory to measure randomness.
        $$ H(X) = - \sum p(x_i) \log_2 p(x_i) $$
        *   **Z-Score Normalization:** Compares current entropy $H$ against the `ag_news` baseline mean ($\mu$) and std ($\sigma$).
        $$ Z = \frac{H - \mu}{\sigma} $$
    *   **4. Keyword Stuffing ($S_{TFIDF}$):** Uses TF-IDF to detect unnatural repetition of keywords common in SEO spam.

**Logic Gate:**
*   IF `Source == Unknown/Low` AND `Sensationalism > 0.5` $\to$ **EARLY EXIT**.

---

### LAYER 1: UNSTRUCTURED TO STRUCTURED (DECOMPOSITION)
**Core Objective:** Convert raw text into structured **Atomic Claims** (JSON-LD) for logical processing.

#### 1. Coreference Resolution
*   **File:** `factcheck/core/Coreference.py` (Class `ReferenceResolver`)
*   **Model:** **FastCoref** (DistilRoBERTa architecture).
*   **Problem:** LLMs fail when extracting sentences with pronouns like "He" or "It" out of context.
*   **Solution:** Cluster mentions (e.g., `{Elon Musk, CEO Tesla, He}`) and replace all mentions with the head entity.
*   **Performance:** ~81.5% F1-Score (OntoNotes 5.0).

#### 2. SAG Construction (Structured Argumentation Graph)
*   **File:** `factcheck/core/Decompose.py` (Class `Decompose`)
*   **Engine:** Gemini Flash (CoVe Baseline).
*   **Mapping:** $\Psi: D \to G(V, E)$
*   **Standard:** **JSON-LD** (Linked Data).
*   **Entities:** Nodes (Claims), Edges (Relationships: Support/Attack).

#### 3. Deduplication
*   **File:** `factcheck/core/Decompose.py`
*   **Model:** **all-MiniLM-L6-v2** (384d, 14,200 sentences/sec).
*   **Algorithm:** Cosine Similarity on Claim Embeddings ($v_i, v_j$).
    $$ S(i, j) = \cos(\theta) = \frac{v_i \cdot v_j}{\|v_i\| \|v_j\|} $$
*   **Rule:** If $S > 0.85$, merge nodes to reduce verification cost.

---

### LAYER 2: VERIFIABILITY & CACHING
**Core Objective:** Check if the claim is factual (verifiable) and if it has been checked before.

#### 1. Verifiability Check
*   **Mapping:** $c_i \to y \in \{0, 1\}$
    *   $y=1$: Fact (Verifiable). Proceed.
    *   $y=0$: Opinion/Question. **DISCARD**.

#### 2. Semantic Mapping & Caching
*   **Model:** `intfloat/e5-base-v2` (768d).
*   **Query:** $k$-NN Search in ChromaDB (Collection: `verified_facts`).
*   **Metric:** Cosine Distance ($d = 1 - Similarity$).
*   **Threshold ($\tau$):** `0.2`.
*   **Workflow:**
    *   **Branch 1 (CACHE HIT, $d \le 0.2$):** Two claims are semantically identical. Return stored verdict immediately (~10ms latency).
    *   **Branch 2 (CACHE MISS, $d > 0.2$):** Push claim to **Batch Processing Queue** (Batch size = 5) for Layer 3 processing.

*   **Feedback Loop:** Verified results from L5 are fed back into L2 cache, enabling dynamic learning.

---

### LAYER 3: HYBRID RETRIEVAL & RERANKING
**Core Objective:** Retrieve high-trust evidence with maximum Recall and Precision.

#### 1. Query Generation
*   **Goal:** Solve "Vocabulary Mismatch" (e.g., User: "Musk buys Blue Bird" vs Index: "Elon Musk acquires Twitter").
*   **Output:** Generalized keyword set $\{q_1, q_2, \dots, q_k\}$.

#### 2. Candidate Retrieval
*   **Source:** Google Index (via Serper API).
*   **Action:** Retrieve Top-K candidates (URLs).
*   **Trust Filtering:**
    *   Function $T(url) \in [0, 1]$.
    *   If $T(url) < 0.5$ (Low MBFC score) $\to$ **Skip Deep Scraping** (Prevention of misinformation poisoning).

#### 3. Deep Scraping
*   **Lib:** `Trafilatura`.
*   **Process:** Parse DOM Tree $\to$ Extract Main Text $\to$ Remove Noise (Ads, Nav).

#### 4. Neural Reranking
*   **Architecture:** **Cross-Encoder**.
*   **Differentiation:** Unlike Bi-Encoders (L1/L2) which treat vectors independently, Cross-Encoders process (Query, Passage) pairs together.
*   **Scoring:**
    $$ Score(q, p) = \sigma(W \cdot BERT(q, p) + b) $$
*   **Output:** Top-3 passages ($D_{sorted}$) selected as **Final Context**.

---

### LAYER 4: THE COUNCIL (MULTI-AGENT DEBATE)
**Core Objective:** Surface truth via cognitive conflict.

**Personas:**
*   **The Logician:** Identifies fallacies and temporal inconsistencies.
*   **The Skeptic:** "Devil's Advocate" - utilizes *Occam's Razor* to oppose conspiracy theories.
*   **The Researcher:** Aligns claims with Layer 3 evidence.

**Mechanism:** Agents debate iteratively based on the SAG structure. If a Parent Node ($A$) is refuted, all Child Nodes dependent on $A$ are invalidated (Causal Tracing).

---

### LAYER 5: EXECUTIVE SYNTHESIS
**Core Objective:** Final adjudication.

**Logic:**
*   **Aggregation:** Weighted voting from Council members.
*   **Hard Rules:**
    *   High Refutation Ratio $\to$ **FALSE**.
    *   Insufficient Evidence $\to$ **UNVERIFIED** (System refuses to guess).
*   **Output:** Investigation Report containing Verdict, Citations, and Logic Trace.

---

## Conclusion
FailSafe uses a "Systems Engineering" approach to AI safety. By combining solid statistical mathematics (Layer 0), optimized local models (Layers 1-2), and rigorous multi-agent logic (Layers 4-5), it creates a verification engine that is structurally immune to the common pitfalls of Sycophancy and Snowball Hallucinations.

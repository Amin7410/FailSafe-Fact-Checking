# Feature Proposal: Confidence-Weighted Soft Voting for Multi-Agent Council

**Status:** Planned / Draft
**Target Component:** `factcheck.core.ClaimVerify` (The Council)
**Owner:** @Amin7410

---

## 1. Rationale: Why do we need this?

**Current State:**
The current consensus mechanism uses **Simple Majority Voting (Hard Voting)**. If the *Researcher* finds strong evidence refuting a claim, but the *Logician* and *Skeptic* vaguely support it (due to lack of obvious logical errors), the system outputs a False Positive "SUPPORTS" verdict (2 vs 1).

**The Problem:**
- **Equality Bias:** Not all agents are equal in all contexts. The *Researcher's* "Refutes" based on hard evidence should carry more weight than the *Logician's* "Supports" based on sentence structure.
- **Lack of Nuance:** A "51% sure" vote counts the same as a "99% sure" vote. This leads to brittle verdicts in ambiguous cases.

**The Goal:**
Implement a **Confidence-Weighted Soft Voting** system where the final verdict is determined by the *sum of confidence scores* rather than the *count of votes*.

---

## 2. Impact Analysis

### Pros (Advantages)
1.  **Higher Accuracy:** reduces False Positives by allowing strong evidence to override weak agreement.
2.  **Experts-in-the-Loop:** Mimics real-world decision-making where the domain expert's opinion (e.g., Researcher) matters more than the generalist's.
3.  **Nuanced Verdicts:** Enables the system to output "Conflicting" or "Unverified" when confidence sums are close, rather than forcing a binary decision.

### Cons (Disadvantages)
1.  **Complexity:** Adds computational logic and requires parsing float values from LLM outputs (potential for parsing errors).
2.  **Tuning Difficulty:** "Magic Numbers" (weights) like 1.2x or 1.5x can be arbitrary. Tuning them requires a ground-truth dataset (Benchmark).
3.  **Prompt Sensitivity:** Use of `confidence` scores relies on the LLM's self-calibration, which can be unreliable (LLMs are often overconfident).

---

## 3. Implementation Strategy

### Phase 1: Soft Voting (The "Must-Have")
*Objective: Sum confidence scores instead of counting votes.*

1.  **Prompt Engineering:**
    - Update `Logician`, `Researcher`, `Skeptic` prompts to output JSON with a `confidence` field (0.0 to 1.0).
    - Example: `{"verdict": "REFUTES", "confidence": 0.9, "reasoning": "..."}`.
2.  **Aggregator Logic:**
    - Calculate `Total_Support_Score = Sum(Confidence_Support)`
    - Calculate `Total_Refute_Score = Sum(Confidence_Refute)`
    - If `|Total_Support - Total_Refute| < 0.2` -> Verdict is **CONFLICTING**.

### Phase 2: Domain-Weighted Rules (The "Nice-to-Have")
*Objective: Give "Veto Power" or "Bonus Weight" to specific roles.*

1.  **Weights Configuration:**
    ```python
    WEIGHTS = {
        "Researcher": 1.5,  # High trust for external evidence
        "Logician": 1.0,
        "Skeptic": 1.1      # Tie-breaker bias towards safety
    }
    ```
2.  **Weighted Sum:**
    - `Score += Confidence * Weight[Role]`

### Recommended Stack
- No new libraries needed.
- Modify `factcheck/core/ClaimVerify.py`.

---

## 4. Contingency Plan (Fallback)

**Risk:** The LLM fails to output a valid float `confidence` score (e.g., returns "High" instead of 0.9 or omits the field).

**Fallback Strategy:**
1.  **Default Value:** If parsing fails, assign a default confidence of **0.5** (Neutral/Unsure).
2.  **Revert to Majority:** If >50% of agents fail to return confidence scores, the system automatically degrades back to **Simple Majority Voting** (Current logic) and logs a warning.
3.  **Hard Veto:** If *any* agent returns "REFUTES" with Confidence > 0.95, immediate override to "REFUTES" regardless of other votes (Safety First).

---

## 5. Next Steps
1.  Create a branch `feature/weighted-voting`.
2.  Update prompts in `factcheck/config/prompts.yaml` (if exists) or code.
3.  Run `pytest` on `ClaimVerify` to ensure no regression.

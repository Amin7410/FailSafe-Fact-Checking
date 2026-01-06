
from factcheck import FactCheck

# Initializes the system with default configuration
print("Initializing FailSafe Fact-Checking System...")
fc = FactCheck.from_config()

# Define a test claim
text_to_check = "The Eiffel Tower is located in Rome, Italy."

print(f"\nChecking claim: '{text_to_check}'")
print("-" * 50)

# Run the fact-checking pipeline
result = fc.check_text_with_progress(text_to_check, session_id="demo_session")

# Display the final verdict
print("\n" + "="*20 + " RESULTS " + "="*20)
print(f"Final Verdict: {result.get('verdict', 'Unknown')}")
print(f"Confidence Score: {result.get('final_score', 0)}")
print("\nSummary:")
print(result.get("summary", {}).get("message", "No summary available."))

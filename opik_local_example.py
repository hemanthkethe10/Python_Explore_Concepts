"""
Opik Prompt Optimization - Local Mode Example
==============================================
This example runs Opik in local mode without needing a Comet ML account.
"""

import os

# Configure for local mode (no cloud tracking)
os.environ["OPIK_URL_OVERRIDE"] = "http://localhost:5173/api"
os.environ["OPIK_TRACK_DISABLE"] = "true"

def main():
    print("\n" + "=" * 60)
    print("   OPIK PROMPT OPTIMIZATION - LOCAL DEMO")
    print("=" * 60 + "\n")
    
    # Import libraries
    from opik_optimizer import FewShotBayesianOptimizer, ChatPrompt
    from opik.evaluation.metrics import LevenshteinRatio
    import litellm
    
    print("✓ Libraries loaded\n")
    
    # Step 1: Create a simple dataset (as a list of dicts)
    print("STEP 1: Creating evaluation dataset...")
    dataset_items = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
        {"question": "What is the largest planet?", "answer": "Jupiter"},
        {"question": "What year did WW2 end?", "answer": "1945"},
    ]
    print(f"✓ Created {len(dataset_items)} evaluation items\n")
    
    # Step 2: Define initial prompt
    print("STEP 2: Defining prompts...")
    initial_prompt = ChatPrompt(
        messages=[
            {"role": "system", "content": "Answer questions briefly and accurately."},
            {"role": "user", "content": "{question}"}
        ]
    )
    print("✓ Initial prompt: 'Answer questions briefly and accurately.'\n")
    
    # Step 3: Test the prompt with OpenAI
    print("STEP 3: Testing prompt with OpenAI...")
    
    def call_llm(question):
        """Call LLM with the prompt."""
        response = litellm.completion(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer questions briefly and accurately."},
                {"role": "user", "content": question}
            ],
            max_tokens=100,
        )
        return response.choices[0].message.content
    
    # Test one question
    test_q = "What is the capital of France?"
    test_a = call_llm(test_q)
    print(f"  Q: {test_q}")
    print(f"  A: {test_a}")
    print("✓ OpenAI connection working!\n")
    
    # Step 4: Evaluate baseline
    print("STEP 4: Evaluating baseline prompt...")
    
    def evaluate_prompt(dataset, prompt_template):
        """Evaluate a prompt against the dataset."""
        scores = []
        metric = LevenshteinRatio()
        
        for item in dataset:
            response = litellm.completion(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt_template},
                    {"role": "user", "content": item["question"]}
                ],
                max_tokens=50,
            )
            output = response.choices[0].message.content.strip()
            
            # Calculate similarity
            score = metric.score(reference=item["answer"], output=output)
            scores.append(score.value if hasattr(score, 'value') else score)
            
            print(f"  Q: {item['question']}")
            print(f"  Expected: {item['answer']}")
            print(f"  Got: {output}")
            print(f"  Score: {scores[-1]:.2f}")
            print()
        
        return sum(scores) / len(scores)
    
    baseline_score = evaluate_prompt(
        dataset_items[:3],  # Use first 3 for quick demo
        "Answer questions briefly and accurately."
    )
    print(f"\n📊 BASELINE SCORE: {baseline_score:.2%}\n")
    
    # Step 5: Test optimized prompt with few-shot examples
    print("=" * 60)
    print("STEP 5: Testing with few-shot examples...")
    print("=" * 60 + "\n")
    
    optimized_prompt = """Answer questions briefly and accurately.

Here are some examples:
Q: What is 2 + 2?
A: 4

Q: What is the capital of France?
A: Paris

Now answer the following question in the same brief style:"""
    
    print("OPTIMIZED PROMPT (with few-shot examples):")
    print("-" * 40)
    print(optimized_prompt)
    print("-" * 40 + "\n")
    
    optimized_score = evaluate_prompt(
        dataset_items[:3],
        optimized_prompt
    )
    print(f"\n📊 OPTIMIZED SCORE: {optimized_score:.2%}")
    
    # Summary
    print("\n" + "=" * 60)
    print("   SUMMARY")
    print("=" * 60)
    print(f"\n  Baseline Score:  {baseline_score:.2%}")
    print(f"  Optimized Score: {optimized_score:.2%}")
    improvement = (optimized_score - baseline_score) / baseline_score * 100 if baseline_score > 0 else 0
    print(f"  Improvement:     {improvement:+.1f}%")
    print("\n" + "=" * 60)
    print("\n✅ This demonstrates how few-shot examples improve prompts!")
    print("   The Opik optimizer automates this process to find the")
    print("   BEST combination of examples from your dataset.\n")


if __name__ == "__main__":
    main()

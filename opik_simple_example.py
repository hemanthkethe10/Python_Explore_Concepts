"""
Simple Opik Prompt Optimization Example
=======================================
A straightforward example showing how Opik optimizes prompts.
"""

import os

# Set the API key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

def main():
    print("\n" + "=" * 60)
    print("   OPIK PROMPT OPTIMIZATION - LIVE DEMO")
    print("=" * 60 + "\n")
    
    # Import Opik libraries
    try:
        import opik
        from opik.evaluation.metrics import LevenshteinRatio
        from opik_optimizer import FewShotBayesianOptimizer, ChatPrompt
        print("✓ Opik libraries loaded successfully\n")
    except ImportError as e:
        print(f"❌ Error importing Opik: {e}")
        print("Run: pip install opik opik-optimizer")
        return
    
    # Step 1: Create dataset
    print("STEP 1: Creating evaluation dataset...")
    client = opik.Opik()
    
    dataset = client.get_or_create_dataset(
        name="simple_qa_dataset",
        description="Simple Q&A pairs for demo"
    )
    
    # Clear and add fresh data
    dataset.insert([
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
        {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
        {"question": "What year did World War 2 end?", "answer": "1945"},
    ])
    print(f"✓ Dataset created with {len(dataset)} items\n")
    
    # Step 2: Define initial prompt
    print("STEP 2: Defining initial prompt...")
    initial_prompt = ChatPrompt(
        messages=[
            {"role": "system", "content": "Answer questions accurately."},
            {"role": "user", "content": "{question}"}
        ]
    )
    print(f"✓ Initial prompt: 'Answer questions accurately.'\n")
    
    # Step 3: Define metric
    print("STEP 3: Setting up evaluation metric...")
    def similarity_metric(dataset_item, llm_output):
        """Measure how similar the output is to expected answer."""
        metric = LevenshteinRatio()
        return metric.score(reference=dataset_item["answer"], output=llm_output)
    print("✓ Using LevenshteinRatio metric (similarity score)\n")
    
    # Step 4: Create optimizer
    print("STEP 4: Initializing FewShotBayesianOptimizer...")
    optimizer = FewShotBayesianOptimizer(
        model="openai/gpt-4o-mini",
        min_examples=2,
        max_examples=4,
        n_threads=2,
        seed=42,
    )
    print("✓ Optimizer ready\n")
    
    # Step 5: Run optimization
    print("STEP 5: Running optimization...")
    print("-" * 40)
    print("This will:")
    print("  1. Evaluate baseline prompt")
    print("  2. Try different few-shot examples")
    print("  3. Find the best combination")
    print("-" * 40)
    print("\n🚀 Starting optimization (this may take 1-2 minutes)...\n")
    
    try:
        result = optimizer.optimize_prompt(
            prompt=initial_prompt,
            dataset=dataset,
            metric=similarity_metric,
            n_samples=5,
            n_trials=2,
        )
        
        # Display results
        print("\n" + "=" * 60)
        print("   OPTIMIZATION COMPLETE!")
        print("=" * 60)
        
        result.display()
        
        print("\n✅ Done! Check the Opik dashboard for detailed results.")
        
    except Exception as e:
        print(f"\n❌ Optimization error: {e}")
        print("\nThis might be due to:")
        print("  - Invalid API key")
        print("  - Rate limiting")
        print("  - Network issues")


if __name__ == "__main__":
    main()

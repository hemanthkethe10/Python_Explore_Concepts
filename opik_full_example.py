"""
Opik Full Prompt Optimization with Comet ML Cloud
==================================================

This example uses the full Opik optimizer with cloud tracking.

Prerequisites:
1. OpenAI API key (for LLM calls)
2. Comet ML API key (for Opik tracking) - Get free at: https://www.comet.com/signup

Setup:
    export OPENAI_API_KEY='sk-...'
    export COMET_API_KEY='your-comet-api-key'
    
Or run: opik configure
"""

import os
import sys

def check_api_keys():
    """Check if required API keys are set."""
    openai_key = os.environ.get("OPENAI_API_KEY")
    comet_key = os.environ.get("COMET_API_KEY")
    
    print("\n" + "=" * 60)
    print("   API KEY STATUS")
    print("=" * 60)
    
    if openai_key:
        print(f"✓ OPENAI_API_KEY: {openai_key[:15]}...")
    else:
        print("✗ OPENAI_API_KEY: NOT SET")
        print("  Get one at: https://platform.openai.com/api-keys")
    
    if comet_key:
        print(f"✓ COMET_API_KEY: {comet_key[:15]}...")
    else:
        print("✗ COMET_API_KEY: NOT SET")
        print("  Get one FREE at: https://www.comet.com/signup")
    
    print("=" * 60 + "\n")
    
    return openai_key and comet_key


def run_full_optimization():
    """Run the full Opik optimization with cloud tracking."""
    
    import opik
    from opik.evaluation.metrics import LevenshteinRatio
    from opik_optimizer import FewShotBayesianOptimizer, ChatPrompt
    
    print("\n" + "=" * 60)
    print("   OPIK FULL OPTIMIZATION WITH CLOUD TRACKING")
    print("=" * 60 + "\n")
    
    # Step 1: Initialize Opik client
    print("STEP 1: Connecting to Opik Cloud...")
    client = opik.Opik()
    print("✓ Connected to Opik Cloud\n")
    
    # Step 2: Create dataset
    print("STEP 2: Creating evaluation dataset...")
    dataset = client.get_or_create_dataset(
        name="qa_optimization_demo",
        description="Q&A pairs for prompt optimization demo"
    )
    
    # Add evaluation data
    dataset.insert([
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
        {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
        {"question": "What year did World War 2 end?", "answer": "1945"},
        {"question": "What is the chemical symbol for water?", "answer": "H2O"},
        {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
        {"question": "What is the capital of Japan?", "answer": "Tokyo"},
        {"question": "How many continents are there?", "answer": "7"},
        {"question": "What is the speed of light in m/s?", "answer": "299,792,458"},
    ])
    print(f"✓ Dataset created with {len(dataset)} items\n")
    
    # Step 3: Define initial prompt
    print("STEP 3: Defining initial prompt...")
    initial_prompt = ChatPrompt(
        messages=[
            {"role": "system", "content": "Answer questions accurately and concisely."},
            {"role": "user", "content": "{question}"}
        ]
    )
    print("✓ Initial prompt defined\n")
    print("  System: 'Answer questions accurately and concisely.'")
    print("  User: '{question}'\n")
    
    # Step 4: Define evaluation metric
    print("STEP 4: Setting up evaluation metric...")
    
    def similarity_metric(dataset_item, llm_output):
        """
        Levenshtein ratio measures string similarity.
        1.0 = exact match, 0.0 = completely different
        """
        metric = LevenshteinRatio()
        return metric.score(
            reference=dataset_item["answer"], 
            output=llm_output
        )
    
    print("✓ Using LevenshteinRatio for evaluation")
    print("  (Measures how similar the output is to expected answer)\n")
    
    # Step 5: Initialize optimizer
    print("STEP 5: Initializing FewShotBayesianOptimizer...")
    optimizer = FewShotBayesianOptimizer(
        model="openai/gpt-4o-mini",  # LiteLLM model name
        min_examples=2,              # Minimum few-shot examples to try
        max_examples=5,              # Maximum few-shot examples to try
        n_threads=4,                 # Parallel evaluation threads
        seed=42,                     # For reproducibility
        verbose=1,                   # Show progress
    )
    print("✓ Optimizer configured:")
    print("  - Model: gpt-4o-mini")
    print("  - Few-shot examples: 2-5")
    print("  - Threads: 4\n")
    
    # Step 6: Evaluate baseline
    print("STEP 6: Evaluating baseline prompt...")
    baseline_score = optimizer.evaluate_prompt(
        prompt=initial_prompt,
        dataset=dataset,
        metric=similarity_metric,
        n_samples=5,
        n_threads=4,
    )
    print(f"\n📊 BASELINE SCORE: {baseline_score:.2%}\n")
    
    # Step 7: Run optimization
    print("=" * 60)
    print("STEP 7: Running Bayesian Optimization...")
    print("=" * 60)
    print("\nThis will:")
    print("  1. Bootstrap few-shot example candidates")
    print("  2. Use Bayesian optimization to find best combination")
    print("  3. Evaluate each trial against the dataset")
    print("\n🚀 Starting optimization (this may take 2-5 minutes)...\n")
    
    result = optimizer.optimize_prompt(
        prompt=initial_prompt,
        dataset=dataset,
        metric=similarity_metric,
        n_samples=5,               # Samples per trial
        n_trials=3,                # Number of optimization trials
        project_name="prompt-optimization-demo",  # Comet project name
    )
    
    # Step 8: Display results
    print("\n" + "=" * 60)
    print("   OPTIMIZATION COMPLETE!")
    print("=" * 60 + "\n")
    
    # Show the optimized prompt
    print("OPTIMIZED PROMPT:")
    print("-" * 40)
    result.display()
    print("-" * 40)
    
    # Get improvement stats
    final_score = result.score if hasattr(result, 'score') else 0
    improvement = ((final_score - baseline_score) / baseline_score * 100) if baseline_score > 0 else 0
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"  Baseline Score:  {baseline_score:.2%}")
    print(f"  Optimized Score: {final_score:.2%}")
    print(f"  Improvement:     {improvement:+.1f}%")
    
    print("\n🌐 VIEW DETAILED RESULTS:")
    print("  Visit https://www.comet.com/opik to see:")
    print("  - All optimization trials")
    print("  - Score progression over time")
    print("  - Best performing prompt variations")
    print("  - Dataset evaluation details")
    
    return result


def main():
    print("\n" + "🔧" * 30)
    print("\n   OPIK FULL OPTIMIZATION DEMO")
    print("\n" + "🔧" * 30)
    
    # Check API keys
    if not check_api_keys():
        print("\n⚠️  Missing API keys!")
        print("\nTo get a FREE Comet ML API key:")
        print("  1. Go to: https://www.comet.com/signup")
        print("  2. Create a free account")
        print("  3. Go to Settings > API Keys")
        print("  4. Copy your API key")
        print("\nThen run:")
        print("  export COMET_API_KEY='your-key-here'")
        print("  python3 opik_full_example.py")
        print("\nOr use the Opik CLI:")
        print("  opik configure")
        return
    
    try:
        run_full_optimization()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

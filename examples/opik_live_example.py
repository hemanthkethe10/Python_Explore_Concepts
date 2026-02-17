"""
Opik Agent Optimization - Live Example
=======================================

This is a working example that demonstrates how Opik optimizes prompts
using real datasets and evaluation metrics.

Prerequisites:
--------------
1. Install required packages:
   pip install opik opik-optimizer openai

2. Set your OpenAI API key:
   export OPENAI_API_KEY="your-api-key"

3. (Optional) Set Comet ML API key for logging:
   export COMET_API_KEY="your-comet-api-key"

How It Works:
-------------
1. Start with an initial prompt & eval dataset
2. Let the optimizer iteratively improve the prompt
3. Get the optimal prompt automatically!

The optimizer uses Bayesian optimization to:
- Test different prompt variations
- Select optimal few-shot examples
- Measure performance against your metric
- Converge on the best performing prompt
"""

import os
from typing import Dict, Any

# Check for API key
if not os.environ.get("OPENAI_API_KEY"):
    print("⚠️  WARNING: OPENAI_API_KEY not set. Set it with:")
    print("   export OPENAI_API_KEY='your-api-key'")
    print()


def example_1_basic_optimization():
    """
    Example 1: Basic Prompt Optimization
    
    This example shows the fundamental workflow:
    - Create a dataset with question/answer pairs
    - Define a metric to measure quality
    - Let Opik find the optimal prompt
    """
    import opik
    from opik.evaluation.metrics import LevenshteinRatio
    from opik_optimizer import FewShotBayesianOptimizer, ChatPrompt
    
    print("=" * 60)
    print("EXAMPLE 1: Basic Prompt Optimization")
    print("=" * 60)
    
    # Step 1: Create an Opik client and dataset
    client = opik.Opik()
    
    dataset = client.get_or_create_dataset(
        name="qa_optimization_dataset",
        description="Question-answer pairs for prompt optimization"
    )
    
    # Step 2: Add evaluation data (input/expected output pairs)
    dataset.insert([
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
        {"question": "What is the largest planet?", "answer": "Jupiter"},
        {"question": "What year did World War 2 end?", "answer": "1945"},
        {"question": "What is the chemical symbol for water?", "answer": "H2O"},
        {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
        {"question": "What is the speed of light?", "answer": "299,792,458 meters per second"},
        {"question": "What is the capital of Japan?", "answer": "Tokyo"},
        {"question": "How many continents are there?", "answer": "7"},
    ])
    
    print(f"✓ Created dataset with {len(dataset)} items")
    
    # Step 3: Define the initial prompt
    initial_prompt = ChatPrompt(
        messages=[
            {"role": "system", "content": "Answer questions accurately."},
            {"role": "user", "content": "{question}"}
        ]
    )
    
    print(f"✓ Initial prompt: '{initial_prompt.messages[0]['content']}'")
    
    # Step 4: Define the evaluation metric
    def levenshtein_ratio(dataset_item: Dict, llm_output: str) -> float:
        """
        Measures how similar the LLM output is to the expected answer.
        Score ranges from 0 (completely different) to 1 (exact match).
        """
        metric = LevenshteinRatio()
        result = metric.score(reference=dataset_item["answer"], output=llm_output)
        return result
    
    # Step 5: Create the optimizer
    optimizer = FewShotBayesianOptimizer(
        model="openai/gpt-4o-mini",  # LiteLLM model name
        min_examples=2,              # Minimum few-shot examples
        max_examples=5,              # Maximum few-shot examples
        n_threads=4,                 # Parallel evaluation threads
        seed=42,                     # For reproducibility
    )
    
    print("✓ Optimizer configured")
    print("\n🚀 Starting optimization...\n")
    
    # Step 6: Run the optimization!
    result = optimizer.optimize_prompt(
        prompt=initial_prompt,
        dataset=dataset,
        metric=levenshtein_ratio,
        n_samples=10,    # Number of samples per trial
        n_trials=3,      # Number of optimization trials
    )
    
    # Step 7: Display results
    print("\n" + "=" * 60)
    print("OPTIMIZATION RESULTS")
    print("=" * 60)
    result.display()
    
    return result


def example_2_custom_metric():
    """
    Example 2: Custom Evaluation Metric
    
    Shows how to define your own metric for specific use cases.
    Here we optimize for concise responses.
    """
    import opik
    from opik.evaluation.metrics import score_result
    from opik_optimizer import MetaPromptOptimizer, ChatPrompt
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Custom Metric Optimization")
    print("=" * 60)
    
    client = opik.Opik()
    
    dataset = client.get_or_create_dataset(
        name="concise_response_dataset",
        description="Dataset for testing response conciseness"
    )
    
    dataset.insert([
        {"question": "What is Python?", "max_words": 20},
        {"question": "Explain REST APIs", "max_words": 30},
        {"question": "What is machine learning?", "max_words": 25},
        {"question": "Define a database", "max_words": 15},
        {"question": "What is an API?", "max_words": 20},
    ])
    
    # Custom metric: Rewards concise, accurate responses
    def conciseness_score(dataset_item: Dict, llm_output: str):
        """
        Custom metric that scores based on:
        - Brevity (shorter is better, up to a point)
        - Completeness (must have substance)
        """
        word_count = len(llm_output.split())
        max_words = dataset_item.get("max_words", 50)
        
        # Score calculation
        if word_count == 0:
            score = 0.0
            reason = "Empty response"
        elif word_count <= max_words:
            score = 1.0
            reason = f"Concise response ({word_count} words)"
        elif word_count <= max_words * 2:
            score = 0.5
            reason = f"Slightly verbose ({word_count} words)"
        else:
            score = 0.2
            reason = f"Too verbose ({word_count} words)"
        
        return score_result.ScoreResult(
            name="conciseness",
            value=score,
            reason=reason
        )
    
    initial_prompt = ChatPrompt(
        messages=[
            {"role": "system", "content": "You are an assistant. Answer questions."},
            {"role": "user", "content": "{question}"}
        ]
    )
    
    # MetaPromptOptimizer modifies the system prompt itself
    optimizer = MetaPromptOptimizer(
        model="openai/gpt-4o-mini",
    )
    
    print("✓ Using MetaPromptOptimizer (modifies system prompt)")
    print("\n🚀 Starting optimization...\n")
    
    result = optimizer.optimize_prompt(
        prompt=initial_prompt,
        dataset=dataset,
        metric=conciseness_score,
        n_samples=5,
    )
    
    print("\n" + "=" * 60)
    print("OPTIMIZATION RESULTS")
    print("=" * 60)
    result.display()
    
    return result


def example_3_hierarchical_optimizer():
    """
    Example 3: HierarchicalReflectiveOptimizer
    
    The most sophisticated optimizer that:
    - Analyzes failures deeply
    - Generates targeted improvements
    - Uses reflection to understand why prompts fail
    """
    import opik
    from opik.evaluation.metrics import score_result
    from opik_optimizer import HierarchicalReflectiveOptimizer, ChatPrompt
    
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Hierarchical Reflective Optimization")
    print("=" * 60)
    
    client = opik.Opik()
    
    dataset = client.get_or_create_dataset(
        name="format_optimization_dataset",
        description="Dataset for testing response formatting"
    )
    
    # Dataset where we want specific formatted responses
    dataset.insert([
        {"question": "List 3 programming languages", "expected_format": "numbered_list"},
        {"question": "Name 3 countries in Europe", "expected_format": "numbered_list"},
        {"question": "What are 3 types of databases?", "expected_format": "numbered_list"},
    ])
    
    def format_score(dataset_item: Dict, llm_output: str):
        """Scores based on whether output matches expected format."""
        expected = dataset_item.get("expected_format", "")
        
        if expected == "numbered_list":
            # Check if output contains numbered items (1., 2., 3.)
            has_numbers = any(f"{i}." in llm_output for i in range(1, 4))
            if has_numbers:
                return score_result.ScoreResult(
                    name="format", value=1.0, reason="Correct numbered list format"
                )
            else:
                return score_result.ScoreResult(
                    name="format", value=0.3, reason="Missing numbered list format"
                )
        
        return score_result.ScoreResult(name="format", value=0.5, reason="Unknown format")
    
    initial_prompt = ChatPrompt(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "{question}"}
        ]
    )
    
    optimizer = HierarchicalReflectiveOptimizer(
        model="openai/gpt-4o-mini",
    )
    
    print("✓ Using HierarchicalReflectiveOptimizer")
    print("  This optimizer analyzes failures and reflects on improvements")
    print("\n🚀 Starting optimization...\n")
    
    result = optimizer.optimize_prompt(
        prompt=initial_prompt,
        dataset=dataset,
        metric=format_score,
        max_trials=2,
    )
    
    print("\n" + "=" * 60)
    print("OPTIMIZATION RESULTS")
    print("=" * 60)
    result.display()
    
    return result


def explain_optimization_process():
    """
    Explains how Opik improves prompts step by step.
    """
    explanation = """
╔══════════════════════════════════════════════════════════════════════╗
║          HOW OPIK IMPROVES YOUR PROMPTS - STEP BY STEP              ║
╚══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: BASELINE EVALUATION                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Your Initial Prompt:                                               │
│  ┌─────────────────────────────────────────────────┐               │
│  │ "You are a helpful assistant. Answer questions." │               │
│  └─────────────────────────────────────────────────┘               │
│                                                                     │
│  Tested against your dataset (e.g., 100 Q&A pairs)                 │
│  Baseline Score: 62%                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: BOOTSTRAP FEW-SHOT EXAMPLES                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  The optimizer selects examples from your dataset that              │
│  demonstrate the ideal input → output behavior:                     │
│                                                                     │
│  Example 1: Q: "What is 2+2?"  →  A: "4"                           │
│  Example 2: Q: "Capital of France?"  →  A: "Paris"                 │
│  Example 3: Q: "Who wrote Hamlet?"  →  A: "William Shakespeare"    │
│                                                                     │
│  These become few-shot examples in the prompt!                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: BAYESIAN OPTIMIZATION                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Trial 1: Test with 3 examples → Score: 71%                        │
│  Trial 2: Test with 5 examples → Score: 78%                        │
│  Trial 3: Test different examples → Score: 82%                     │
│  Trial 4: Optimize example selection → Score: 85%                  │
│  Trial 5: Fine-tune combination → Score: 88%                       │
│                                                                     │
│  Bayesian optimization efficiently explores the space              │
│  of possible prompts to find the best configuration.               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: FINAL OPTIMIZED PROMPT                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ SYSTEM: You are a helpful assistant. Answer questions       │   │
│  │ accurately and concisely.                                   │   │
│  │                                                             │   │
│  │ Here are some examples:                                     │   │
│  │                                                             │   │
│  │ Q: What is 2+2?                                            │   │
│  │ A: 4                                                        │   │
│  │                                                             │   │
│  │ Q: What is the capital of France?                          │   │
│  │ A: Paris                                                    │   │
│  │                                                             │   │
│  │ Q: Who wrote Romeo and Juliet?                             │   │
│  │ A: William Shakespeare                                      │   │
│  │                                                             │   │
│  │ Now answer the following:                                   │   │
│  │ Q: {user_question}                                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Final Score: 88% (improved from 62%)                              │
│  Improvement: +26 percentage points! 🎉                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║                    WHY THIS WORKS                                    ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. DATA-DRIVEN: Uses your actual examples to learn what works      ║
║                                                                      ║
║  2. OBJECTIVE METRICS: Removes guesswork with measurable scores     ║
║                                                                      ║
║  3. FEW-SHOT LEARNING: Shows the model exactly what you expect      ║
║                                                                      ║
║  4. BAYESIAN SEARCH: Efficiently explores prompt variations         ║
║                                                                      ║
║  5. ITERATIVE REFINEMENT: Small improvements compound over trials   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
    print(explanation)


def main():
    """Main function to run examples."""
    print("\n" + "🔧" * 30)
    print("\n   OPIK AGENT OPTIMIZATION - LIVE EXAMPLES")
    print("\n" + "🔧" * 30 + "\n")
    
    # First, explain how it works
    explain_optimization_process()
    
    # Check if API key is available
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n" + "=" * 60)
        print("⚠️  DEMO MODE - No API key detected")
        print("=" * 60)
        print("\nTo run the live examples, set your OpenAI API key:")
        print("\n  export OPENAI_API_KEY='sk-...'")
        print("\nThen run this script again!")
        print("\nThe examples above show exactly what would happen.")
        return
    
    # Ask user which example to run
    print("\n" + "=" * 60)
    print("SELECT AN EXAMPLE TO RUN:")
    print("=" * 60)
    print("\n1. Basic Optimization (FewShotBayesianOptimizer)")
    print("   - Best for: Adding few-shot examples to improve accuracy")
    print("\n2. Custom Metric Optimization (MetaPromptOptimizer)")
    print("   - Best for: Optimizing for specific behaviors (conciseness, format, etc.)")
    print("\n3. Hierarchical Reflective Optimization")
    print("   - Best for: Complex tasks needing deep analysis")
    print("\n4. Run all examples")
    print("\n0. Exit")
    
    try:
        choice = input("\nEnter your choice (0-4): ").strip()
        
        if choice == "1":
            example_1_basic_optimization()
        elif choice == "2":
            example_2_custom_metric()
        elif choice == "3":
            example_3_hierarchical_optimizer()
        elif choice == "4":
            example_1_basic_optimization()
            example_2_custom_metric()
            example_3_hierarchical_optimizer()
        elif choice == "0":
            print("\nGoodbye! 👋")
        else:
            print("\nInvalid choice. Running Example 1 by default...")
            example_1_basic_optimization()
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have installed the required packages:")
        print("  pip install opik opik-optimizer openai")


if __name__ == "__main__":
    main()

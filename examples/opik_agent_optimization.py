"""
Opik Agent Optimization Toolkit
================================

A toolkit for automatic prompt optimization using evaluation datasets.

Workflow Overview:
------------------
1. Start with an initial prompt & eval dataset
2. Let the optimizer iteratively improve the prompt
3. Get the optimal prompt automatically!

Inputs:
-------
- Eval dataset: A collection of test cases to evaluate prompt performance
- Evaluation criteria: Metrics and rules for measuring prompt quality
- Initial prompt: The starting prompt to be optimized

Outputs:
--------
- Optimization report: Detailed analysis of the optimization process
- Improved prompt: The optimized version of the initial prompt

Reference: https://twitter.com/akshay_pachaar (Dec 2, 2024)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class EvalDataset:
    """Represents the evaluation dataset for prompt optimization."""
    name: str
    test_cases: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_test_case(self, input_data: str, expected_output: str, metadata: Optional[Dict] = None):
        """Add a test case to the evaluation dataset."""
        test_case = {
            "input": input_data,
            "expected_output": expected_output,
            "metadata": metadata or {}
        }
        self.test_cases.append(test_case)
        return self
    
    def __len__(self):
        return len(self.test_cases)


@dataclass
class EvaluationCriteria:
    """Defines the criteria for evaluating prompt performance."""
    name: str
    metrics: List[str] = field(default_factory=list)
    scoring_rules: Dict[str, Any] = field(default_factory=dict)
    
    def add_metric(self, metric_name: str, weight: float = 1.0):
        """Add an evaluation metric."""
        self.metrics.append(metric_name)
        self.scoring_rules[metric_name] = {"weight": weight}
        return self


@dataclass
class OptimizationReport:
    """Contains the results and analysis of the optimization process."""
    iterations: int = 0
    initial_score: float = 0.0
    final_score: float = 0.0
    improvement_percentage: float = 0.0
    iteration_history: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        """Generate a summary of the optimization report."""
        return f"""
Optimization Report Summary
===========================
Total Iterations: {self.iterations}
Initial Score: {self.initial_score:.2f}
Final Score: {self.final_score:.2f}
Improvement: {self.improvement_percentage:.1f}%
Recommendations: {len(self.recommendations)}
"""


class AgentOptimizationToolkit:
    """
    Main class for the Agent Optimization Toolkit.
    
    Uses Opik to iteratively improve prompts based on evaluation datasets
    and defined criteria.
    """
    
    def __init__(self, initial_prompt: str):
        self.initial_prompt = initial_prompt
        self.improved_prompt = initial_prompt
        self.eval_dataset: Optional[EvalDataset] = None
        self.evaluation_criteria: Optional[EvaluationCriteria] = None
        self.report: Optional[OptimizationReport] = None
    
    def set_eval_dataset(self, dataset: EvalDataset) -> "AgentOptimizationToolkit":
        """Set the evaluation dataset."""
        self.eval_dataset = dataset
        return self
    
    def set_evaluation_criteria(self, criteria: EvaluationCriteria) -> "AgentOptimizationToolkit":
        """Set the evaluation criteria."""
        self.evaluation_criteria = criteria
        return self
    
    def optimize(self, max_iterations: int = 10) -> "AgentOptimizationToolkit":
        """
        Run the optimization process.
        
        This is a placeholder implementation. In practice, this would:
        1. Evaluate the current prompt against the eval dataset
        2. Use Opik to suggest improvements
        3. Iterate until convergence or max_iterations reached
        """
        if not self.eval_dataset:
            raise ValueError("Evaluation dataset must be set before optimization")
        if not self.evaluation_criteria:
            raise ValueError("Evaluation criteria must be set before optimization")
        
        # Initialize report
        self.report = OptimizationReport()
        self.report.initial_score = self._evaluate_prompt(self.initial_prompt)
        
        current_prompt = self.initial_prompt
        current_score = self.report.initial_score
        
        for i in range(max_iterations):
            # Placeholder for actual Opik optimization logic
            # In practice, this would call Opik's API
            improved = self._improve_prompt_iteration(current_prompt)
            new_score = self._evaluate_prompt(improved)
            
            self.report.iteration_history.append({
                "iteration": i + 1,
                "prompt": improved,
                "score": new_score,
                "improvement": new_score - current_score
            })
            
            if new_score > current_score:
                current_prompt = improved
                current_score = new_score
            
            # Check for convergence
            if i > 0 and abs(new_score - current_score) < 0.01:
                break
        
        self.improved_prompt = current_prompt
        self.report.final_score = current_score
        self.report.iterations = len(self.report.iteration_history)
        self.report.improvement_percentage = (
            (self.report.final_score - self.report.initial_score) 
            / self.report.initial_score * 100
            if self.report.initial_score > 0 else 0
        )
        
        return self
    
    def _evaluate_prompt(self, prompt: str) -> float:
        """
        Evaluate a prompt against the eval dataset.
        
        Placeholder implementation - returns a mock score.
        In practice, this would run the prompt through the eval cases.
        """
        # Mock evaluation score
        return 0.5 + len(prompt) % 10 / 20
    
    def _improve_prompt_iteration(self, prompt: str) -> str:
        """
        Generate an improved version of the prompt.
        
        Placeholder implementation.
        In practice, this would use Opik's optimization algorithms.
        """
        # Mock improvement - in practice, use Opik
        return prompt + " [optimized]"
    
    def get_improved_prompt(self) -> str:
        """Return the optimized prompt."""
        return self.improved_prompt
    
    def get_optimization_report(self) -> OptimizationReport:
        """Return the optimization report."""
        if not self.report:
            raise ValueError("Optimization must be run first")
        return self.report


def example_usage():
    """
    Example usage of the Agent Optimization Toolkit.
    """
    # 1. Define your initial prompt
    initial_prompt = """
    You are a helpful assistant. Answer the user's questions 
    accurately and concisely.
    """
    
    # 2. Create an evaluation dataset
    eval_dataset = EvalDataset(name="customer_support_eval")
    eval_dataset.add_test_case(
        input_data="What are your business hours?",
        expected_output="Our business hours are Monday-Friday, 9 AM to 5 PM."
    )
    eval_dataset.add_test_case(
        input_data="How do I reset my password?",
        expected_output="Go to Settings > Security > Reset Password."
    )
    
    # 3. Define evaluation criteria
    criteria = EvaluationCriteria(name="quality_metrics")
    criteria.add_metric("accuracy", weight=0.4)
    criteria.add_metric("relevance", weight=0.3)
    criteria.add_metric("conciseness", weight=0.2)
    criteria.add_metric("tone", weight=0.1)
    
    # 4. Initialize and run the optimizer
    toolkit = AgentOptimizationToolkit(initial_prompt)
    toolkit.set_eval_dataset(eval_dataset)
    toolkit.set_evaluation_criteria(criteria)
    toolkit.optimize(max_iterations=5)
    
    # 5. Get results
    improved_prompt = toolkit.get_improved_prompt()
    report = toolkit.get_optimization_report()
    
    print("=" * 50)
    print("AGENT OPTIMIZATION TOOLKIT - RESULTS")
    print("=" * 50)
    print(f"\nInitial Prompt:\n{initial_prompt}")
    print(f"\nImproved Prompt:\n{improved_prompt}")
    print(report.summary())


if __name__ == "__main__":
    example_usage()

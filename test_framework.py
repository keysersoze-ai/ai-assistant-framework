#!/usr/bin/env python3
"""
Quick tests for the AI Assistant Framework
Run with: python test_framework.py
"""

import asyncio
from main import AIAssistant, MemorySystem, ReasoningEngine
import time

async def test_memory_persistence():
    """Test that memories persist across queries"""
    print("Testing memory persistence...")
    
    assistant = AIAssistant()
    
    # First query
    await assistant.process("Python is a great language")
    
    # Related query should find context
    result = await assistant.process("Tell me about Python")
    
    assert result["context_used"] > 0, "Should have found relevant context"
    print("✓ Memory persistence working")

async def test_reasoning_strategies():
    """Test different reasoning strategies"""
    print("\nTesting reasoning strategies...")
    
    strategies = ["chain_of_thought", "tree_of_thought", "basic"]
    
    for strategy in strategies:
        assistant = AIAssistant(
            reasoning=ReasoningEngine(strategy=strategy)
        )
        result = await assistant.process("Complex query")
        assert result["confidence"] > 0, f"Strategy {strategy} failed"
        print(f"✓ {strategy} strategy working")

async def stress_test():
    """Basic stress test"""
    print("\nRunning stress test...")
    
    assistant = AIAssistant()
    start = time.time()
    
    queries = ["Query " + str(i) for i in range(100)]
    
    for q in queries:
        await assistant.process(q)
    
    elapsed = time.time() - start
    print(f"✓ Processed 100 queries in {elapsed:.2f} seconds")
    print(f"  Average: {elapsed/100*1000:.2f}ms per query")

async def main():
    print("="*50)
    print("AI Assistant Framework - Test Suite")
    print("="*50)
    
    await test_memory_persistence()
    await test_reasoning_strategies()
    await stress_test()
    
    print("\n" + "="*50)
    print("All tests passed! 🎉")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
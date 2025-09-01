#!/usr/bin/env python3
"""
AI Assistant Framework - Main Entry Point
A modular, extensible AI assistant with advanced reasoning capabilities
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Represents a message in the conversation"""
    content: str
    role: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class MemorySystem:
    """Handles persistent memory and context management"""
    
    def __init__(self, max_context_size: int = 10000):
        self.memories: List[Message] = []
        self.max_context_size = max_context_size
        self.importance_scores: Dict[str, float] = {}
        
    def add_memory(self, message: Message, importance: float = 1.0):
        """Add a new memory with importance scoring"""
        self.memories.append(message)
        self.importance_scores[id(message)] = importance
        self._optimize_memory()
        
    def _optimize_memory(self):
        """Optimize memory storage based on importance and recency"""
        if len(self.memories) > self.max_context_size:
            # Keep most important and recent memories
            sorted_memories = sorted(
                self.memories,
                key=lambda m: self.importance_scores.get(id(m), 1.0) * 
                             (1.0 / (datetime.now() - m.timestamp).total_seconds()),
                reverse=True
            )
            self.memories = sorted_memories[:self.max_context_size]
    
    def get_relevant_context(self, query: str, limit: int = 5) -> List[Message]:
        """Retrieve relevant memories for the given query"""
        # Simple relevance scoring based on content overlap
        relevant = []
        query_words = set(query.lower().split())
        
        for memory in self.memories:
            memory_words = set(memory.content.lower().split())
            overlap = len(query_words.intersection(memory_words))
            if overlap > 0:
                relevant.append((overlap, memory))
        
        relevant.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in relevant[:limit]]


class ReasoningEngine:
    """Advanced reasoning and decision-making engine"""
    
    def __init__(self, strategy: str = "chain_of_thought"):
        self.strategy = strategy
        self.reasoning_chain: List[str] = []
        
    async def reason(self, query: str, context: List[Message]) -> Dict[str, Any]:
        """Apply reasoning strategy to generate response"""
        self.reasoning_chain = []
        
        if self.strategy == "chain_of_thought":
            return await self._chain_of_thought(query, context)
        elif self.strategy == "tree_of_thought":
            return await self._tree_of_thought(query, context)
        else:
            return await self._basic_reasoning(query, context)
    
    async def _chain_of_thought(self, query: str, context: List[Message]) -> Dict[str, Any]:
        """Implement chain-of-thought reasoning"""
        steps = [
            "Understanding the query",
            "Identifying key concepts",
            "Retrieving relevant information",
            "Synthesizing response",
            "Validating conclusions"
        ]
        
        for step in steps:
            self.reasoning_chain.append(f"{step}: Processing '{query}'")
            await asyncio.sleep(0.1)  # Simulate processing
        
        return {
            "response": f"Based on chain-of-thought analysis: {query}",
            "reasoning": self.reasoning_chain,
            "confidence": 0.85
        }
    
    async def _tree_of_thought(self, query: str, context: List[Message]) -> Dict[str, Any]:
        """Implement tree-of-thought exploration"""
        branches = [
            "Exploring possibility A",
            "Exploring possibility B",
            "Evaluating trade-offs",
            "Selecting optimal path"
        ]
        
        for branch in branches:
            self.reasoning_chain.append(f"{branch}: Analyzing '{query}'")
            await asyncio.sleep(0.1)
        
        return {
            "response": f"After exploring multiple paths: {query}",
            "reasoning": self.reasoning_chain,
            "confidence": 0.90
        }
    
    async def _basic_reasoning(self, query: str, context: List[Message]) -> Dict[str, Any]:
        """Basic reasoning fallback"""
        return {
            "response": f"Processing: {query}",
            "reasoning": ["Direct processing"],
            "confidence": 0.70
        }


class AIAssistant:
    """Main AI Assistant class coordinating all components"""
    
    def __init__(self, memory: Optional[MemorySystem] = None, 
                 reasoning: Optional[ReasoningEngine] = None):
        self.memory = memory or MemorySystem()
        self.reasoning = reasoning or ReasoningEngine()
        self.session_start = datetime.now()
        logger.info("AI Assistant initialized")
    
    async def process(self, query: str) -> Dict[str, Any]:
        """Process a query through the full pipeline"""
        logger.info(f"Processing query: {query}")
        
        # Create message
        message = Message(
            content=query,
            role="user",
            timestamp=datetime.now()
        )
        
        # Add to memory
        self.memory.add_memory(message, importance=1.0)
        
        # Get relevant context
        context = self.memory.get_relevant_context(query)
        
        # Apply reasoning
        result = await self.reasoning.reason(query, context)
        
        # Store assistant response
        response_message = Message(
            content=result["response"],
            role="assistant",
            timestamp=datetime.now(),
            metadata={"confidence": result["confidence"]}
        )
        self.memory.add_memory(response_message, importance=result["confidence"])
        
        logger.info(f"Generated response with confidence: {result['confidence']}")
        
        return {
            "query": query,
            "response": result["response"],
            "reasoning": result["reasoning"],
            "confidence": result["confidence"],
            "context_used": len(context),
            "session_duration": (datetime.now() - self.session_start).total_seconds()
        }
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about the current session"""
        return {
            "total_memories": len(self.memory.memories),
            "session_duration": (datetime.now() - self.session_start).total_seconds(),
            "reasoning_strategy": self.reasoning.strategy,
            "memory_usage": len(self.memory.memories) / self.memory.max_context_size
        }


async def main():
    """Example usage of the AI Assistant Framework"""
    print("🤖 AI Assistant Framework v1.0")
    print("=" * 50)
    
    # Initialize assistant with advanced configuration
    assistant = AIAssistant(
        memory=MemorySystem(max_context_size=1000),
        reasoning=ReasoningEngine(strategy="chain_of_thought")
    )
    
    # Example queries
    queries = [
        "What are the key principles of distributed systems?",
        "How does memory management work in modern operating systems?",
        "Explain the trade-offs between SQL and NoSQL databases"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        result = await assistant.process(query)
        
        print(f"💭 Response: {result['response']}")
        print(f"🎯 Confidence: {result['confidence']:.2%}")
        print(f"🧠 Reasoning steps: {len(result['reasoning'])}")
        print("-" * 50)
    
    # Display session statistics
    stats = assistant.get_session_stats()
    print("\n📊 Session Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
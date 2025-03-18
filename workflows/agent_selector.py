from temporalio import workflow
from typing import Dict, Any, Optional
import json
import re

from tools.goal_registry import (
    goal_match_train_invoice, 
    goal_event_flight_invoice, 
    music_creation_goal, 
    json_array_creation_goal,
    unified_agent_goal
)
from models.tool_definitions import AgentGoal


@workflow.defn
class AgentSelectorWorkflow:
    """
    A workflow that selects the appropriate agent goal based on user intent.
    This allows dynamically switching between different agent goals during a conversation.
    """
    
    @workflow.run
    async def run(self, conversation_history: str) -> Dict[str, Any]:
        """
        Analyzes the conversation history to determine the most appropriate agent goal.
        
        Args:
            conversation_history: The conversation history as a string
            
        Returns:
            The selected agent goal as a dictionary
        """
        # Default to unified agent goal
        selected_goal = "unified_agent_goal"
        
        # Only select a specialized goal if explicitly requested
        if "only use music tool" in conversation_history.lower() or "only music" in conversation_history.lower():
            return {"selected_goal": "music_creation_goal"}
            
        if "only use json tool" in conversation_history.lower() or "only json" in conversation_history.lower():
            return {"selected_goal": "json_array_creation_goal"}
            
        if "only uk travel" in conversation_history.lower() or "only train booking" in conversation_history.lower():
            return {"selected_goal": "goal_match_train_invoice"}
            
        if "only oceania events" in conversation_history.lower() or "only event booking" in conversation_history.lower():
            return {"selected_goal": "goal_event_flight_invoice"}
            
        # Otherwise, use the unified agent that can handle all tool types
        return {"selected_goal": selected_goal} 
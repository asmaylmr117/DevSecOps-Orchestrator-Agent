from typing import TypedDict, List, Dict, Optional, Any

class DevSecOpsState(TypedDict):
    """
    Represents the current system state of the DevSecOps module in LangGraph.
    """
        
    sarif_input: List[Dict] 
       
    commit_id: str 
       
    final_priority_score: Optional[float]  
    
    jira_ticket_id: Optional[str] 
    
    remediation_status: str 
    
    messages: List[str]
    
    # New field for Router - stores routing decision
    routing_decision: Optional[str]


INITIAL_STATE: DevSecOpsState = {
    "sarif_input": [],
    "commit_id": "",
    "final_priority_score": None,
    "jira_ticket_id": None,
    "remediation_status": "START_PROCESSING",
    "messages": ["DevSecOps Orchestrator workflow initialized."],
    "routing_decision": None
}
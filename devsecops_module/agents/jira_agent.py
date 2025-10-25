from typing import Dict, Any
from ..state_schema import DevSecOpsState
import uuid
import requests 

def create_jira_ticket(final_score: float) -> str:
    """Simulate ticket creation via external API."""
    
   
    if final_score >= 8.5:
       
        ticket_id = f"JIRA-{uuid.uuid4().hex[:6].upper()}"
        
        return ticket_id
    else:
        return "SKIPPED"

def create_ticket_node(state: DevSecOpsState) -> Dict[str, Any]:
    """Node (3): Integrates with Jira/Azure DevOps to create a work ticket."""
    
    final_score = state.get("final_priority_score", 0.0)
    
    if final_score is None or final_score < 1.0:
        return {"remediation_status": "SKIPPED", "messages": ["Ticketing skipped: Low score or error."]}

    jira_id = create_jira_ticket(final_score)
    
    new_status = "TICKET_CREATED" if jira_id != "SKIPPED" else "ACTION_COMPLETE"
    
    print(f"[NODE 3/3] Jira Integration: Status is {new_status}")
    
    return {
        "jira_ticket_id": jira_id,
        "remediation_status": new_status,
        "messages": [f"Jira status: {new_status}"]
    }


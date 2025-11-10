from typing import Dict, Any
from ..state_schema import DevSecOpsState
import uuid
import requests 

def create_jira_ticket(final_score: float) -> str:
    """
    Simulate ticket creation via external API.
    
    Note: Decision logic (score >= 8.5) is now handled at graph level.
    This function assumes it's only called when score meets the threshold.
    
    Args:
        final_score: The calculated priority score
        
    Returns:
        str: Generated JIRA ticket ID
    """
    # Generate unique ticket ID
    ticket_id = f"JIRA-{uuid.uuid4().hex[:6].upper()}"
    
    print(f"[JIRA API] Creating ticket for score {final_score}: {ticket_id}")
    
    # TODO: Replace with actual JIRA API call
    # response = requests.post(
    #     "https://your-jira-instance.atlassian.net/rest/api/3/issue",
    #     headers={"Authorization": "Bearer YOUR_TOKEN"},
    #     json={
    #         "fields": {
    #             "project": {"key": "SEC"},
    #             "summary": f"Security Finding - Priority {final_score}",
    #             "issuetype": {"name": "Bug"}
    #         }
    #     }
    # )
    
    return ticket_id


def create_ticket_node(state: DevSecOpsState) -> Dict[str, Any]:
    """
    Node (3): Integrates with Jira/Azure DevOps to create a work ticket.
    
    This node is only reached when score >= 8.5 (decision handled at graph level).
    Creates a ticket and updates the state with ticket information.
    
    Args:
        state: Current DevSecOps state
        
    Returns:
        Dict: State updates including ticket ID and status
    """
    
    final_score = state.get("final_priority_score", 0.0)
    
    # Create ticket (no need to check score again - graph already filtered)
    jira_id = create_jira_ticket(final_score)
    
    print(f"[NODE 3/3] Jira Integration: Ticket created - {jira_id}")
    
    return {
        "jira_ticket_id": jira_id,
        "remediation_status": "TICKET_CREATED",
        "messages": state.get("messages", []) + [
            f"Jira ticket created: {jira_id} (Score: {final_score})"
        ]
    }

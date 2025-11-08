from typing import Dict, Any
from ..state_schema import DevSecOpsState

# CONTINUE_REMEDIATION: Specialist L3
ROUTER_PATHS = ["CONTINUE_REMEDIATION", "END_WORKFLOW"]

def router_node(state: DevSecOpsState) -> Dict[str, Any]:
    """
    Node (L2/Router): Receives ticket and decides the next path.
    This node updates the state with the routing decision.
    
    Returns:
        Dict: State updates including the next step decision
    """
    
    jira_id = state.get("jira_ticket_id")
    
    if jira_id and jira_id != "SKIPPED":
        # Ticket created: Move to L3 stage
        print("[NODE L2/ROUTER] Ticket created. Directing to L3 Remediation.")
        next_step = "CONTINUE_REMEDIATION"
    else:
        # No ticket (low risk): End the workflow
        print("[NODE L2/ROUTER] Low score or failed. Directing to END.")
        next_step = "END_WORKFLOW"
    
    return {
        "routing_decision": next_step,
        "messages": state.get("messages", []) + [f"Router: Decision made - {next_step}"]
    }


def route_after_router(state: DevSecOpsState) -> str:
    """
    Conditional edge function: Reads Router decision and routes to appropriate path.
    
    Returns:
        str: Next path name ("CONTINUE_REMEDIATION" or "END_WORKFLOW")
    """
    decision = state.get("routing_decision", "END_WORKFLOW")
    return decision
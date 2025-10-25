from typing import Dict, Any, List
from ..state_schema import DevSecOpsState

def apply_risk_scoring(findings: List[Dict], commit_id: str) -> float:
    """Risk Algorithm Application: (Severity * Context Factor)."""
    if not findings: return 0.0
    
    
    context_factor = 1.2 
    base_severity = findings[0].get('tool_severity', 0.0)
    
    
    final_score = base_severity * context_factor
    return round(final_score, 2)

def prioritization_node(state: DevSecOpsState) -> Dict[str, Any]:
    """Node (2): Apply the risk algorithm to determine the final priority."""
    
    findings = state.get("sarif_input", [])
    commit_id = state.get("commit_id", "N/A")
    
    if not findings:
        return {"remediation_status": "SKIPPED", "messages": ["Prioritization skipped: No findings."]}
        
    final_priority = apply_risk_scoring(findings, commit_id)
    
    print(f"[NODE 2/3] Prioritization: Score calculated: {final_priority}")
    
    return {
        "final_priority_score": final_priority,
        "remediation_status": "PRIORITIZED",
        "messages": [f"Final priority score: {final_priority}"]
    }
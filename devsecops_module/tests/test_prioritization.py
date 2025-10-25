import pytest
from devsecops_module.agents.prioritization_agent import apply_risk_scoring

from devsecops_module.state_schema import DevSecOpsState
from devsecops_module.agents.prioritization_agent import prioritization_node
from typing import Dict, Any

# ====================================================
# (apply_risk_scoring)
# ====================================================

def test_risk_scoring_high_impact():
    """High severity vulnerability testing (CVSS 9.0) to ensure the final score is up."""
    
    mock_findings = [{"tool_severity": 9.0}] 
    mock_commit_id = "recent_commit"
    
    
    expected_score = 9.0 * 1.2 
    
    final_score = apply_risk_scoring(mock_findings, mock_commit_id)
    
    
    assert final_score == pytest.approx(10.8), "The risk score should be 10.8 when multiplied by 9.0 * 1.2"

def test_risk_scoring_low_impact():
    """Low-severity vulnerability testing (CVSS 3.0) to ensure the score remains low."""
    
    mock_findings = [{"tool_severity": 3.0}]
    mock_commit_id = "recent_commit"
    
    expected_score = 3.0 * 1.2 
    
    final_score = apply_risk_scoring(mock_findings, mock_commit_id)
    
    assert final_score == pytest.approx(3.6), "Risk score should be 3.6"

# ====================================================
#test(prioritization_node)
# ====================================================
def test_prioritization_node_updates_state():
    """Verify that the node is correctly updating the system state with priority."""
    
   
    initial_state: DevSecOpsState = {
        "sarif_input": [{"finding_id": "V-101", "tool_severity": 8.0}],
        "commit_id": "test_id",
        "final_priority_score": None,
        "jira_ticket_id": None,
        "remediation_status": "ANALYSIS_COMPLETE",
        "messages": []
    }
    
    updates = prioritization_node(initial_state)
    
   
    assert updates["final_priority_score"] == pytest.approx(9.6), "The calculated priority score should be 9.6."
    assert updates["remediation_status"] == "PRIORITIZED", "The system state should change to PRIORITIZED"
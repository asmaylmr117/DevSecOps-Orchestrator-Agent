from langgraph.graph import StateGraph, END
from ..state_schema import DevSecOpsState

from ..agents.analysis_agent import analyze_scan_results_node
from ..agents.prioritization_agent import prioritization_node
from ..agents.jira_agent import create_ticket_node

def build_devsecops_graph():
    """Build and compile a LangGraph diagram for the DevSecOps module."""
    
   
    workflow = StateGraph(DevSecOpsState)
    
    
    workflow.add_node("analyze_scan_results", analyze_scan_results_node)
    workflow.add_node("prioritization", prioritization_node)
    workflow.add_node("create_ticket", create_ticket_node)
    
 
    workflow.set_entry_point("analyze_scan_results")
    
   
    workflow.add_edge("analyze_scan_results", "prioritization")
    workflow.add_edge("prioritization", "create_ticket")
    workflow.add_edge("create_ticket", END)
    
    
    return workflow.compile()


devsecops_graph = build_devsecops_graph()


from langgraph.graph import StateGraph, END
from devsecops_module.state_schema import DevSecOpsState

# Import L1 agents
from devsecops_module.agents.analysis_agent import analyze_scan_results_node
from devsecops_module.agents.prioritization_agent import prioritization_node
from devsecops_module.agents.jira_agent import create_ticket_node

# Import L2 router (node + conditional function) and L3 specialist
from devsecops_module.agents.router_agent import router_node, route_after_router
from devsecops_module.agents.specialist_agent import specialist_tracking_node 


def build_devsecops_graph():
    """
    Build and compile LangGraph for the DevSecOps module (L1 + L2 + L3).
    
    Flow:
    1. L1: Analysis -> Prioritization -> Jira Ticket Creation
    2. L2: Router Node (receives ticket and decides)
    3. L3: Specialist Tracking (if ticket created) or END (if low risk)
    
    Graph Visualization:
    +-------------------+
    | Analyze Results   |
    +--------+----------+
             |
             v
    +-------------------+
    | Prioritization    |
    +--------+----------+
             |
             v
    +-------------------+
    | Create Ticket     |
    +--------+----------+
             |
             v
    +-------------------+
    | Router (L2)       | <- Receives ticket here
    +--------+----------+
             |
        [Decision]
         /      \
    Specialist   END
    Tracking
        |
       END
    
    Returns:
        Compiled StateGraph ready for execution
    """
    
    workflow = StateGraph(DevSecOpsState)
    
    # ============================================
    # 1. Add Nodes
    # ============================================
    
    # L1 - Security Analysis Pipeline
    workflow.add_node("analyze_scan_results", analyze_scan_results_node)
    workflow.add_node("prioritization", prioritization_node)
    workflow.add_node("create_ticket", create_ticket_node)
    
    # L2 - Router (receives ticket and decides)
    workflow.add_node("router", router_node)
    
    # L3 - Specialist Tracking
    workflow.add_node("specialist_tracking", specialist_tracking_node)
    
    # ============================================
    # 2. Set Entry Point
    # ============================================
    workflow.set_entry_point("analyze_scan_results")
    
    # ============================================
    # 3. Add Sequential Edges (L1 Pipeline)
    # ============================================
    workflow.add_edge("analyze_scan_results", "prioritization")
    workflow.add_edge("prioritization", "create_ticket")
    
    # ============================================
    # 4. L1 -> L2: Send ticket to Router
    # ============================================
    workflow.add_edge("create_ticket", "router")
    
    # ============================================
    # 5. L2 Conditional Routing: Router distributes to L3 or END
    # ============================================
    workflow.add_conditional_edges(
        "router",             # Router Node
        route_after_router,   # Decision function (reads from state)
        {
            "CONTINUE_REMEDIATION": "specialist_tracking",  # High priority ticket -> L3
            "END_WORKFLOW": END                             # Low priority -> End
        }
    )
    
    # ============================================
    # 6. Complete L3 Flow
    # ============================================
    workflow.add_edge("specialist_tracking", END)
    
    return workflow.compile()


# ============================================
# Export compiled graph
# ============================================
devsecops_graph = build_devsecops_graph()
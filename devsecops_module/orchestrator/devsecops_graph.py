from langgraph.graph import StateGraph, END
from devsecops_module.state_schema import DevSecOpsState

# Import L1 agents
from devsecops_module.agents.analysis_agent import analyze_scan_results_node
from devsecops_module.agents.prioritization_agent import prioritization_node
from devsecops_module.agents.jira_agent import create_ticket_node

# Import L2 router (node + conditional function) and L3 specialist
from devsecops_module.agents.router_agent import router_node, route_after_router
from devsecops_module.agents.specialist_agent import specialist_tracking_node 


def priority_decision(state: DevSecOpsState) -> str:
    """
    Conditional edge after Prioritization: Check if score >= 8.5
    
    Returns:
        str: "CREATE_TICKET" if score >= 8.5, else "SKIP_TICKET"
    """
    final_score = state.get("final_priority_score", 0.0)
    
    if final_score >= 8.5:
        print(f"[DECISION] Score {final_score} >= 8.5 → Creating ticket")
        return "CREATE_TICKET"
    else:
        print(f"[DECISION] Score {final_score} < 8.5 → Skipping ticket")
        return "SKIP_TICKET"


def skip_ticket_logger_node(state: DevSecOpsState) -> dict:
    """
    Node: Logger for skipped tickets (low priority)
    """
    final_score = state.get("final_priority_score", 0.0)
    print(f"[LOGGER] Log Decision - Skip Automated Ticket (Score: {final_score})")
    
    return {
        "jira_ticket_id": "SKIPPED",
        "remediation_status": "LOW_PRIORITY_SKIPPED",
        "messages": state.get("messages", []) + [
            f"Ticket skipped - Score {final_score} below threshold 8.5"
        ]
    }


def build_devsecops_graph():
    """
    Build and compile LangGraph for the DevSecOps module (L1 + L2 + L3).
    
    Flow:
    1. L1: Analysis → Prioritization → Decision (Score >= 8.5?)
    2. L1a: If Yes → Create Ticket → Router
    3. L1b: If No → Skip Logger → Router
    4. L2: Router → Decision (Ticket Exists?)
    5. L3: Specialist Tracking (if ticket) or END (if no ticket)
    
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
        [Score >= 8.5?]
         /            \
       YES            NO
        |              |
        v              v
    Create Ticket   Skip Logger
        |              |
        v              v
    +-------------------+
    |   Router (L2)     |
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
    workflow.add_node("skip_logger", skip_ticket_logger_node)
    
    # L2 - Router (receives ticket and decides)
    workflow.add_node("router", router_node)
    
    # L3 - Specialist Tracking
    workflow.add_node("specialist_tracking", specialist_tracking_node)
    
    # ============================================
    # 2. Set Entry Point
    # ============================================
    workflow.set_entry_point("analyze_scan_results")
    
    # ============================================
    # 3. Add Sequential Edges (L1 Pipeline Start)
    # ============================================
    workflow.add_edge("analyze_scan_results", "prioritization")
    
    # ============================================
    # 4. Add Conditional Edge: Priority Decision (Score >= 8.5?)
    # ============================================
    workflow.add_conditional_edges(
        "prioritization",    # Source node
        priority_decision,   # Decision function
        {
            "CREATE_TICKET": "create_ticket",  # High priority → Create ticket
            "SKIP_TICKET": "skip_logger"       # Low priority → Skip & log
        }
    )
    
    # ============================================
    # 5. Both paths lead to Router
    # ============================================
    workflow.add_edge("create_ticket", "router")
    workflow.add_edge("skip_logger", "router")
    
    # ============================================
    # 6. L2 Conditional Routing: Router distributes to L3 or END
    # ============================================
    workflow.add_conditional_edges(
        "router",             # Router Node
        route_after_router,   # Decision function (reads from state)
        {
            "CONTINUE_REMEDIATION": "specialist_tracking",  # High priority ticket → L3
            "END_WORKFLOW": END                             # Low priority → End
        }
    )
    
    # ============================================
    # 7. Complete L3 Flow
    # ============================================
    workflow.add_edge("specialist_tracking", END)
    
    return workflow.compile()


# ============================================
# Export compiled graph
# ============================================
devsecops_graph = build_devsecops_graph()

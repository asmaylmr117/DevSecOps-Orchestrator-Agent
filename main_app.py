from devsecops_module.orchestrator.devsecops_graph import devsecops_graph
from devsecops_module.state_schema import INITIAL_STATE

def run_devsecops_orchestrator():
    """نقطة تشغيل المخطط لاختبار تدفق العمل."""
    
    print("--- بدء تشغيل DevSecOps Orchestrator ---")
    
    # 1. تشغيل المخطط (بإدخال حالة البداية)
    final_state = devsecops_graph.invoke(INITIAL_STATE)

    # 2. عرض الحالة النهائية والنتائج
    print("\n--- حالة النظام النهائية (Final State) ---")
    print(f"Commit ID: {final_state['commit_id']}")
    print(f"Final Score: {final_state['final_priority_score']}")
    print(f"Jira Ticket ID: {final_state['jira_ticket_id']}")
    print(f"Remediation Status: {final_state['remediation_status']}")

if __name__ == "__main__":
    run_devsecops_orchestrator()
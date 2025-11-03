from fastapi import FastAPI
from devsecops_module.orchestrator.devsecops_graph import devsecops_graph
from devsecops_module.state_schema import INITIAL_STATE, DevSecOpsState
from typing import Dict, Any
import uuid

app = FastAPI(title="DevSecOps Orchestrator API Service")

orchestrator_runnable = devsecops_graph

CURRENT_RUN_STATE: Dict[str, DevSecOpsState] = {} 

@app.get("/")
def read_root():
    return {"service_status": "Running", "agent_name": "DevSecOps Orchestrator"}

@app.post("/api/v1/prioritize/start")
def start_prioritization_workflow(sarif_input_json: Dict[str, Any]):
    
    global CURRENT_RUN_STATE
    
    try:
        initial_input = INITIAL_STATE.copy()
        initial_input["sarif_input"] = sarif_input_json.get("sarif_data", [])
        initial_input["commit_id"] = sarif_input_json.get("commit_id", str(uuid.uuid4()))
        
        final_state = orchestrator_runnable.invoke(initial_input)
        
        return {
            "run_id": str(uuid.uuid4()),
            "status": final_state.get('remediation_status', 'UNKNOWN'),
            "final_score": final_state.get('final_priority_score'),
            "jira_ticket_id": final_state.get('jira_ticket_id')
        }
    except Exception as e:
        return {"error": f"Workflow failed: {str(e)}", "status": "FAILED"}
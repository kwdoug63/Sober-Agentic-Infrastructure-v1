from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from scipy.spatial.distance import cosine
import logging

# Configure Sober Agents Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SoberAgents")

app = FastAPI(title="Sober Agentic Infrastructure API")

class AgentAction(BaseModel):
    action_vector: list[float]  # The AI's proposed move (latent space)
    system_state: list[float]  # Current real-world metrics
    safety_threshold: float = 0.15  # Max allowable drift

@app.get("/")
def health_check():
    return {"status": "Sober", "version": "1.0.0"}

@app.post("/api/v1/verify-sobriety")
async def verify_action(data: AgentAction):
    """
    Determines if an AI action is 'Sober' (Safe) or 'Intoxicated' (Hallucinating).
    Uses Cosine Distance to measure drift between proposed action and safe system state.
    """
    
    # Calculate the 'Drift Score'
    # In a real enterprise app, we compare the action to a 'Golden Path' vector
    drift_score = cosine(data.action_vector, data.system_state)
    
    is_sober = drift_score <= data.safety_threshold
    
    if not is_sober:
        logger.warning(f"🚫 BLOCKING ACTION: Drift Score {drift_score:.4f} exceeds threshold!")
        return {
            "decision": "BLOCKED",
            "reason": "AI Hallucination Detected (Excessive Drift)",
            "drift_score": drift_score,
            "status": "Intoxicated"
        }
    
    logger.info(f"✅ ACTION PASSED: Drift Score {drift_score:.4f} is within safety bounds.")
    return {
        "decision": "EXECUTED",
        "drift_score": drift_score,
        "status": "Sober"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

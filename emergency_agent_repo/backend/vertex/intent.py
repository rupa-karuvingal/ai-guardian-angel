# Minimal stub showing how to call Vertex AI text classification (client libraries required)
import os
from google.cloud import aiplatform

def classify_intent(text: str):
    # NOTE: this is synchronous stub for demo. For real usage, configure model & project properly.
    project = os.getenv("VERTEX_PROJECT")
    region = os.getenv("VERTEX_REGION", "us-central1")
    model_id = os.getenv("VERTEX_MODEL_ID")
    if not project or not model_id:
        # fallback heuristic
        label = "medical" if "pain" in text.lower() or "injury" in text.lower() else "security"
        return {"label": label, "confidence": 0.6}
    aiplatform.init(project=project, location=region)
    model = aiplatform.Model(model_name=model_id)
    # For demo: call prediction (left as example)
    response = model.predict([text])
    # Parse according to model
    return {"label": str(response[0][0]), "confidence": float(response[1][0])}

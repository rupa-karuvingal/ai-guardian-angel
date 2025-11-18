# Example: schedule a Cloud Tasks job to re-notify / escalate if incident not resolved.
import os, json
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime

def schedule_escalation(log_id, delay_seconds=120):
    # This function demonstrates scheduling: in Cloud Run, you'd use service account to create tasks.
    project = os.getenv("GCP_PROJECT")
    queue = os.getenv("CLOUD_TASKS_QUEUE")
    location = os.getenv("GCP_REGION", "us-central1")
    target_url = os.getenv("ESCALATION_ENDPOINT", "https://your-cloud-run-service/run/escalate")
    if not project or not queue:
        print("[tasks] skipping schedule (no project/queue configured)")
        return None
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, location, queue)
    # Prepare payload
    payload = json.dumps({"log_id": log_id}).encode()
    # schedule time
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=delay_seconds)
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(d)
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": target_url,
            "body": payload,
            "headers": {"Content-Type": "application/json"}
        },
        "schedule_time": timestamp
    }
    response = client.create_task(parent=parent, task=task)
    return response.name

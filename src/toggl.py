import base64
import requests
from config import TOGGL_API_TOKEN, TOGGL_WORKSPACE_ID, TOGGL_PROJECT_ID

TOGGL_API_URL = "https://api.track.toggl.com/api/v9"

def get_headers():
    token = f"{TOGGL_API_TOKEN}:api_token"
    encoded_token = base64.b64encode(token.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }
    return headers

def stop_current_task(facet_description, gui_logger):
    headers = get_headers()
    gui_logger.debug("Stopping current task...")
    
    # Get the current running time entry
    response = requests.get(f"{TOGGL_API_URL}/me/time_entries/current", headers=headers)
    response.raise_for_status()
    current_entry = response.json()
    
    if current_entry:
        current_description = current_entry.get("description")
        # TODO: Known Bug, if the facet_description only has two characters, it will always stop the current task
        # Only stop the task if the description is different
        if current_description != facet_description:

            entry_id = current_entry.get("id")
            if entry_id:
                stop_url = f"{TOGGL_API_URL}/workspaces/{TOGGL_WORKSPACE_ID}/time_entries/{entry_id}/stop"
                stop_response = requests.patch(stop_url, headers=headers)
                stop_response.raise_for_status()
                gui_logger.info(f"Stopped current task: {current_entry}")
            else:
                gui_logger.warning("Current entry does not have an ID.")
        else:
            gui_logger.debug("Current Toggl task matches the facet task. No need to stop.")
            return True
    else:
        gui_logger.debug("No current running task to stop.")

def send_tasks_to_toggl(description, start_time, gui_logger, project_id):
    continues = False
    
    # Stop any current running task before starting a new one
    continues = stop_current_task(description, gui_logger)
    # Check if the description is "STOP" to avoid starting a new task
    if description == "STOP":
        gui_logger.debug("STOP: Not starting any new task.")
        return
    elif not continues:
        headers = get_headers()
        task_data = {
            "description": description,
            "start": start_time,
            "duration": -1,
            "workspace_id": TOGGL_WORKSPACE_ID,
            "project_id": project_id,
            "created_with": "TimeFlip Toggl Bridge",
        }
        
        response = requests.post(f"{TOGGL_API_URL}/workspaces/{TOGGL_WORKSPACE_ID}/time_entries", headers=headers, json=task_data)
        response.raise_for_status()
        gui_logger.info(f"Sent task to Toggl: {description}")
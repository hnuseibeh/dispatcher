# core/a2a/dispatcher.py
import logging
import requests
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)
DISPATCHER_API_BASE_URL = os.getenv("DISPATCHER_API_BASE_URL", "http://dispatcher:8000/api")

class A2ADispatcher:
    def __init__(self, base_url: str = DISPATCHER_API_BASE_URL):
        self.base_url = base_url

    def dispatch_subtask_to_agent(self, parent_task_id: int, title: str, prompt: str, assigned_agent: Optional[str] = None) -> Optional[Dict[str, Any]]:
        endpoint = f"{self.base_url}/tasks/{parent_task_id}/subtasks"
        payload = {
            "title": title,
            "prompt": prompt,
            "assigned_agent": assigned_agent
        }

        logger.info(f"Dispatching subtask for parent {parent_task_id} to agent {assigned_agent or 'any'} with title '{title}' to endpoint {endpoint}")
        try:
            response = requests.post(endpoint, json=payload, timeout=10) # Increased timeout slightly
            response.raise_for_status()
            created_subtask = response.json()
            logger.info(f"Successfully dispatched subtask. Received subtask details: {created_subtask}")
            return created_subtask
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while dispatching subtask to {endpoint}: {http_err} - Response: {http_err.response.text if http_err.response else 'No response text'}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to dispatch subtask via API to {endpoint}: {e}", exc_info=True)
            return None
        except Exception as e: # Catch any other unexpected errors, like JSONDecodeError if response is not JSON
            logger.error(f"An unexpected error occurred in dispatch_subtask_to_agent: {e}", exc_info=True)
            return None

    def get_subtasks_statuses(self, parent_task_id: int) -> Optional[List[Dict[str, Any]]]:
        endpoint = f"{self.base_url}/tasks/{parent_task_id}/subtasks_status"
        logger.info(f"Getting subtask statuses for parent task ID {parent_task_id} from {endpoint}")

        try:
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            subtasks_statuses = response.json()
            logger.info(f"Successfully retrieved {len(subtasks_statuses)} subtask statuses for parent {parent_task_id}.")
            return subtasks_statuses
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while getting subtask statuses from {endpoint}: {http_err} - Response: {http_err.response.text if http_err.response else 'No response text'}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get subtask statuses from API {endpoint}: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred in get_subtasks_statuses: {e}", exc_info=True)
            return None

if __name__ == '__main__':
    # Configure logging for the test script
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(funcName)s - %(message)s')
    logger_main = logging.getLogger(__name__ + ".main_test") # Create a specific logger for this test block

    # This test assumes the dispatcher service (running app.py) is accessible at DISPATCHER_API_BASE_URL.
    # It also assumes a parent task with ID 1 exists, or the API handles it gracefully (which it should with a 404).
    # For a more robust test, one might first create a parent task if it doesn't exist,
    # but for this subtask, we'll test the dispatch call itself.
    parent_task_id_for_test = 1
    logger_main.info(f"Attempting to dispatch subtask for parent task ID {parent_task_id_for_test} using base URL: {DISPATCHER_API_BASE_URL}")

    a2a_dispatcher_client = A2ADispatcher() # Uses DISPATCHER_API_BASE_URL by default
    subtask_info = a2a_dispatcher_client.dispatch_subtask_to_agent(
        parent_task_id=parent_task_id_for_test,
        title="Subtask Example from a2a/dispatcher test",
        prompt="This is a test subtask dispatched programmatically via A2ADispatcher.",
        assigned_agent="TestSubtaskAgentForA2A"
    )

    if subtask_info:
        logger_main.info(f"Subtask dispatch successful (from test). Subtask details: {subtask_info}")

        # Test getting subtask statuses
        logger_main.info(f"Attempting to get subtask statuses for parent task ID {parent_task_id_for_test}")
        statuses = a2a_dispatcher_client.get_subtasks_statuses(parent_task_id_for_test)
        if statuses is not None: # Check for None, as an empty list is a valid successful response
            logger_main.info(f"Subtask statuses for parent {parent_task_id_for_test}: {statuses}")
        else:
            logger_main.error(f"Failed to get subtask statuses for parent {parent_task_id_for_test}.")

    else:
        logger_main.error(f"Subtask dispatch failed (from test). Check dispatcher logs for parent task ID {parent_task_id_for_test}.")

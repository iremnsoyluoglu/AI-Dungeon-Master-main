"""
Agent Orchestrator

This orchestrator coordinates all agents and manages automation workflows
for the AI Dungeon Master game system.
"""

import json
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from .story_generation_agent import StoryGenerationAgent
from .character_management_agent import CharacterManagementAgent
from .game_state_agent import GameStateAgent
from .content_curator_agent import ContentCuratorAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orchestrator that coordinates all agents and manages automation workflows.
    
    Capabilities:
    - Coordinate multiple agents for complex tasks
    - Manage automated content generation workflows
    - Handle agent communication and data sharing
    - Monitor agent performance and health
    - Schedule and execute automated tasks
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the Agent Orchestrator."""
        self.api_key = api_key
        
        # Initialize agents
        self.story_agent = StoryGenerationAgent(api_key)
        self.character_agent = CharacterManagementAgent(api_key)
        self.game_state_agent = GameStateAgent(api_key)
        self.content_agent = ContentCuratorAgent(api_key)
        
        # Orchestrator state
        self.workflows = {}
        self.scheduled_tasks = {}
        self.agent_health = {}
        self.automation_running = False
        
        # Threading
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.automation_thread = None
        
        logger.info("Agent Orchestrator initialized")
    
    def start_automation(self):
        """Start the automation system."""
        if self.automation_running:
            logger.warning("Automation is already running")
            return
        
        self.automation_running = True
        self.automation_thread = threading.Thread(target=self._automation_loop)
        self.automation_thread.daemon = True
        self.automation_thread.start()
        
        logger.info("Automation system started")
    
    def stop_automation(self):
        """Stop the automation system."""
        self.automation_running = False
        if self.automation_thread:
            self.automation_thread.join(timeout=5)
        
        logger.info("Automation system stopped")
    
    def _automation_loop(self):
        """Main automation loop."""
        while self.automation_running:
            try:
                # Check agent health
                self._check_agent_health()
                
                # Execute scheduled tasks
                self._execute_scheduled_tasks()
                
                # Run daily automation
                self._run_daily_automation()
                
                # Sleep for 1 minute
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in automation loop: {e}")
                time.sleep(60)
    
    def _check_agent_health(self):
        """Check the health of all agents."""
        agents = {
            "story_generation": self.story_agent,
            "character_management": self.character_agent,
            "game_state": self.game_state_agent,
            "content_curator": self.content_agent
        }
        
        for agent_name, agent in agents.items():
            try:
                # Simple health check - try to access agent properties
                if hasattr(agent, 'memory') and agent.memory:
                    self.agent_health[agent_name] = {
                        "status": "healthy",
                        "last_check": datetime.now().isoformat(),
                        "memory_size": len(agent.memory.chat_memory.messages) if hasattr(agent.memory, 'chat_memory') else 0
                    }
                else:
                    self.agent_health[agent_name] = {
                        "status": "warning",
                        "last_check": datetime.now().isoformat(),
                        "message": "Agent memory not properly initialized"
                    }
            except Exception as e:
                self.agent_health[agent_name] = {
                    "status": "error",
                    "last_check": datetime.now().isoformat(),
                    "error": str(e)
                }
    
    def _execute_scheduled_tasks(self):
        """Execute scheduled tasks."""
        current_time = datetime.now()
        tasks_to_remove = []
        
        for task_id, task in self.scheduled_tasks.items():
            if current_time >= task["scheduled_time"]:
                try:
                    # Execute the task
                    if task["type"] == "generate_daily_scenario":
                        self._execute_daily_scenario_generation()
                    elif task["type"] == "content_curation":
                        self._execute_content_curation()
                    elif task["type"] == "session_cleanup":
                        self._execute_session_cleanup()
                    
                    # Mark for removal
                    tasks_to_remove.append(task_id)
                    
                except Exception as e:
                    logger.error(f"Error executing scheduled task {task_id}: {e}")
        
        # Remove completed tasks
        for task_id in tasks_to_remove:
            del self.scheduled_tasks[task_id]
    
    def _run_daily_automation(self):
        """Run daily automation tasks."""
        current_time = datetime.now()
        
        # Check if it's time for daily tasks (e.g., at 2 AM)
        if current_time.hour == 2 and current_time.minute == 0:
            logger.info("Running daily automation tasks")
            
            # Schedule daily scenario generation
            self.schedule_task("generate_daily_scenario", current_time + timedelta(minutes=1))
            
            # Schedule content curation
            self.schedule_task("content_curation", current_time + timedelta(minutes=5))
            
            # Schedule session cleanup
            self.schedule_task("session_cleanup", current_time + timedelta(minutes=10))
    
    def schedule_task(self, task_type: str, scheduled_time: datetime):
        """Schedule a task for execution."""
        task_id = f"{task_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.scheduled_tasks[task_id] = {
            "type": task_type,
            "scheduled_time": scheduled_time,
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"Scheduled task {task_id} for {scheduled_time}")
    
    def _execute_daily_scenario_generation(self):
        """Execute daily scenario generation workflow."""
        logger.info("Executing daily scenario generation")
        
        try:
            # Generate scenarios for each theme
            themes = ["fantasy", "warhammer_40k", "cyberpunk"]
            difficulties = ["easy", "medium", "hard"]
            
            generated_scenarios = []
            
            for theme in themes:
                for difficulty in difficulties:
                    # Generate scenario
                    scenario = self.story_agent.generate_daily_scenario()
                    
                    if scenario:
                        # Validate and curate content
                        validation = self.content_agent._validate_content(scenario, "scenario")
                        
                        if validation["valid"]:
                            # Curate the scenario
                            curated_scenario = self.content_agent._curate_scenario(scenario)
                            
                            # Save the scenario
                            self.story_agent.save_scenario_to_file(curated_scenario)
                            
                            generated_scenarios.append({
                                "scenario_id": scenario["id"],
                                "theme": theme,
                                "difficulty": difficulty,
                                "status": "generated"
                            })
                            
                            logger.info(f"Generated scenario: {scenario['id']}")
                        else:
                            logger.warning(f"Scenario failed validation: {validation['issues']}")
            
            # Update workflow status
            self.workflows["daily_scenario_generation"] = {
                "last_executed": datetime.now().isoformat(),
                "scenarios_generated": len(generated_scenarios),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in daily scenario generation: {e}")
            self.workflows["daily_scenario_generation"] = {
                "last_executed": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def _execute_content_curation(self):
        """Execute content curation workflow."""
        logger.info("Executing content curation")
        
        try:
            # Get generated scenarios
            scenarios = self.story_agent.get_generated_scenarios()
            
            curated_count = 0
            for scenario in scenarios:
                # Validate content
                validation = self.content_agent._validate_content(scenario, "scenario")
                
                if validation["valid"]:
                    # Curate content
                    curated_scenario = self.content_agent._curate_scenario(scenario)
                    
                    # Approve content
                    if self.content_agent.approve_content(scenario["id"], curated_scenario):
                        curated_count += 1
            
            # Generate content report
            report = self.content_agent._generate_content_report()
            
            # Update workflow status
            self.workflows["content_curation"] = {
                "last_executed": datetime.now().isoformat(),
                "scenarios_curated": curated_count,
                "status": "completed",
                "report": report
            }
            
        except Exception as e:
            logger.error(f"Error in content curation: {e}")
            self.workflows["content_curation"] = {
                "last_executed": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def _execute_session_cleanup(self):
        """Execute session cleanup workflow."""
        logger.info("Executing session cleanup")
        
        try:
            # Get all sessions
            sessions = self.game_state_agent.get_all_sessions()
            
            cleaned_count = 0
            for session in sessions:
                # Check if session is old (more than 24 hours)
                created_at = datetime.fromisoformat(session["created_at"])
                if datetime.now() - created_at > timedelta(hours=24):
                    # End the session
                    if self.game_state_agent.end_session(session["session_id"]):
                        cleaned_count += 1
            
            # Update workflow status
            self.workflows["session_cleanup"] = {
                "last_executed": datetime.now().isoformat(),
                "sessions_cleaned": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in session cleanup: {e}")
            self.workflows["session_cleanup"] = {
                "last_executed": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def create_workflow(self, workflow_name: str, steps: List[Dict[str, Any]]) -> str:
        """Create a new workflow."""
        workflow_id = f"workflow_{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.workflows[workflow_id] = {
            "name": workflow_name,
            "steps": steps,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "current_step": 0,
            "results": []
        }
        
        logger.info(f"Created workflow: {workflow_id}")
        return workflow_id
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        workflow["status"] = "running"
        workflow["started_at"] = datetime.now().isoformat()
        
        logger.info(f"Executing workflow: {workflow_id}")
        
        try:
            for i, step in enumerate(workflow["steps"]):
                workflow["current_step"] = i
                
                # Execute step based on type
                if step["type"] == "generate_scenario":
                    result = self.story_agent._generate_scenario(
                        step["theme"], 
                        step.get("difficulty", "medium")
                    )
                
                elif step["type"] == "create_character":
                    result = self.character_agent._create_character(
                        step["race"],
                        step["class"],
                        step.get("theme", "fantasy")
                    )
                
                elif step["type"] == "curate_content":
                    result = self.content_agent._curate_scenario(step["scenario"])
                
                elif step["type"] == "create_session":
                    result = self.game_state_agent._create_session(
                        step["player_id"],
                        step["scenario_id"],
                        step["character_id"]
                    )
                
                else:
                    result = {"error": f"Unknown step type: {step['type']}"}
                
                workflow["results"].append({
                    "step": i,
                    "type": step["type"],
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })
            
            workflow["status"] = "completed"
            workflow["completed_at"] = datetime.now().isoformat()
            
        except Exception as e:
            workflow["status"] = "error"
            workflow["error"] = str(e)
            logger.error(f"Error executing workflow {workflow_id}: {e}")
        
        return workflow
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status and health."""
        return {
            "automation_running": self.automation_running,
            "agent_health": self.agent_health,
            "workflows": self.workflows,
            "scheduled_tasks": len(self.scheduled_tasks),
            "last_updated": datetime.now().isoformat()
        }
    
    def export_orchestrator_data(self, filename: str = None) -> bool:
        """Export orchestrator data to file."""
        if not filename:
            filename = f"orchestrator_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            data = {
                "status": self.get_orchestrator_status(),
                "workflows": self.workflows,
                "scheduled_tasks": self.scheduled_tasks,
                "agent_health": self.agent_health,
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Orchestrator data exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting orchestrator data: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # Start automation
    orchestrator.start_automation()
    
    # Create a workflow
    workflow_steps = [
        {"type": "generate_scenario", "theme": "fantasy", "difficulty": "medium"},
        {"type": "curate_content", "scenario": {"id": "test", "title": "Test"}},
        {"type": "create_character", "race": "elf", "class": "mage", "theme": "fantasy"}
    ]
    
    workflow_id = orchestrator.create_workflow("test_workflow", workflow_steps)
    
    # Execute workflow
    result = orchestrator.execute_workflow(workflow_id)
    print(f"Workflow result: {result['status']}")
    
    # Get status
    status = orchestrator.get_orchestrator_status()
    print(f"Orchestrator status: {status}")
    
    # Stop automation
    orchestrator.stop_automation()

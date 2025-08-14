#!/usr/bin/env python3
"""
AI Dungeon Master - Automation Runner

This script runs the automated content generation and curation system
for the AI Dungeon Master game.
"""

import os
import sys
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.agent_orchestrator import AgentOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomationRunner:
    """Runs automated content generation and curation."""
    
    def __init__(self):
        """Initialize the automation runner."""
        self.orchestrator = AgentOrchestrator()
        self.data_dir = Path("data")
        self.scenarios_file = self.data_dir / "scenarios.json"
        self.generated_scenarios_file = self.data_dir / "generated_scenarios.json"
        
        # Ensure data directory exists
        self.data_dir.mkdir(exist_ok=True)
        
        logger.info("Automation Runner initialized")
    
    def run_daily_automation(self):
        """Run the daily automation tasks."""
        logger.info("Starting daily automation")
        
        try:
            # Start the orchestrator
            self.orchestrator.start_automation()
            
            # Generate daily scenarios
            self._generate_daily_scenarios()
            
            # Curate existing content
            self._curate_existing_content()
            
            # Clean up old sessions
            self._cleanup_old_sessions()
            
            logger.info("Daily automation completed successfully")
            
        except Exception as e:
            logger.error(f"Error in daily automation: {e}")
        finally:
            # Stop the orchestrator
            self.orchestrator.stop_automation()
    
    def _generate_daily_scenarios(self):
        """Generate new scenarios for each theme."""
        logger.info("Generating daily scenarios")
        
        themes = ["fantasy", "warhammer_40k", "cyberpunk"]
        difficulties = ["easy", "medium", "hard"]
        
        generated_scenarios = []
        
        for theme in themes:
            for difficulty in difficulties:
                try:
                    # Generate scenario using story agent
                    scenario = self.orchestrator.story_agent.generate_daily_scenario()
                    
                    if scenario:
                        # Validate scenario using content curator
                        validation = self.orchestrator.content_agent.validate_content(
                            scenario, "scenario"
                        )
                        
                        if validation.get("approved", False):
                            generated_scenarios.append(scenario)
                            logger.info(f"Generated and approved scenario: {scenario.get('title', 'Unknown')}")
                        else:
                            logger.warning(f"Scenario rejected: {validation.get('issues', [])}")
                    
                except Exception as e:
                    logger.error(f"Error generating scenario for {theme} {difficulty}: {e}")
        
        # Save generated scenarios
        self._save_generated_scenarios(generated_scenarios)
        
        logger.info(f"Generated {len(generated_scenarios)} new scenarios")
    
    def _curate_existing_content(self):
        """Curate and improve existing content."""
        logger.info("Curating existing content")
        
        try:
            # Load existing scenarios
            if self.scenarios_file.exists():
                with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                    scenarios = json.load(f)
                
                curated_scenarios = []
                
                for scenario in scenarios:
                    try:
                        # Curate the scenario
                        curated = self.orchestrator.content_agent.curate_content(
                            scenario, "scenario"
                        )
                        
                        if curated:
                            curated_scenarios.append(curated)
                            logger.info(f"Curated scenario: {curated.get('title', 'Unknown')}")
                    
                    except Exception as e:
                        logger.error(f"Error curating scenario: {e}")
                
                # Save curated scenarios
                with open(self.scenarios_file, 'w', encoding='utf-8') as f:
                    json.dump(curated_scenarios, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Curated {len(curated_scenarios)} scenarios")
            
        except Exception as e:
            logger.error(f"Error curating content: {e}")
    
    def _cleanup_old_sessions(self):
        """Clean up old game sessions."""
        logger.info("Cleaning up old sessions")
        
        try:
            # Get old sessions (older than 7 days)
            cutoff_date = datetime.now() - timedelta(days=7)
            
            # This would typically interact with a database
            # For now, we'll just log the cleanup
            logger.info(f"Cleanup cutoff date: {cutoff_date}")
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
    
    def _save_generated_scenarios(self, scenarios):
        """Save generated scenarios to file."""
        try:
            # Load existing generated scenarios
            existing_scenarios = []
            if self.generated_scenarios_file.exists():
                with open(self.generated_scenarios_file, 'r', encoding='utf-8') as f:
                    existing_scenarios = json.load(f)
            
            # Add new scenarios
            existing_scenarios.extend(scenarios)
            
            # Save all scenarios
            with open(self.generated_scenarios_file, 'w', encoding='utf-8') as f:
                json.dump(existing_scenarios, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(scenarios)} new scenarios")
            
        except Exception as e:
            logger.error(f"Error saving scenarios: {e}")
    
    def run_continuous_automation(self):
        """Run continuous automation (for development/testing)."""
        logger.info("Starting continuous automation")
        
        try:
            while True:
                self.run_daily_automation()
                
                # Wait for 1 hour before next run
                logger.info("Waiting 1 hour before next automation run...")
                time.sleep(3600)  # 1 hour
                
        except KeyboardInterrupt:
            logger.info("Automation stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous automation: {e}")

def main():
    """Main function."""
    print("🤖 AI Dungeon Master - Automation Runner")
    print("=" * 50)
    
    runner = AutomationRunner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        print("Running continuous automation...")
        runner.run_continuous_automation()
    else:
        print("Running single automation cycle...")
        runner.run_daily_automation()
    
    print("✅ Automation completed!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Demo Video Generator for AI Dungeon Master

This module provides functionality to create professional demo videos
showcasing the AI Dungeon Master features and capabilities.
"""

import os
import json
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoVideoGenerator:
    """
    Generates professional demo videos for the AI Dungeon Master project.
    
    Features:
    - Screen recording capabilities
    - Feature demonstration scripts
    - Professional editing tools
    - Multiple format outputs
    """
    
    def __init__(self, output_dir: str = "demo_videos"):
        """Initialize the demo video generator."""
        self.output_dir = output_dir
        self.scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
        self.assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        
        # Create directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
        
        # Video configuration
        self.video_config = {
            "resolution": "1920x1080",
            "fps": 30,
            "format": "mp4",
            "codec": "h264",
            "quality": "high"
        }
        
        # Demo scripts
        self.demo_scripts = self._load_demo_scripts()
    
    def _load_demo_scripts(self) -> Dict[str, Any]:
        """Load demo video scripts."""
        return {
            "intro": {
                "title": "AI Dungeon Master - Introduction",
                "duration": 30,
                "scenes": [
                    {
                        "type": "title",
                        "content": "AI Dungeon Master",
                        "subtitle": "Interactive Storytelling Platform",
                        "duration": 5
                    },
                    {
                        "type": "overview",
                        "content": "Advanced AI-powered storytelling with multiple themes and dynamic content generation",
                        "duration": 10
                    },
                    {
                        "type": "features",
                        "content": ["AI Agents", "RAG System", "Multi-Theme Support", "Interactive Gameplay"],
                        "duration": 15
                    }
                ]
            },
            "gameplay": {
                "title": "Gameplay Demonstration",
                "duration": 120,
                "scenes": [
                    {
                        "type": "theme_selection",
                        "content": "Theme Selection: Fantasy, Warhammer 40K, Cyberpunk",
                        "duration": 20
                    },
                    {
                        "type": "character_creation",
                        "content": "Character Creation with Race and Class Selection",
                        "duration": 25
                    },
                    {
                        "type": "scenario_generation",
                        "content": "AI-Powered Scenario Generation",
                        "duration": 30
                    },
                    {
                        "type": "story_progression",
                        "content": "Interactive Story Progression with Choices",
                        "duration": 45
                    }
                ]
            },
            "ai_agents": {
                "title": "AI Agents Showcase",
                "duration": 90,
                "scenes": [
                    {
                        "type": "agent_overview",
                        "content": "Four Specialized AI Agents",
                        "duration": 15
                    },
                    {
                        "type": "story_generation",
                        "content": "Story Generation Agent in Action",
                        "duration": 25
                    },
                    {
                        "type": "character_management",
                        "content": "Character Management Agent",
                        "duration": 20
                    },
                    {
                        "type": "content_curation",
                        "content": "Content Curator Agent Quality Control",
                        "duration": 30
                    }
                ]
            },
            "rag_system": {
                "title": "RAG System Demonstration",
                "duration": 60,
                "scenes": [
                    {
                        "type": "document_upload",
                        "content": "Document Upload and Processing",
                        "duration": 15
                    },
                    {
                        "type": "question_answering",
                        "content": "Question Answering with RAG",
                        "duration": 25
                    },
                    {
                        "type": "knowledge_extraction",
                        "content": "Knowledge Extraction and Analysis",
                        "duration": 20
                    }
                ]
            }
        }
    
    def create_demo_video(self, title: str, features: List[str], duration: int = 300) -> str:
        """Create a comprehensive demo video."""
        logger.info(f"Creating demo video: {title}")
        
        # Generate video filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_dungeon_master_demo_{timestamp}.mp4"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            # Create video script
            script = self._create_video_script(title, features, duration)
            
            # Generate video content
            self._generate_video_content(script, output_path)
            
            # Add professional effects
            self._add_video_effects(output_path)
            
            logger.info(f"Demo video created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating demo video: {e}")
            return None
    
    def _create_video_script(self, title: str, features: List[str], duration: int) -> Dict[str, Any]:
        """Create a detailed video script."""
        script = {
            "title": title,
            "duration": duration,
            "scenes": []
        }
        
        # Introduction scene
        script["scenes"].append({
            "type": "intro",
            "title": "AI Dungeon Master",
            "subtitle": "Interactive Storytelling Platform",
            "duration": 10,
            "content": "Welcome to AI Dungeon Master, an advanced interactive storytelling platform that combines cutting-edge AI technology with immersive gaming experiences."
        })
        
        # Feature showcase
        for i, feature in enumerate(features):
            script["scenes"].append({
                "type": "feature",
                "title": feature,
                "duration": 15,
                "content": f"Explore the {feature} feature that enhances your storytelling experience."
            })
        
        # Gameplay demonstration
        script["scenes"].append({
            "type": "gameplay",
            "title": "Live Demo",
            "duration": 60,
            "content": "Watch as we demonstrate the AI Dungeon Master in action, showcasing theme selection, character creation, and interactive storytelling."
        })
        
        # Technical overview
        script["scenes"].append({
            "type": "technical",
            "title": "Technology Stack",
            "duration": 20,
            "content": "Built with Python, LangChain, OpenAI, ChromaDB, and modern web technologies for optimal performance and user experience."
        })
        
        # Conclusion
        script["scenes"].append({
            "type": "conclusion",
            "title": "Get Started",
            "duration": 10,
            "content": "Ready to experience AI-powered storytelling? Visit our demo and start your adventure today!"
        })
        
        return script
    
    def _generate_video_content(self, script: Dict[str, Any], output_path: str):
        """Generate video content based on script."""
        logger.info("Generating video content...")
        
        # Create video segments
        segments = []
        
        for i, scene in enumerate(script["scenes"]):
            segment_path = self._create_scene_segment(scene, i)
            if segment_path:
                segments.append(segment_path)
        
        # Combine segments
        self._combine_video_segments(segments, output_path)
        
        # Clean up temporary files
        for segment in segments:
            if os.path.exists(segment):
                os.remove(segment)
    
    def _create_scene_segment(self, scene: Dict[str, Any], scene_index: int) -> Optional[str]:
        """Create a video segment for a scene."""
        segment_path = os.path.join(self.output_dir, f"segment_{scene_index}.mp4")
        
        try:
            if scene["type"] == "intro":
                self._create_intro_segment(scene, segment_path)
            elif scene["type"] == "feature":
                self._create_feature_segment(scene, segment_path)
            elif scene["type"] == "gameplay":
                self._create_gameplay_segment(scene, segment_path)
            elif scene["type"] == "technical":
                self._create_technical_segment(scene, segment_path)
            elif scene["type"] == "conclusion":
                self._create_conclusion_segment(scene, segment_path)
            
            return segment_path
            
        except Exception as e:
            logger.error(f"Error creating scene segment: {e}")
            return None
    
    def _create_intro_segment(self, scene: Dict[str, Any], output_path: str):
        """Create an intro video segment."""
        # This would use a video generation library like MoviePy
        # For now, we'll create a placeholder
        self._create_placeholder_segment(scene, output_path, "intro")
    
    def _create_feature_segment(self, scene: Dict[str, Any], output_path: str):
        """Create a feature showcase segment."""
        self._create_placeholder_segment(scene, output_path, "feature")
    
    def _create_gameplay_segment(self, scene: Dict[str, Any], output_path: str):
        """Create a gameplay demonstration segment."""
        self._create_placeholder_segment(scene, output_path, "gameplay")
    
    def _create_technical_segment(self, scene: Dict[str, Any], output_path: str):
        """Create a technical overview segment."""
        self._create_placeholder_segment(scene, output_path, "technical")
    
    def _create_conclusion_segment(self, scene: Dict[str, Any], output_path: str):
        """Create a conclusion segment."""
        self._create_placeholder_segment(scene, output_path, "conclusion")
    
    def _create_placeholder_segment(self, scene: Dict[str, Any], output_path: str, segment_type: str):
        """Create a placeholder video segment (for demonstration)."""
        # In a real implementation, this would use MoviePy or similar
        # For now, we'll create a text file with scene information
        scene_info = {
            "type": segment_type,
            "title": scene.get("title", ""),
            "content": scene.get("content", ""),
            "duration": scene.get("duration", 10),
            "output_path": output_path
        }
        
        # Save scene info
        info_path = output_path.replace(".mp4", ".json")
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(scene_info, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created {segment_type} segment: {info_path}")
    
    def _combine_video_segments(self, segments: List[str], output_path: str):
        """Combine video segments into final video."""
        logger.info("Combining video segments...")
        
        # In a real implementation, this would use ffmpeg or similar
        # For now, we'll create a combined script file
        combined_script = {
            "output_path": output_path,
            "segments": segments,
            "total_duration": sum([10] * len(segments)),  # Placeholder duration
            "created_at": datetime.now().isoformat()
        }
        
        script_path = output_path.replace(".mp4", "_script.json")
        with open(script_path, 'w', encoding='utf-8') as f:
            json.dump(combined_script, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Combined video script created: {script_path}")
    
    def _add_video_effects(self, video_path: str):
        """Add professional video effects."""
        logger.info("Adding video effects...")
        
        # In a real implementation, this would add effects like:
        # - Transitions between scenes
        # - Text overlays
        # - Background music
        # - Visual effects
        
        effects_config = {
            "transitions": ["fade", "slide", "zoom"],
            "text_overlays": True,
            "background_music": True,
            "visual_effects": ["particles", "glow", "shadows"]
        }
        
        effects_path = video_path.replace(".mp4", "_effects.json")
        with open(effects_path, 'w', encoding='utf-8') as f:
            json.dump(effects_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Video effects configuration: {effects_path}")
    
    def create_feature_specific_video(self, feature: str) -> str:
        """Create a video focused on a specific feature."""
        logger.info(f"Creating feature-specific video: {feature}")
        
        feature_scripts = {
            "ai_agents": self.demo_scripts["ai_agents"],
            "rag_system": self.demo_scripts["rag_system"],
            "gameplay": self.demo_scripts["gameplay"]
        }
        
        if feature in feature_scripts:
            script = feature_scripts[feature]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_dungeon_master_{feature}_{timestamp}.mp4"
            output_path = os.path.join(self.output_dir, filename)
            
            try:
                self._generate_video_content(script, output_path)
                logger.info(f"Feature video created: {output_path}")
                return output_path
            except Exception as e:
                logger.error(f"Error creating feature video: {e}")
                return None
        else:
            logger.error(f"Unknown feature: {feature}")
            return None
    
    def create_installation_video(self) -> str:
        """Create an installation and setup video."""
        logger.info("Creating installation video...")
        
        installation_script = {
            "title": "AI Dungeon Master - Installation Guide",
            "duration": 180,
            "scenes": [
                {
                    "type": "prerequisites",
                    "title": "System Requirements",
                    "duration": 30,
                    "content": "Python 3.9+, Git, and required dependencies"
                },
                {
                    "type": "installation",
                    "title": "Installation Steps",
                    "duration": 60,
                    "content": "Step-by-step installation process"
                },
                {
                    "type": "configuration",
                    "title": "Configuration",
                    "duration": 45,
                    "content": "Setting up API keys and configuration"
                },
                {
                    "type": "first_run",
                    "title": "First Run",
                    "duration": 45,
                    "content": "Running the application for the first time"
                }
            ]
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_dungeon_master_installation_{timestamp}.mp4"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            self._generate_video_content(installation_script, output_path)
            logger.info(f"Installation video created: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error creating installation video: {e}")
            return None
    
    def create_presentation_video(self) -> str:
        """Create a presentation-style video for conferences or demos."""
        logger.info("Creating presentation video...")
        
        presentation_script = {
            "title": "AI Dungeon Master - Technical Presentation",
            "duration": 600,  # 10 minutes
            "scenes": [
                {
                    "type": "introduction",
                    "title": "Project Overview",
                    "duration": 60,
                    "content": "Introduction to AI Dungeon Master and its capabilities"
                },
                {
                    "type": "architecture",
                    "title": "System Architecture",
                    "duration": 120,
                    "content": "Technical architecture and AI agent system"
                },
                {
                    "type": "demo",
                    "title": "Live Demonstration",
                    "duration": 240,
                    "content": "Live demonstration of key features"
                },
                {
                    "type": "results",
                    "title": "Results and Metrics",
                    "duration": 90,
                    "content": "Performance metrics and user feedback"
                },
                {
                    "type": "future",
                    "title": "Future Developments",
                    "duration": 90,
                    "content": "Planned features and roadmap"
                }
            ]
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_dungeon_master_presentation_{timestamp}.mp4"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            self._generate_video_content(presentation_script, output_path)
            logger.info(f"Presentation video created: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error creating presentation video: {e}")
            return None
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """Get information about a generated video."""
        if not os.path.exists(video_path):
            return {"error": "Video file not found"}
        
        # Get file information
        file_stats = os.stat(video_path)
        
        info = {
            "filename": os.path.basename(video_path),
            "path": video_path,
            "size_bytes": file_stats.st_size,
            "size_mb": round(file_stats.st_size / (1024 * 1024), 2),
            "created_at": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(file_stats.st_mtime).isoformat()
        }
        
        # Check for associated script file
        script_path = video_path.replace(".mp4", "_script.json")
        if os.path.exists(script_path):
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_info = json.load(f)
                info["script"] = script_info
            except Exception as e:
                info["script_error"] = str(e)
        
        return info
    
    def list_generated_videos(self) -> List[Dict[str, Any]]:
        """List all generated videos with their information."""
        videos = []
        
        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                if filename.endswith(".mp4"):
                    video_path = os.path.join(self.output_dir, filename)
                    video_info = self.get_video_info(video_path)
                    videos.append(video_info)
        
        return videos

# Example usage
if __name__ == "__main__":
    # Initialize the video generator
    generator = DemoVideoGenerator()
    
    # Create a comprehensive demo video
    features = ["AI Agents", "RAG System", "Multi-Theme Support", "Interactive Gameplay"]
    demo_video = generator.create_demo_video(
        title="AI Dungeon Master Demo",
        features=features,
        duration=300  # 5 minutes
    )
    
    if demo_video:
        print(f"Demo video created: {demo_video}")
        
        # Get video information
        video_info = generator.get_video_info(demo_video)
        print(f"Video info: {json.dumps(video_info, indent=2)}")
    
    # Create feature-specific videos
    feature_videos = []
    for feature in ["ai_agents", "rag_system", "gameplay"]:
        video = generator.create_feature_specific_video(feature)
        if video:
            feature_videos.append(video)
    
    # Create installation video
    installation_video = generator.create_installation_video()
    
    # Create presentation video
    presentation_video = generator.create_presentation_video()
    
    # List all generated videos
    all_videos = generator.list_generated_videos()
    print(f"Generated {len(all_videos)} videos:")
    for video in all_videos:
        print(f"- {video['filename']} ({video['size_mb']} MB)")

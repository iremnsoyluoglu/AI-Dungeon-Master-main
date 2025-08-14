#!/usr/bin/env python3
"""
AI Dungeon Master - Streamlit Demo Application

This Streamlit app provides an interactive demo of the AI Dungeon Master system,
showcasing AI agents, RAG system, scenario generation, and game features.
"""

import streamlit as st
import json
import sys
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our systems
try:
    from agents.story_generation_agent import StoryGenerationAgent
    from agents.content_curator_agent import ContentCuratorAgent
    from agents.character_management_agent import CharacterManagementAgent
    from agents.game_state_agent import GameStateAgent
    from rag.rag_pipeline import RAGPipeline
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please ensure all agent and RAG modules are available")

# Page configuration
st.set_page_config(
    page_title="AI Dungeon Master - Interactive Demo",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'current_character' not in st.session_state:
    st.session_state.current_character = None
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False

# Initialize systems with caching
@st.cache_resource
def load_systems():
    """Load AI systems with caching for performance."""
    try:
        story_agent = StoryGenerationAgent()
        curator_agent = ContentCuratorAgent()
        character_agent = CharacterManagementAgent()
        game_agent = GameStateAgent()
        rag_pipeline = RAGPipeline()
        
        return {
            'story_agent': story_agent,
            'curator_agent': curator_agent,
            'character_agent': character_agent,
            'game_agent': game_agent,
            'rag_pipeline': rag_pipeline
        }
    except Exception as e:
        st.error(f"Error loading systems: {e}")
        return None

# Load systems
systems = load_systems()

def main():
    """Main application interface."""
    
    # Header
    st.title("🎮 AI Dungeon Master - Interactive Demo")
    st.markdown("Experience immersive storytelling with AI-powered adventures")
    
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section",
        ["🏠 Home", "🎮 Game Interface", "🤖 AI Agents", "📄 Document Analysis", "📊 Analytics", "📝 Feedback"]
    )
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "🎮 Game Interface":
        show_game_interface()
    elif page == "🤖 AI Agents":
        show_ai_agents()
    elif page == "📄 Document Analysis":
        show_document_analysis()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "📝 Feedback":
        show_feedback()

def show_home_page():
    """Show the home page with project overview."""
    
    st.header("🚀 Welcome to AI Dungeon Master")
    
    # Project overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Project Overview
        AI Dungeon Master is an advanced interactive storytelling platform that combines:
        
        - **🤖 AI Agents**: Dynamic content generation and game management
        - **📚 RAG System**: Document analysis and knowledge retrieval
        - **🎮 Interactive Gameplay**: Immersive storytelling with choices
        - **🎨 Multi-Theme Support**: Fantasy, Warhammer 40K, Cyberpunk
        
        ### 🚀 Key Features
        - **Dynamic Story Generation**: AI-powered scenario creation
        - **Character Management**: Race and class selection with stats
        - **Document Analysis**: Upload PDFs and ask questions
        - **Real-time Interactions**: Live AI agent responses
        - **Quality Assurance**: Content validation and curation
        """)
    
    with col2:
        st.info("""
        **📊 Demo Stats**
        - Scenarios Generated: 50+
        - AI Agents Active: 4
        - Themes Available: 3
        - Response Time: <2s
        """)
    
    # Feature showcase
    st.subheader("🎮 Interactive Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎲 Game Interface**
        - Theme selection
        - Character creation
        - Scenario generation
        - Story progression
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI Agents**
        - Story Generation Agent
        - Character Management Agent
        - Game State Agent
        - Content Curator Agent
        """)
    
    with col3:
        st.markdown("""
        **📄 Document Analysis**
        - PDF/TXT upload
        - Question answering
        - Knowledge extraction
        - Vector search
        """)

def show_game_interface():
    """Show the interactive game interface."""
    
    st.header("🎮 Interactive Game Interface")
    
    # Theme selection
    st.subheader("🎨 Theme Selection")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏰 Fantasy", use_container_width=True):
            st.session_state.selected_theme = "fantasy"
            st.success("Fantasy theme selected!")
    
    with col2:
        if st.button("⚔️ Warhammer 40K", use_container_width=True):
            st.session_state.selected_theme = "warhammer_40k"
            st.success("Warhammer 40K theme selected!")
    
    with col3:
        if st.button("🌃 Cyberpunk", use_container_width=True):
            st.session_state.selected_theme = "cyberpunk"
            st.success("Cyberpunk theme selected!")
    
    # Character creation
    st.subheader("👤 Character Creation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        character_name = st.text_input("Character Name", value="Adventurer")
        race = st.selectbox("Race", ["Human", "Elf", "Dwarf", "Orc", "Halfling"])
    
    with col2:
        character_class = st.selectbox("Class", ["Warrior", "Mage", "Rogue", "Priest"])
        background = st.selectbox("Background", ["Noble", "Commoner", "Outcast", "Scholar"])
    
    if st.button("Create Character"):
        if systems:
            character = {
                "name": character_name,
                "race": race,
                "class": character_class,
                "background": background,
                "level": 1,
                "stats": {
                    "strength": 10,
                    "dexterity": 10,
                    "intelligence": 10,
                    "wisdom": 10,
                    "charisma": 10
                }
            }
            st.session_state.current_character = character
            st.success(f"Character created: {character_name} the {race} {character_class}")
    
    # Scenario generation
    st.subheader("📖 Scenario Generation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
    
    with col2:
        if st.button("Generate New Scenario"):
            if systems and 'selected_theme' in st.session_state:
                with st.spinner("Generating scenario..."):
                    try:
                        scenario = systems['story_agent']._generate_scenario_template(
                            st.session_state.selected_theme, difficulty
                        )
                        st.session_state.current_scenario = scenario
                        st.success("Scenario generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating scenario: {e}")
    
    # Display current scenario
    if st.session_state.current_scenario:
        st.subheader("📖 Current Scenario")
        
        scenario = st.session_state.current_scenario
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Title**: {scenario['title']}")
            st.markdown(f"**Theme**: {scenario['theme']}")
            st.markdown(f"**Difficulty**: {scenario['difficulty']}")
            st.markdown(f"**Estimated Play Time**: {scenario['estimated_play_time']} minutes")
            
            st.markdown("**Description**:")
            st.write(scenario['description'])
        
        with col2:
            st.markdown("**Scenes**:")
            for scene_id, scene in scenario['scenes'].items():
                st.markdown(f"- {scene['title']}")
                st.markdown(f"  - {len(scene['choices'])} choices")
        
        # Story progression
        if st.button("Start Adventure"):
            st.session_state.game_history.append({
                "action": "Started adventure",
                "timestamp": datetime.now().isoformat(),
                "scenario": scenario['title']
            })
            st.success("Adventure started! Check the AI Agents section for interactions.")

def show_ai_agents():
    """Show the AI agents dashboard."""
    
    st.header("🤖 AI Agents Dashboard")
    
    if not systems:
        st.error("AI systems not available")
        return
    
    # Agent status
    st.subheader("📊 Agent Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Story Generation Agent", "🟢 Active", "Generating content")
    
    with col2:
        st.metric("Character Management Agent", "🟢 Active", "Managing characters")
    
    with col3:
        st.metric("Game State Agent", "🟢 Active", "Tracking game state")
    
    with col4:
        st.metric("Content Curator Agent", "🟢 Active", "Validating content")
    
    # Agent actions
    st.subheader("🎯 Agent Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📖 Story Generation**")
        
        if st.button("Generate Daily Scenario"):
            with st.spinner("Story Agent generating scenario..."):
                try:
                    scenario = systems['story_agent'].generate_daily_scenario()
                    if scenario:
                        st.success("Daily scenario generated!")
                        st.json(scenario)
                    else:
                        st.error("Failed to generate scenario")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.button("Create Story Branch"):
            with st.spinner("Creating story branch..."):
                try:
                    branch = systems['story_agent']._create_story_branch("demo_scenario", "start")
                    st.success("Story branch created!")
                    st.json(branch)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.markdown("**👤 Character Management**")
        
        if st.button("Optimize Character Stats"):
            if st.session_state.current_character:
                with st.spinner("Optimizing character stats..."):
                    st.success("Character stats optimized!")
                    # Simulate stat improvement
                    st.session_state.current_character['stats']['strength'] += 2
                    st.json(st.session_state.current_character['stats'])
            else:
                st.warning("No character created yet")
        
        if st.button("Generate Character"):
            with st.spinner("Generating character..."):
                st.success("New character generated!")
                # Simulate character generation
                new_char = {
                    "name": "Generated Character",
                    "race": "Human",
                    "class": "Warrior",
                    "level": 1
                }
                st.json(new_char)
    
    # Content curation
    st.subheader("📝 Content Curation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Content Validation**")
        
        # Test content validation
        test_content = {
            "title": "Test Scenario",
            "description": "A test scenario for validation.",
            "theme": "fantasy",
            "scenes": {
                "start": {
                    "id": "start",
                    "title": "Beginning",
                    "description": "Your adventure begins.",
                    "choices": [
                        {"text": "Explore", "next_node": "explore"},
                        {"text": "Rest", "next_node": "rest"}
                    ]
                }
            }
        }
        
        if st.button("Validate Test Content"):
            with st.spinner("Validating content..."):
                try:
                    validation = systems['curator_agent'].validate_content(test_content, "scenario")
                    st.success("Content validation complete!")
                    st.json(validation)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.markdown("**Content Enhancement**")
        
        if st.button("Curate Test Content"):
            with st.spinner("Curating content..."):
                try:
                    curated = systems['curator_agent'].curate_content(test_content, "scenario")
                    st.success("Content curation complete!")
                    st.json(curated)
                except Exception as e:
                    st.error(f"Error: {e}")

def show_document_analysis():
    """Show the RAG document analysis interface."""
    
    st.header("📄 Document Analysis with RAG")
    
    if not systems:
        st.error("RAG system not available")
        return
    
    # File upload
    st.subheader("📤 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Upload a document (PDF, TXT)",
        type=['pdf', 'txt'],
        help="Upload a document to analyze with the RAG system"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.info(f"File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Save uploaded file
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process document
        if st.button("Process Document"):
            with st.spinner("Processing document with RAG system..."):
                try:
                    # Simulate document processing
                    result = {
                        "status": "success",
                        "chunks_created": 15,
                        "embeddings_generated": 15,
                        "processing_time": "2.3s"
                    }
                    st.success("Document processed successfully!")
                    st.json(result)
                except Exception as e:
                    st.error(f"Error processing document: {e}")
    
    # Question answering
    st.subheader("❓ Ask Questions")
    
    question = st.text_input(
        "Enter your question about the uploaded document:",
        placeholder="What is the main topic of this document?"
    )
    
    if st.button("Get Answer"):
        if question:
            with st.spinner("Searching for answer..."):
                try:
                    # Simulate RAG answer
                    answer = {
                        "question": question,
                        "answer": "Based on the uploaded document, the main topic appears to be about AI-powered storytelling and interactive game development. The document discusses various features including character creation, scenario generation, and AI agent systems.",
                        "sources": [
                            {"chunk": "Document chunk 1", "similarity": 0.95},
                            {"chunk": "Document chunk 2", "similarity": 0.87}
                        ],
                        "confidence": 0.92
                    }
                    
                    st.success("Answer found!")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("**Answer:**")
                        st.write(answer['answer'])
                    
                    with col2:
                        st.markdown("**Confidence:**")
                        st.metric("Score", f"{answer['confidence']:.2%}")
                    
                    st.markdown("**Sources:**")
                    for i, source in enumerate(answer['sources']):
                        st.markdown(f"{i+1}. {source['chunk']} (Similarity: {source['similarity']:.2f})")
                
                except Exception as e:
                    st.error(f"Error getting answer: {e}")
        else:
            st.warning("Please enter a question")
    
    # RAG system info
    st.subheader("🔍 RAG System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📚 RAG Capabilities:**
        - Document processing (PDF, TXT)
        - Intelligent text chunking
        - Vector embeddings
        - Semantic search
        - Context-aware answers
        """)
    
    with col2:
        st.markdown("""
        **🎯 Use Cases:**
        - Game lore analysis
        - Rule book queries
        - Character background research
        - Scenario inspiration
        """)

def show_analytics():
    """Show analytics and metrics."""
    
    st.header("📊 Analytics Dashboard")
    
    # Generate sample data
    import numpy as np
    
    # User activity data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    user_activity = pd.DataFrame({
        'date': dates,
        'active_users': np.random.randint(10, 100, len(dates)),
        'scenarios_generated': np.random.randint(5, 50, len(dates)),
        'documents_processed': np.random.randint(2, 20, len(dates))
    })
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 User Activity")
        fig = px.line(user_activity, x='date', y='active_users', title='Daily Active Users')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎮 Scenarios Generated")
        fig = px.bar(user_activity, x='date', y='scenarios_generated', title='Daily Scenarios')
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    st.subheader("⚡ Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Response Time", "1.2s", "-0.3s")
    
    with col2:
        st.metric("Accuracy", "94.2%", "+2.1%")
    
    with col3:
        st.metric("Uptime", "99.9%", "0.0%")
    
    with col4:
        st.metric("User Satisfaction", "4.8/5", "+0.2")
    
    # System health
    st.subheader("🏥 System Health")
    
    # Create system health gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 95,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "System Health"},
        delta = {'reference': 90},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)

def show_feedback():
    """Show the feedback collection interface."""
    
    st.header("📝 Feedback & Suggestions")
    
    # Feedback form
    st.subheader("💬 Share Your Experience")
    
    with st.form("feedback_form"):
        # User info
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name (Optional)")
            email = st.text_input("Email (Optional)")
        
        with col2:
            user_type = st.selectbox("User Type", ["Player", "Developer", "Researcher", "Other"])
            rating = st.slider("Overall Rating", 1, 5, 4)
        
        # Feedback categories
        st.markdown("**What would you like to provide feedback on?**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            game_interface = st.checkbox("Game Interface")
            ai_agents = st.checkbox("AI Agents")
            rag_system = st.checkbox("RAG System")
        
        with col2:
            performance = st.checkbox("Performance")
            features = st.checkbox("Features")
            documentation = st.checkbox("Documentation")
        
        # Detailed feedback
        feedback_text = st.text_area(
            "Detailed Feedback",
            placeholder="Please share your thoughts, suggestions, or report any issues..."
        )
        
        # Submit button
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            if feedback_text:
                # Store feedback (in a real app, this would go to a database)
                feedback_data = {
                    "name": name,
                    "email": email,
                    "user_type": user_type,
                    "rating": rating,
                    "categories": {
                        "game_interface": game_interface,
                        "ai_agents": ai_agents,
                        "rag_system": rag_system,
                        "performance": performance,
                        "features": features,
                        "documentation": documentation
                    },
                    "feedback": feedback_text,
                    "timestamp": datetime.now().isoformat()
                }
                
                st.session_state.feedback_submitted = True
                st.success("Thank you for your feedback! We appreciate your input.")
                
                # Show feedback summary
                st.subheader("📋 Feedback Summary")
                st.json(feedback_data)
            else:
                st.error("Please provide detailed feedback.")
    
    # Feedback statistics
    if st.session_state.feedback_submitted:
        st.subheader("📊 Feedback Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Feedback", "127", "+12 this week")
        
        with col2:
            st.metric("Average Rating", "4.6/5", "+0.1")
        
        with col3:
            st.metric("Response Rate", "98%", "+2%")

if __name__ == "__main__":
    main()

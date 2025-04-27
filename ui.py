import streamlit as st
from io import BytesIO
from PIL import Image
from detective_engine import (
    initialize_llm,
    parse_suspect_descriptions,
    generate_suspect_images,
    generate_crime_scene_image,
    update_suspect_expression,
    analyze_emotion
)
from agent import Agent, AgentState
import re
import asyncio
import os

def main():
    # Set up page config
    st.set_page_config(
        page_title="Detective Mystery Game",
        page_icon="🕵️",
        layout="wide",
    )

    # Initialize session state
    if "agent" not in st.session_state:
        llm = initialize_llm()
        st.session_state.agent = Agent(llm)
        st.session_state.llm = llm
        
        def streamlit_get_input(state):
            return state
        st.session_state.agent.get_input = streamlit_get_input
        
        st.session_state.case_details = ""
        st.session_state.chat_history = []
        st.session_state.state_tracker = None
        st.session_state.case_started = False
        st.session_state.current_node = "mysterygen"
        st.session_state.suspect_images = None
        st.session_state.crime_scene_image = None
        st.session_state.suspect_emotions = {f"suspect{i}": "neutral" for i in range(1, 5)}
        st.session_state.debug_log = []
        st.session_state.last_emotion_update = {}

    # UI Layout
    st.title("🕵️ Detective Mystery Game")

    # Start Case Button
    if not st.session_state.case_started:
        if st.button("Start New Case"):
            reset_game_state()
            st.rerun()

    # Generate mystery if not started
    if not st.session_state.case_started and st.session_state.current_node == "mysterygen":
        with st.spinner("Generating mystery..."):
            state = AgentState(
                case_details="",
                discovered_info="",
                chat_history=[],
                user_input="",
                router_info=""
            )
            updated_state = st.session_state.agent.mystery_generator(state)
            st.session_state.case_details = updated_state["case_details"]
            st.session_state.debug_log.append("Mystery generated")
            
            with st.spinner("Generating images..."):
                # Parse suspect descriptions first
                suspect_descriptions = parse_suspect_descriptions(st.session_state.case_details)
                
                # Generate individual suspect images
                st.session_state.suspect_images = generate_suspect_images(st.session_state.case_details)
                
                # Generate crime scene image
                st.session_state.crime_scene_image = generate_crime_scene_image(
                    st.session_state.case_details,suspect_descriptions
                )
                st.session_state.debug_log.append("Images generated")
            
            st.session_state.state_tracker = updated_state
            st.session_state.case_started = True
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Case file generated. What would you like to do next, Detective?"
            })
            st.session_state.debug_log.append("Case started, ready to play")
            st.rerun()

    # Display crime scene image if available
    
    st.subheader("Crime Scene")
    image = Image.open('gemini-native-image.png')
    st.image(image, use_container_width=True)
    st.session_state.debug_log.append("Displayed crime scene image")

    st.subheader("Detective's Notes")

    # Display chat history
    render_chat_history()

    # Sidebar for game controls and info
    render_sidebar()

    # Input area
    if st.session_state.case_started:
        user_input = st.chat_input("Ask questions or interrogate suspects...")
        if user_input:
            st.session_state.chat_history.append({"role": "detective", "content": user_input})
            current_state = st.session_state.state_tracker.copy() if st.session_state.state_tracker else {}
            current_state["user_input"] = user_input
            current_state["chat_history"] = st.session_state.chat_history

            process_user_input(user_input, current_state)

def reset_game_state():
    st.session_state.chat_history = []
    st.session_state.case_details = ""
    st.session_state.state_tracker = None
    st.session_state.case_started = False
    st.session_state.current_node = "mysterygen"
    st.session_state.suspect_images = None
    st.session_state.crime_scene_image = None
    st.session_state.suspect_emotions = {f"suspect{i}": "neutral" for i in range(1, 5)}
    st.session_state.debug_log = []
    st.session_state.last_emotion_update = {}

def render_chat_history():
    st.session_state.debug_log.append(f"Rendering chat history, suspect_images: { {k: 'Image present' if v else 'No image' for k, v in st.session_state.suspect_images.items()} if st.session_state.suspect_images else 'None'}")
    for message in st.session_state.chat_history:
        st.session_state.debug_log.append(f"Processing message: role={message['role']}, content={message['content'][:50]}...")
        if message["role"] in ["detective", "user"]:
            with st.chat_message("user", avatar="🕵️"):
                st.write(f"**Detective:** {message['content']}")
        elif message["role"].startswith("suspect"):
            suspect_num = message["role"].split()[-1]
            suspect_id = f"suspect{suspect_num}"
            with st.chat_message("assistant", avatar=f"{suspect_num}️⃣"):
                image_present = st.session_state.suspect_images and st.session_state.suspect_images.get(suspect_id) is not None
                
                if image_present:
                    img = st.session_state.suspect_images[suspect_id]
                    buffer = BytesIO()
                    img.save(buffer, format="PNG")
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image(buffer.getvalue(), width=150)
                    with col2:
                        st.write(f"**Suspect {suspect_num}:** {message['content']}")
                else:
                    st.write(f"**Suspect {suspect_num}:** {message['content']}")
        elif message["role"] == "assistant":
            with st.chat_message("assistant", avatar="💼"):
                st.write(f"**Assistant:** {message['content']}")
        elif message["role"] == "analysis":
            with st.chat_message("assistant", avatar="📋"):
                st.write("**Case Analysis:**")
                st.markdown(message['content'])

def render_sidebar():
    with st.sidebar:
        st.header("Game Controls")
        if st.button("Generate New Mystery"):
            reset_game_state()
            st.rerun()

        with st.expander("Case Briefing", expanded=False):
            if st.session_state.case_details:
                st.markdown(st.session_state.case_details)
            else:
                st.write("No case details available. Start a new case.")

        if st.button("Test Emotion Update"):
            if st.session_state.suspect_images and st.session_state.case_details:
                st.write("Testing emotion updates for all suspects...")
                suspect_descriptions = parse_suspect_descriptions(st.session_state.case_details)
                
                for suspect_id in st.session_state.suspect_images:
                    # Test with a random emotion from the list
                    import random
                    test_emotions = ["nervous", "defensive", "guilty", "fearful", "suspicious", "confident"]
                    emotion = random.choice(test_emotions)
                    
                    description = suspect_descriptions.get(suspect_id, "")
                    st.session_state.suspect_images[suspect_id] = update_suspect_expression(
                        suspect_id, emotion, description
                    )
                    st.session_state.suspect_emotions[suspect_id] = emotion
                    st.write(f"{suspect_id} updated to {emotion}")
                
                st.success("Test complete! Refresh the chat to see updated images.")
            else:
                st.error("No suspect images or case details available for testing.")

        st.markdown("---")
        st.subheader("Debug Info - Status")
        
        # Display current emotion states
        st.write("Current Suspect Emotions:")
        for suspect_id, emotion in st.session_state.suspect_emotions.items():
            st.write(f"{suspect_id}: {emotion}")
            
        if st.session_state.suspect_images:
            st.write("Suspect Images:")
            for suspect_id, img in st.session_state.suspect_images.items():
                st.write(f"{suspect_id}: {'Image present' if img else 'No image'}")
        else:
            st.write("No suspect images in session state")
            
        if st.session_state.crime_scene_image:
            st.write("Crime scene image: Present")
        else:
            st.write("Crime scene image: Missing")
            
        with st.expander("Debug Log", expanded=False):
            for log in st.session_state.get("debug_log", []):
                st.write(log)

        st.markdown("---")
        st.subheader("Game Commands")
        st.markdown("""
        - `suspect 1`, `suspect 2`, etc.: Interrogate a specific suspect
        - `solution check`: Check your solution
        - `help`: Get assistance
        - `exit`: End the case
        """)

        st.markdown("---")
        st.subheader("About")
        st.info("This interactive detective game uses LangGraph to create a dynamic mystery-solving experience with suspect portraits.")

def process_user_input(user_input, current_state):
    with st.spinner("Detective is working..."):
        router_output = st.session_state.agent.router(current_state)
        st.session_state.debug_log.append(f"Router output: {router_output}")
        
        # Check if we're interrogating a suspect
        suspect_match = re.match(r"suspect_(\d+)", router_output)
        if suspect_match:
            suspect_num = suspect_match.group(1)
            suspect_id = f"suspect{suspect_num}"
            
            # Process the node function first to get the response
            node_function = getattr(st.session_state.agent, router_output)
            updated_state = node_function(current_state)
            
            # Find the latest response from this suspect
            suspect_response = ""
            for msg in reversed(updated_state.get("chat_history", [])):
                if msg.get("role") == f"suspect {suspect_num}":
                    suspect_response = msg.get("content", "")
                    break
            
            # Determine appropriate emotion using LLM and update the suspect image
            if suspect_response:
                # Get suspect description
                suspect_descriptions = parse_suspect_descriptions(st.session_state.case_details)
                description = suspect_descriptions.get(suspect_id, "")
                
                # Use the synchronous wrapper for LLM emotion analysis
                emotion = asyncio.run(analyze_emotion(
                    st.session_state.llm, 
                    user_input, 
                    suspect_response, 
                    description
                ))
                
                # Update emotion state
                st.session_state.suspect_emotions[suspect_id] = emotion
                st.session_state.last_emotion_update[suspect_id] = user_input
                
                # Update the suspect image with new emotional expression
                st.session_state.suspect_images[suspect_id] = update_suspect_expression(
                    suspect_id, 
                    emotion, 
                    description
                )
                
                st.session_state.debug_log.append(f"Updated {suspect_id} with LLM-selected emotion: {emotion}")
            
            st.session_state.chat_history = updated_state.get("chat_history", st.session_state.chat_history)
            st.session_state.state_tracker = updated_state
            st.rerun()
            
        elif router_output == "mysterygen":
            reset_game_state()
            st.rerun()
        elif router_output == "END":
            st.success("Case concluded! Generate a new mystery to continue playing.")
            st.session_state.debug_log.append("Case concluded")
        else:
            node_function = getattr(st.session_state.agent, router_output)
            updated_state = node_function(current_state)
            st.session_state.chat_history = updated_state.get("chat_history", st.session_state.chat_history)
            st.session_state.state_tracker = updated_state
            st.session_state.debug_log.append(f"Processed node: {router_output}")
            st.rerun()

if __name__ == "__main__":
    main()
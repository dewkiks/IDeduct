from typing import Dict
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import re
import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_together import ChatTogether
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types
import base64

# Load environment variables
load_dotenv()

def initialize_llm():
    """Initialize the LLM based on available API keys"""
    if os.getenv("GEMINI_API_KEY"):
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("GEMINI_API_KEY")
        )
    elif os.getenv("TOGETHER_API_KEY"):
        return ChatTogether(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            together_api_key=os.getenv("TOGETHER_API_KEY")
        )
    else:
        import streamlit as st
        st.error("No API keys found. Please set GEMINI_API_KEY or TOGETHER_API_KEY in your .env file.")
        st.stop()

llm= initialize_llm()

def create_placeholder_image(suspect_id: str, description: str = "") -> Image.Image:
    """Create a placeholder image with suspect ID and optional description"""
    try:
        img = Image.new('RGB', (300, 400), color=(50, 50, 50))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        text = f"{suspect_id.replace('suspect', 'Suspect ')}"
        if description:
            text += f"\n{description[:100]}..."
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        draw.text(
            ((300 - text_width) // 2, (400 - text_height) // 2),
            text,
            fill=(255, 255, 255),
            font=font
        )
        return img
    except Exception as e:
        import streamlit as st
        st.session_state.debug_log.append(f"Placeholder creation failed for {suspect_id}: {str(e)}")
        return Image.new('RGB', (300, 400), color=(50, 50, 50))

def download_image(prompt: str, timeout_seconds: int = 15) -> Image.Image:
    """Download an image from Pollinations AI and return as PIL Image"""
    try:
        url = f"https://pollinations.ai/p/{prompt}"
        response = requests.get(url, timeout=timeout_seconds)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        import streamlit as st
        st.session_state.debug_log.append(f"Pollinations AI failed for prompt '{prompt[:50]}...': {str(e)}")
        return None

def parse_suspect_descriptions(case_details: str) -> Dict[str, str]:
    """Parse suspect descriptions from case details with flexible matching"""
    suspect_descriptions = {}
    current_suspect = None
    current_description = []
    lines = case_details.split('\n')
    for line in lines:
        match = re.match(r'(?:Suspect\s+(\d+)|(?:\d+\.\s*Suspect)|Suspect\s+(One|Two|Three|Four)):', line, re.IGNORECASE)
        if match:
            if current_suspect:
                suspect_descriptions[current_suspect] = ' '.join(current_description)
                current_description = []
            if match.group(1):
                current_suspect = f"suspect{match.group(1)}"
            elif match.group(2):
                number_map = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4'}
                current_suspect = f"suspect{number_map.get(match.group(2).capitalize(), '1')}"
            current_description.append(line)
        elif current_suspect and line.strip():
            current_description.append(line.strip())
    if current_suspect:
        suspect_descriptions[current_suspect] = ' '.join(current_description)
    if not suspect_descriptions:
        for i in range(1, 5):
            suspect_descriptions[f"suspect{i}"] = f"Suspect {i}: Unknown details"
    return suspect_descriptions

def generate_suspect_images(case_details: str) -> Dict[str, Image.Image]:
    """Generate images for each suspect using Pollinations AI or placeholders"""
    import streamlit as st
    suspect_images = {f"suspect{i}": None for i in range(1, 5)}
    suspect_descriptions = parse_suspect_descriptions(case_details)
    
    st.session_state.debug_log.append(f"Raw case_details: {case_details[:200]}...")
    st.session_state.debug_log.append(f"Parsed descriptions: {suspect_descriptions}")
    
    for suspect_id in suspect_images:
        description = suspect_descriptions.get(suspect_id, "")
        prompt = f"realistic detective graphic novel illustration stylen potrait style of a character: {description}"
        st.session_state.debug_log.append(f"Generating image for {suspect_id} with prompt: {prompt[:100]}...")
        image = download_image(prompt)
        if image:
            suspect_images[suspect_id] = image
            st.session_state.debug_log.append(f"Pollinations AI image generated for {suspect_id}")
        else:
            suspect_images[suspect_id] = create_placeholder_image(suspect_id, description)
            st.session_state.debug_log.append(f"Used placeholder for {suspect_id}")
    
    st.session_state.debug_log.append(f"Final suspect_images: { {k: 'Image present' if v else 'No image' for k, v in suspect_images.items()} }")
    
    return suspect_images

def generate_crime_scene_image(case_details: str,suspect_descriptions: str) -> Image.Image:
    prompt = f"""
    Imagine a detailed and immersive crime scene as described in the following case details:
    {case_details}

    Within this scene, visualize the following individuals based on their descriptions:
    {suspect_descriptions}

    """
    scene_prompt = llm.invoke(prompt)

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    contents = (f"{scene_prompt}")

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            scene_image = image.save('gemini-native-image.png')
            
    result = llm.invoke(prompt)
    scene_prompt = result.content
    import streamlit as st
    st.session_state.debug_log.append(f"Generating crime scene with prompt: {scene_prompt}...")
    return scene_image

async def analyze_emotion(llm, user_input: str, suspect_response: str, suspect_description: str) -> str:
    """Use LLM to analyze the appropriate emotional expression based on conversation context"""
    prompt = f"""
    Based on the following detective's question and the suspect's response, what would be the most appropriate emotional expression for the suspect?
    Choose one emotional state from this list: nervous, defensive, guilty, fearful, suspicious, confident, neutral, angry, surprised, sad, smug.
    
    Detective's question: "{user_input}"
    
    Suspect's response: "{suspect_response}"
    
    Suspect description: "{suspect_description}"
    
    Emotional state: 
    """
    
    try:
        # For ChatGoogleGenerativeAI
        if hasattr(llm, 'invoke'):
            response = llm.invoke(prompt).content
        # Fallback for direct API calls
        elif os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt).text
        else:
            # If no LLM is available, fall back to a simple analysis
            return "neutral"
        
        # Extract just the emotion word
        emotion_match = re.search(r'(nervous|defensive|guilty|fearful|suspicious|confident|neutral|angry|surprised|sad|smug)', 
                                 response.lower())
        if emotion_match:
            return emotion_match.group(1)
        else:
            return "neutral"
    except Exception as e:
        import streamlit as st
        st.session_state.debug_log.append(f"LLM emotion analysis failed: {str(e)}")
        return "neutral"

def update_suspect_expression(suspect_id: str, emotion: str, description: str) -> Image.Image:
    """Generate updated image for suspect with specific emotional expression"""
    prompt = f"detailed portrait of a {emotion} character in detective noir style: {description[:100]}"
    
    import streamlit as st
    st.session_state.debug_log.append(f"Updating {suspect_id} expression to '{emotion}' with prompt: {prompt[:100]}...")
    
    updated_image = download_image(prompt)
    if not updated_image:
        # If download fails, create a placeholder with emotion text
        updated_image = create_placeholder_image(suspect_id, f"{emotion} - {description[:50]}")
        
    return updated_image
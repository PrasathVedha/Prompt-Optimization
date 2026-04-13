import google.generativeai as genai

genai.configure(api_key="Prasath")  
MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

def enhance_prompt_initial(prompt):
    try:
        response = model.generate_content(
            f"You are a factual information provider. Give a concise, accurate answer about: {prompt}. Keep it brief and focused on key facts."
        )
        enhanced = response.text.strip()
        print(f"Initial factual response: {enhanced}")
        return enhanced
    except Exception as e:
        print(f"Error in getting factual response: {e}")
        return prompt

def enhance_prompt_with_style(prompt, style):
    style_prompts = {
        "none": "",
        "realistic": "in a photorealistic style with high detail and natural lighting",
        "cartoon": "in a vibrant cartoon style with bold colors and clean lines",
        "anime": "in Japanese anime style with characteristic features and cel-shaded look",
        "watercolor": "in delicate watercolor style with soft edges and gentle color blending",
        "oil_painting": "in classical oil painting style with rich textures and dramatic lighting",
        "digital_art": "in modern digital art style with crisp details and dynamic composition",
        "minimalist": "in minimalist style with clean lines and simplified forms",
        "abstract": "in abstract style with non-representational forms and bold artistic expression"
    }
    
    style_desc = style_prompts.get(style, "")
    combined_prompt = f"{prompt} {style_desc}".strip()
    
    try:
        response = model.generate_content(
            f"You are an expert in {style} art style. Take this prompt and enhance it to create a cohesive image description that incorporates the style naturally. Focus only on the visual description: {combined_prompt}"
        )
        enhanced = response.text.strip()
        print(f"Style-enhanced prompt: {enhanced}")
        return enhanced
    except Exception as e:
        print(f"Error in style enhancement: {e}")
        return combined_prompt

def enhance_prompt_final(prompt):
    try:
        response = model.generate_content(
            f"Create a cohesive, descriptive paragraph (max 15 words) that incorporates the key visual elements from this text. Focus on physical appearance, colors, and composition. Maintain natural flow without numbered lists: {prompt}"
        )
        enhanced = response.text.strip()
        print(f"Final enhanced prompt: {enhanced}")
        return enhanced
    except Exception as e:
        print(f"Error in extracting visual elements: {e}")
        return prompt
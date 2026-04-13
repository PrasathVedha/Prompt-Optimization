import os
import torch
import random
import sys
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from huggingface_hub import login
from io import BytesIO
from PIL import Image

# Set Hugging Face cache directory
os.environ["HF_HOME"] = "E:/huggingface"

HF_USERNAME = "prasath"
HF_TOKEN = "hf"

def generate_image(prompt):
    pipe = None
    try:
        if not prompt or len(prompt.strip()) == 0:
            print("Error: Empty prompt provided")
            raise ValueError("Empty prompt provided")

        # Validate available VRAM
        if torch.cuda.is_available():
            free_memory = torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)
            if free_memory < 8 * 1024 * 1024 * 1024:  # 8GB minimum
                print("Warning: Low VRAM available, may affect generation quality")

        # Login to Hugging Face
        try:
            login(token=HF_TOKEN)
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with Hugging Face: {str(e)}")

        # Load Full Stable Diffusion XL Model Without Restrictions
        try:
            pipe = DiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                cache_dir="E:/huggingface",  # Store model cache in E:huggingface
                use_safetensors=True,
                safety_checker=None  # Remove any safety restrictions
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")

        # Move model to best available device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        pipe = pipe.to(device)
        
        # Enable memory efficient attention if using CUDA
        if device.type == "cuda":
            pipe.enable_model_cpu_offload()
            pipe.enable_sequential_cpu_offload()
            pipe.enable_xformers_memory_efficient_attention()
        
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        
        # Performance optimizations
        if device.type == "cpu":
            # CPU-specific optimizations
            pipe.enable_attention_slicing()
            pipe.enable_vae_slicing()
            pipe.enable_vae_tiling()
        else:
            # CUDA optimizations
            pipe.enable_attention_slicing()
            torch.backends.cudnn.benchmark = True
        
        # Check if PyTorch SDPA is available
        if hasattr(torch.nn.functional, 'scaled_dot_product_attention'):
            print("■ Using PyTorch SDPA for optimized attention")
        else:
            print("■ Using default attention (consider upgrading PyTorch)")
        
        # Generate the image with optimized settings
        seed = random.randint(0, sys.maxsize)
        image = pipe(
            prompt=prompt,
            num_inference_steps=50,  # Reduced steps for faster generation on CPU
            generator=torch.Generator().manual_seed(seed),
            height=512,  # Reduced resolution for CPU processing
            width=512
        ).images[0]

        # Convert to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()

        print(f"■ Prompt:\t{prompt}\n■ Seed:\t{seed}")
        print(f"■ Image generated and saved as bytes")

        return img_bytes

    except ValueError as ve:
        error_msg = f"Validation error: {str(ve)}"
        print(error_msg)
        raise ValueError(error_msg)
    except RuntimeError as re:
        error_msg = f"Runtime error: {str(re)}"
        print(error_msg)
        raise RuntimeError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during image generation: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)
    finally:
        try:
            if pipe is not None:
                # Free GPU memory
                del pipe
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
        except Exception as e:
            print(f"Warning: Failed to clean up resources: {str(e)}")

from enhance_prompt import enhance_prompt_initial, enhance_prompt_with_style, enhance_prompt_final

def generate_image_with_style(prompt, style):
    try:
        # Initial prompt enhancement
        enhanced_prompt = enhance_prompt_initial(prompt)
        
        # Style-specific enhancement
        styled_prompt = enhance_prompt_with_style(enhanced_prompt, style)
        
        # Final prompt refinement
        final_prompt = enhance_prompt_final(styled_prompt)

        # Generate the image with enhanced prompt
        image_bytes = generate_image(final_prompt)
        if not image_bytes:
            raise ValueError("Failed to generate image bytes")
        return image_bytes
    except Exception as e:
        print(f"Error in generate_image_with_style: {str(e)}")
        raise

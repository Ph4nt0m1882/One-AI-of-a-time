from huggingface_hub import InferenceClient
import json
import re
import os
from typing import Tuple, List

from tui import Spinner


DEFAULT_LLM = "Qwen/Qwen2.5-72B-Instruct"

def get_hf_client() -> InferenceClient:
    """Creates and returns a Hugging Face InferenceClient using the API token from environment variables."""
    token = os.getenv("HF_TOKEN")
    return InferenceClient(token=token)


def discover_models_via_LLM(
        objective: str,
        teacher_model: str|None = None,
        student_model: str|None = None,
) -> Tuple[str, str]:
    """
    Uses a language model to discover suitable teacher and student models based on the provided objective.
    
    Args:
        objective (str): The objective of the distillation process.
        teacher_model (str|None): Optional. The Hugging Face ID of the teacher model.
        student_model (str|None): Optional. The Hugging Face ID of the student model.
    
    Returns:
        Tuple[str, str]: A tuple containing the discovered teacher and student model IDs.
    """

    if teacher_model and student_model: # If both models are provided, return them directly without querying the LLM.
        return teacher_model, student_model

    client = get_hf_client() # Create a Hugging Face InferenceClient using the API token from environment variables.

    ## construct the prompt for the LLM based on the provided objective and any pre-selected models.
    prompt = ( 
        "You are an expert in AI model distillation and in Hugging Face models. "
        "I need some help to create a distilled AI model. "
        f"This model will have this objective: {objective} "
    )
    if teacher_model:
        prompt += f"I have already chosen the teacher model: {teacher_model}. "
        prompt += "Please suggest a suitable student model for this distillation process. "

    if student_model:
        prompt += f"I have already chosen the student model: {student_model}. "
        prompt += "Please suggest a suitable teacher model for this distillation process. "

    prompt += ( # Add instructions for the LLM to return the model suggestions in a specific JSON format.
        "Please provide your suggestions in the following JSON format: "
        '{"teacher_model": "model_id", "student_model": "model_id"} '
        "not in any other format and don't add any extra text. "
        "The model_id value should be the Hugging Face ID of the model, "
        'for example: "google/flan-t5-xl" or "facebook/opt-6.7b". '
        "The models do not necessarily have to be text generators."
    )

    try:

        spinner = Spinner("Discovering suitable models via LLM...")
        spinner.start()

        try:
            ## get the model suggestions from the LLM using the constructed prompt.
            response = client.chat_completion(
                model=DEFAULT_LLM,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.1 # dont be too creative, we want the most relevant models
            )

            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                content = json_match.group(0)
        finally:
            spinner.stop()
            print("Model discovery completed.")
            
        data = json.loads(content)
        teacher = data.get("teacher_model")
        student = data.get("student_model")
        
        if not (teacher or teacher_model) or not (student or student_model):
            raise ValueError("The returned JSON is incomplete.")
            
        return (teacher or teacher_model), (student or student_model)
    
    except Exception as e:
        print(f"Error during the LLM call: {e}")

        print("Using fallback text models.")
        return "meta-llama/Llama-3.3-70B-Instruct", "Qwen/Qwen2.5-1.5B"
    

def generate_synthetic_prompts(
        objective: str,
        num_prompts: int = 10,
) -> List[str]:
    """
    Uses a language model to generate synthetic prompts based on the provided objective.
    
    Args:
        objective (str): The objective of the distillation process.
        num_prompts (int): The number of synthetic prompts to generate. Default is 10.
    
    Returns:
        List[str]: A list of generated synthetic prompts.
    """

    client = get_hf_client() # Create a Hugging Face InferenceClient using the API token from environment variables.

    spinner = Spinner(f"Generating {num_prompts} synthetic prompts via LLM...")
    spinner.start()

    prompt = (
        "You are an expert in AI model distillation and in dataset generation. "
        "I need a dataset of synthetic prompts for distilling an AI model. "
        f"The objective of the distillation process is: {objective}. "
        f"Please generate {num_prompts} diverse and relevant prompts that align with this objective. "
        "Reply ONLY with a JSON array of strings. "
        "Example: [\"request 1\", \"request 2\"] "
    )

    try:
        response = client.chat_completion(
            model=DEFAULT_LLM,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7 # a bit more creative, we want diverse prompts
        )
        content = response.choices[0].message.content.strip()
        
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
            
        prompts = json.loads(content)
        if not isinstance(prompts, list):
            raise ValueError("The response is not a list.")
        return prompts
        
    except Exception as e:
        print(f"Error generating prompts: {e}")
        return [f"Generic example prompt for objective: {objective}"]
    finally:
        spinner.stop()




if __name__ == "__main__":
    # Example usage
    objective = "translate French texts into English"
    teacher_model, student_model = discover_models_via_LLM(objective)
    print(f"Discovered Teacher Model: {teacher_model}")
    print(f"Discovered Student Model: {student_model}")

    prompts = generate_synthetic_prompts(objective, num_prompts=5)
    print(f"Generated Prompts: {prompts}")

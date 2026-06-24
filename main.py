import os
import argparse
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

from src.hf_client import discover_models_via_LLM, generate_synthetic_prompts

load_dotenv()

def _create_parser() -> argparse.ArgumentParser:
    """Creates and returns an argument parser for the command-line tool."""
    parser = argparse.ArgumentParser(description="A command-line tool for distilling AI models.")
    
    parser.add_argument(
        "--objective",
        type=str,
        required=False,
        help="The objective of the distillation process."
    )

    parser.add_argument("--teacher", "--teacher", type=str, required=False, help="The Hugging Face ID of the teacher model.")
    parser.add_argument("--student", "--student", type=str, required=False, help="The Hugging Face ID of the student model.")

    parser.add_argument("--prompt-file", type=str, required=False, help="Path to a JSON file containing prompts for distillation.")
    parser.add_argument("--full-data", type=str, required=False, help="Path to a dataset file containing full data for distillation.")

    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()

    if not args.objective:
        args.objective = prompt(
            "Please enter the objective of the distillation process (Alt+Enter to submit):\n> ",
            multiline=True,
            placeholder=HTML('<style color="#969696">translate French texts into English</style>')
        )
        if not args.objective:
            exit("Objective is required. Exiting.")

    if not args.teacher or not args.student:
        teacher_model, student_model = discover_models_via_LLM(args.objective, args.teacher, args.student)
        print(f"Discovered Teacher Model: {teacher_model}")
        print(f"Discovered Student Model: {student_model}")

    prompts = generate_synthetic_prompts(args.objective, num_prompts=10)
    print(f"Generated Prompts: {prompts}")


if __name__ == "__main__":
    main()
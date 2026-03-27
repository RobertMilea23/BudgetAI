import os
from call_function import available_functions, call_function
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    

    parser = argparse.ArgumentParser(description="budgetAI")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    function_call_result = call_function()
    

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config = types.GenerateContentConfig(tools = [available_functions], system_instruction = system_prompt, temperature=0),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")


    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls != None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

            
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
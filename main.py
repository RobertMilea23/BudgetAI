import sys
sys.stdout.reconfigure(line_buffering=True)
import os
import time
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
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    while True:
        while True:
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=system_prompt,
                        temperature=0,
                    ),
                )
                break
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print("Rate limited, waiting 30 seconds...")
                    time.sleep(30)
                else:
                    raise

        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if not response.function_calls:
            print("Response:")
            print(response.text)
            break

        messages.append(response.candidates[0].content)

        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts")
            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Function call returned no function_response")
            if function_call_result.parts[0].function_response.response is None:
                raise RuntimeError("Function call returned no response")

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            function_results.append(function_call_result.parts[0])

        messages.append(types.Content(role="tool", parts=function_results))


if __name__ == "__main__":
    main()
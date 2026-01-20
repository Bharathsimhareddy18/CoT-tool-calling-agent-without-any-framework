import requests
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

client=OpenAI()

def get_crypto_prices(crypto_name : str ):
    url=f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code==200:
        return f"current price of {crypto_name} is {response.text}"
    
    return f"something went wrong"

SYSTEM_PROMPT = """
You are a Crypto Market Assistant. You help users check cryptocurrency prices.

You operate in a loop:
1. PLAN: You think about what to do.
2. TOOL: You select a tool to use.
3. OUTPUT: You give the final answer.

Available tools:
- get_crypto_price(crypto_name): Takes the coin name (e.g., 'bitcoin', 'ethereum') and returns price in USD.

RULES:
1. Always output in JSON format only.
2. The JSON key "step" MUST be one of: "PLAN", "TOOL", "OUTPUT".
3. Do not guess prices. Use the tool.

JSON FORMATS:
- For Thinking: { "step": "PLAN", "content": "Thinking about what to do..." }
- For Calling Tool: { "step": "TOOL", "tool": "get_crypto_price", "input": "bitcoin" }
- For Final Answer: { "step": "OUTPUT", "content": "The price is $95,000." }
"""



available_tools={
    "get_crypto_price":get_crypto_prices
}


user_input=input("enter the crypto name:")

messaged_history=[
    {"role":"system","content":SYSTEM_PROMPT}
]

messaged_history.append({"role":"user","content":user_input})

while True:
    response=client.chat.completions.create(
        model="gpt-4o",
        messages=messaged_history
    )
    
    raw_result=response.choices[0].message.content
    messaged_history.append({"role":"assistant","content":raw_result})
    parsed_result=json.loads(raw_result)
    
    
    if parsed_result.get("step")=="PLAN":
        print(f"Agent Plan :", parsed_result.get("content"))
        continue
        
    if parsed_result.get("step")=="TOOL":
        tool_to_call=parsed_result.get("tool")
        tool_input= parsed_result.get("input")
        print(f"Agent Action :{tool_to_call}({tool_input})")
        
        tool_response=available_tools[tool_to_call](tool_input)
        
        
        messaged_history.append(
            {"role":"developer","content":f"OBSERVATION: {tool_response}"}
        )
        continue
        
        
    if parsed_result.get("step")=="OUTPUT":
        print(f"Agent output :", parsed_result.get("content"))
        break
        
    
        
        
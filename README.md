# Crypto Price Agent

DIY ReAct agent for crypto prices. Uses OpenAI GPT-4o + CoinGecko API. Loops: PLAN -> TOOL (get price) -> OUTPUT. No frameworks, pure Python.

## How It Runs
- Asks for crypto name (bitcoin, ethereum, etc.).
- Agent thinks (PLAN), calls `getcryptoprice()` tool, then outputs USD price.
- Strict JSON loop: no guessing, always uses tool.[file:11]

Example:
```
user: bitcoin
Agent Plan: Thinking...
Agent Action: getcryptoprice bitcoin
Agent output: current price of bitcoin is $95,000
```

## Setup
1. `.env`: `OPENAI_API_KEY=your_key`
2. `pip install openai python-dotenv requests`
3. `python crypto_agent.py`

## Tools
- `getcryptoprice(name)`: Hits CoinGecko /simple/price API. Returns "current price of X is $Y" or error.[file:11]

## Notes
- GPT-4o parses agent JSON/steps.
- History in messages for context.
- Add more tools? Extend `availabletools` dict.
- Rate limits? CoinGecko free tier fine for testing.
- Prod: Error handling, caching, more coins.

Quick build for agentic AI practice. Expand to portfolio analysis or trades.[file:11]

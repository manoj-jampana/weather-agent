# Weather & Calculator AI Agent

This is a simple AI agent built using Python, LangChain, LangGraph, and Google Gemini.

The agent can:
- Get weather information for a city
- Perform basic calculations

## Technologies Used

- Python
- LangChain
- LangGraph
- Google Gemini
- Open-Meteo API

## How It Works

The user gives a question.

The agent uses Gemini to understand the question and chooses the required tool.

```text
User
  ↓
Agent
  ↓
Gemini
  ↓
Weather Tool / Calculator Tool
  ↓
Result
  ↓
User
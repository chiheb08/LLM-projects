from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.llm.base import LLM
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os 
from pathlib import Path  # For path handling
env_path = Path(__file__).resolve().parent.parent / ".env"


# Load environment variables from .env file
load_dotenv()



class PiNewsLetterConfig:
    def __init__(
            self,
            name: str,
            description: str, 
            instructions: list[str], 
            llm: LLM) -> None:
        self.name = name
        self.description = description
        self.instructions = instructions
        self.llm = llm

class PiNewsLetterAgent:
    def __init__(
            self,
            config: PiNewsLetterConfig,
            tools: list
        ):
        self.config = config
        self.tools = tools

    @property
    def agent(self):
        return Assistant(
            llm = self.config.llm,
            tools = self.tools,
            description = self.config.description,
            instructions = self.config.instructions
        )

config = PiNewsLetterConfig(
    name = "pi weekly newsletter",
    description = """
        Your task is to provide a concise summary of the most recent and relevant weekly news related to Raspberry Pi. 
        This includes any new hardware releases, software updates, community projects, educational resources, and significant discussions in forums or social media. 
        The summary should capture essential information and insights that would be valuable for Raspberry Pi enthusiasts and developers.
    """,
    instructions = [
        "Identify the most significant news items related to Raspberry Pi from the past week.",
        "Summarize each news item, focusing on key developments and their implications.",
        "Ensure that the summary is clear, concise, and free of jargon.",
        "Provide context for each news item to help understand its relevance and impact.",
        "Highlight any resources or links where readers can find more detailed information."
    ],
    llm = OpenAIChat(
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

agent = PiNewsLetterAgent(config, [DuckDuckGo()])
agent.agent.print_response("Summarise the last week news for raspberry pi.", markdown=True)
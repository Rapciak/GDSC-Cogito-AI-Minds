import dotenv

from src.static.ChatBedrockWrapper import ChatBedrockWrapper
from src.static.submission import Submission
from src.submission.crews.PIRLS_crew_solution import PIRLS_crew_with_charts

dotenv.load_dotenv()

def create_submission(call_id: str) -> Submission:
    llm = ChatBedrockWrapper(
        model_id='anthropic.claude-3-5-sonnet-20240620-v1:0',
        model_kwargs={'temperature': 0.01},
        call_id=call_id
    )

    crew = PIRLS_crew_with_charts(llm=llm)
    return crew

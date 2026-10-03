from pydantic import BaseModel


class TriageResult(BaseModel):

    category: str
    priority: str
    issue: str

class QAResult(BaseModel):
    approved: bool
    feedback: str
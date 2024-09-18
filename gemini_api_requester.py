import vertexai
from vertexai.generative_models import GenerativeModel


def init_vertex_ai(project_id: str, location: str):
    vertexai.init(project=project_id, location=location)


def generate_text_safety_config(project_id: str, location: str, question: str) -> str:
    init_vertex_ai(project_id, location)
    multimodal_model = GenerativeModel("gemini-1.0-pro-vision")
    response = multimodal_model.generate_content(question)
    return response.text


def generate_text(project_id: str, location: str, question: str) -> str:
    init_vertex_ai(project_id, location)
    multimodal_model = GenerativeModel("gemini-1.0-pro-vision")
    response = multimodal_model.generate_content(question)
    return response.text

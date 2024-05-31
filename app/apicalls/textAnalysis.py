import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
import json
import asyncio

vertexai.init(project="clean-linker-421304", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-preview-0514")

generation_config = {
    "max_output_tokens": 2248,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

emotion_categories = [
    "Positive", "Negative", "Neutral", "Optimistic", "Pessimistic", "Hopeful",
    "Despairing", "Enthusiastic", "Apathetic", "Confident", "Doubtful",
    "Excited", "Bored", "Content", "Frustrated", "Relaxed", "Tense",
    "Cheerful", "Gloomy", "Calm", "Agitated", "Eager", "Indifferent",
    "Joyful", "Melancholic"
]

tonality_categories = [
    "Positive", "Negative", "Neutral", "Optimistic", "Pessimistic", "Hopeful",
    "Despairing", "Enthusiastic", "Apathetic", "Confident", "Doubtful",
    "Excited", "Bored", "Content", "Frustrated", "Relaxed", "Tense",
    "Cheerful", "Gloomy", "Calm", "Agitated", "Eager", "Indifferent",
    "Joyful", "Melancholic"
]

async def generate_content(text):
    responses = model.generate_content(
        [text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    full_response = ""
    for response in responses:
        full_response += response.text

    return full_response

async def analyze_text(text_to_analyze):
    text = f"""
    Please analyze the following text for spelling mistakes, grammar mistakes, emotions, and tonality, and provide the result in JSON format with the structure:
    {{
      "spell_mistakes": {{
        "errors_count": <number of spelling mistakes>,
        "errors_word": ["list of misspelled words"],
        "explanations": ["list of explanations for misspelled words"]
      }},
      "grammar_mistakes": {{
        "errors_count": <number of grammar mistakes>,
        "errors_word": ["list of grammar mistakes"],
        "explanations": ["list of explanations for grammar mistakes"]
      }},
      "emotion": {{
        "categories": {json.dumps(emotion_categories)},
        "scores": [],
        "explanations": []
      }},
      "tonality": {{
        "categories": {json.dumps(tonality_categories)},
        "scores": [],
        "explanations": []
      }}
    }}

    Only include emotion and tonality categories with non-zero scores and provide explanations only for those categories.
    Text to analyze:
    {text_to_analyze}
    """
    result = await generate_content(text)
    return result

""" async def mycall():
    text = "I'm selfish, impatient and a little insecure. I make mistakes, I am out of control and at times hard to handle. But if you can't handle me at my worst, then you sure as hell don't deserve me at my best."
    
    result = await analyze_text(text)
    print("Analysis Result:", result)

# Run the asynchronous function
asyncio.run(mycall()) """

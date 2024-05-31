def filter_data(data):
    # Filter emotion categories
    filtered_emotion = {
        "categories": [],
        "scores": [],
        "explanations": []
    }
    
    for category, score, explanation in zip(data["emotion"]["categories"], data["emotion"]["scores"], data["emotion"]["explanations"]):
        if score > 0 or explanation:
            filtered_emotion["categories"].append(category)
            filtered_emotion["scores"].append(score)
            filtered_emotion["explanations"].append(explanation)
    
    # Filter tonality categories
    filtered_tonality = {
        "categories": [],
        "scores": [],
        "explanations": []
    }
    
    for category, score, explanation in zip(data["tonality"]["categories"], data["tonality"]["scores"], data["tonality"]["explanations"]):
        if score > 0 or explanation:
            filtered_tonality["categories"].append(category)
            filtered_tonality["scores"].append(score)
            filtered_tonality["explanations"].append(explanation)
    
    # Create new filtered data
    filtered_data = {
        "spell_mistakes": data["spell_mistakes"],
        "grammar_mistakes": data["grammar_mistakes"],
        "emotion": filtered_emotion,
        "tonality": filtered_tonality
    }
    
    return filtered_data
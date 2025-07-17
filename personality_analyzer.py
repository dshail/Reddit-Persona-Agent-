import re
from typing import Dict, List
from collections import Counter

def analyze_big_five_personality(user_data: Dict) -> Dict:
    """
    Analyze Big Five personality traits based on language patterns and content.
    The Big Five: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
    """
    results = {
        'personality_scores': {},
        'trait_indicators': {},
        'personality_profile': {},
        'dominant_traits': [],
        'personality_insights': []
    }
    
    # Combine all text content
    all_texts = []
    for section, items in user_data.items():
        for item in items:
            all_texts.append(item['text'])
    
    if not all_texts:
        return results
    
    # Analyze each personality dimension
    results['personality_scores']['openness'] = analyze_openness(all_texts)
    results['personality_scores']['conscientiousness'] = analyze_conscientiousness(all_texts)
    results['personality_scores']['extraversion'] = analyze_extraversion(all_texts)
    results['personality_scores']['agreeableness'] = analyze_agreeableness(all_texts)
    results['personality_scores']['neuroticism'] = analyze_neuroticism(all_texts)
    
    # Generate trait indicators
    results['trait_indicators'] = generate_trait_indicators(all_texts)
    
    # Create personality profile
    results['personality_profile'] = create_personality_profile(results['personality_scores'])
    
    # Identify dominant traits
    results['dominant_traits'] = identify_dominant_traits(results['personality_scores'])
    
    # Generate insights
    results['personality_insights'] = generate_personality_insights(results)
    
    return results

def analyze_openness(texts: List[str]) -> Dict:
    """
    Analyze Openness to Experience - creativity, curiosity, intellectual interests.
    """
    openness_indicators = {
        'creativity_words': ['creative', 'innovative', 'original', 'artistic', 'imagination', 'design', 'art', 'music'],
        'curiosity_words': ['curious', 'wonder', 'explore', 'discover', 'learn', 'research', 'investigate', 'question'],
        'intellectual_words': ['philosophy', 'theory', 'concept', 'abstract', 'complex', 'analysis', 'intellectual', 'academic'],
        'novelty_words': ['new', 'different', 'unique', 'unusual', 'strange', 'weird', 'interesting', 'fascinating'],
        'change_words': ['change', 'transform', 'evolve', 'adapt', 'experiment', 'try', 'alternative', 'variety']
    }
    
    scores = {}
    total_words = 0
    
    for category, words in openness_indicators.items():
        count = 0
        for text in texts:
            text_lower = text.lower()
            total_words += len(text_lower.split())
            count += sum(1 for word in words if word in text_lower)
        scores[category] = count
    
    # Calculate overall openness score
    total_openness_indicators = sum(scores.values())
    openness_score = min(100, (total_openness_indicators / len(texts)) * 10) if texts else 0
    
    return {
        'score': openness_score,
        'indicators': scores,
        'level': 'high' if openness_score > 60 else 'medium' if openness_score > 30 else 'low'
    }

def analyze_conscientiousness(texts: List[str]) -> Dict:
    """
    Analyze Conscientiousness - organization, discipline, goal-orientation.
    """
    conscientiousness_indicators = {
        'organization_words': ['organize', 'plan', 'schedule', 'structure', 'system', 'method', 'order', 'arrange'],
        'discipline_words': ['discipline', 'control', 'focus', 'dedicated', 'committed', 'persistent', 'determined'],
        'goal_words': ['goal', 'objective', 'target', 'aim', 'achieve', 'accomplish', 'complete', 'finish'],
        'responsibility_words': ['responsible', 'duty', 'obligation', 'reliable', 'dependable', 'accountable'],
        'detail_words': ['detail', 'careful', 'thorough', 'precise', 'accurate', 'exact', 'specific', 'meticulous']
    }
    
    scores = {}
    
    for category, words in conscientiousness_indicators.items():
        count = 0
        for text in texts:
            text_lower = text.lower()
            count += sum(1 for word in words if word in text_lower)
        scores[category] = count
    
    # Look for structured writing patterns
    structure_score = 0
    for text in texts:
        # Check for lists, numbered points, organized structure
        if re.search(r'\d+\.|\*|\-', text):
            structure_score += 1
        if len(text) > 200 and text.count('\n') > 2:  # Well-structured longer posts
            structure_score += 1
    
    scores['structure_patterns'] = structure_score
    
    total_conscientiousness_indicators = sum(scores.values())
    conscientiousness_score = min(100, (total_conscientiousness_indicators / len(texts)) * 8) if texts else 0
    
    return {
        'score': conscientiousness_score,
        'indicators': scores,
        'level': 'high' if conscientiousness_score > 60 else 'medium' if conscientiousness_score > 30 else 'low'
    }

def analyze_extraversion(texts: List[str]) -> Dict:
    """
    Analyze Extraversion - sociability, assertiveness, energy.
    """
    extraversion_indicators = {
        'social_words': ['friends', 'party', 'social', 'people', 'group', 'team', 'community', 'together'],
        'assertive_words': ['confident', 'assert', 'lead', 'direct', 'bold', 'strong', 'powerful', 'dominant'],
        'energy_words': ['excited', 'enthusiastic', 'energetic', 'active', 'dynamic', 'vibrant', 'lively'],
        'communication_words': ['talk', 'speak', 'discuss', 'share', 'tell', 'communicate', 'express', 'voice'],
        'positive_emotion_words': ['happy', 'joy', 'fun', 'great', 'awesome', 'amazing', 'fantastic', 'wonderful']
    }
    
    scores = {}
    
    for category, words in extraversion_indicators.items():
        count = 0
        for text in texts:
            text_lower = text.lower()
            count += sum(1 for word in words if word in text_lower)
        scores[category] = count
    
    # Check for interaction patterns
    interaction_score = 0
    for text in texts:
        # Questions to others
        if '?' in text and any(word in text.lower() for word in ['you', 'anyone', 'everyone', 'somebody']):
            interaction_score += 1
        # Exclamation points (enthusiasm)
        interaction_score += text.count('!')
        # Direct address
        if text.lower().startswith(('hey', 'hi', 'hello')):
            interaction_score += 1
    
    scores['interaction_patterns'] = interaction_score
    
    total_extraversion_indicators = sum(scores.values())
    extraversion_score = min(100, (total_extraversion_indicators / len(texts)) * 6) if texts else 0
    
    return {
        'score': extraversion_score,
        'indicators': scores,
        'level': 'high' if extraversion_score > 60 else 'medium' if extraversion_score > 30 else 'low'
    }

def analyze_agreeableness(texts: List[str]) -> Dict:
    """
    Analyze Agreeableness - cooperation, trust, empathy.
    """
    agreeableness_indicators = {
        'cooperative_words': ['agree', 'cooperate', 'collaborate', 'together', 'team', 'help', 'support', 'assist'],
        'empathy_words': ['understand', 'feel', 'empathy', 'compassion', 'care', 'concern', 'sympathy', 'sorry'],
        'positive_social_words': ['kind', 'nice', 'friendly', 'warm', 'gentle', 'considerate', 'thoughtful'],
        'trust_words': ['trust', 'honest', 'sincere', 'genuine', 'authentic', 'reliable', 'faithful'],
        'harmony_words': ['peace', 'harmony', 'balance', 'calm', 'smooth', 'pleasant', 'comfortable']
    }
    
    scores = {}
    
    for category, words in agreeableness_indicators.items():
        count = 0
        for text in texts:
            text_lower = text.lower()
            count += sum(1 for word in words if word in text_lower)
        scores[category] = count
    
    # Check for polite language patterns
    politeness_score = 0
    polite_phrases = ['please', 'thank you', 'thanks', 'sorry', 'excuse me', 'pardon', 'appreciate']
    
    for text in texts:
        text_lower = text.lower()
        politeness_score += sum(1 for phrase in polite_phrases if phrase in text_lower)
        
        # Avoid confrontational language
        confrontational = ['wrong', 'stupid', 'idiot', 'hate', 'terrible', 'awful']
        if not any(word in text_lower for word in confrontational):
            politeness_score += 0.5
    
    scores['politeness_patterns'] = int(politeness_score)
    
    total_agreeableness_indicators = sum(scores.values())
    agreeableness_score = min(100, (total_agreeableness_indicators / len(texts)) * 7) if texts else 0
    
    return {
        'score': agreeableness_score,
        'indicators': scores,
        'level': 'high' if agreeableness_score > 60 else 'medium' if agreeableness_score > 30 else 'low'
    }

def analyze_neuroticism(texts: List[str]) -> Dict:
    """
    Analyze Neuroticism - emotional instability, anxiety, stress.
    """
    neuroticism_indicators = {
        'anxiety_words': ['anxious', 'worried', 'nervous', 'stress', 'panic', 'fear', 'scared', 'afraid'],
        'negative_emotion_words': ['sad', 'depressed', 'upset', 'angry', 'frustrated', 'annoyed', 'irritated'],
        'instability_words': ['unstable', 'chaotic', 'confused', 'overwhelmed', 'lost', 'helpless', 'hopeless'],
        'self_doubt_words': ['doubt', 'insecure', 'uncertain', 'unsure', 'question', 'worry', 'concern'],
        'catastrophic_words': ['disaster', 'terrible', 'awful', 'horrible', 'worst', 'nightmare', 'crisis']
    }
    
    scores = {}
    
    for category, words in neuroticism_indicators.items():
        count = 0
        for text in texts:
            text_lower = text.lower()
            count += sum(1 for word in words if word in text_lower)
        scores[category] = count
    
    # Check for emotional language patterns
    emotional_intensity_score = 0
    for text in texts:
        # Multiple exclamation points or question marks
        emotional_intensity_score += len(re.findall(r'[!?]{2,}', text))
        
        # All caps words (shouting)
        caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
        emotional_intensity_score += len(caps_words)
        
        # Emotional punctuation
        emotional_intensity_score += text.count('...') * 0.5
    
    scores['emotional_intensity'] = int(emotional_intensity_score)
    
    total_neuroticism_indicators = sum(scores.values())
    neuroticism_score = min(100, (total_neuroticism_indicators / len(texts)) * 8) if texts else 0
    
    return {
        'score': neuroticism_score,
        'indicators': scores,
        'level': 'high' if neuroticism_score > 60 else 'medium' if neuroticism_score > 30 else 'low'
    }

def generate_trait_indicators(texts: List[str]) -> Dict:
    """
    Generate specific behavioral indicators for each trait.
    """
    indicators = {
        'openness': [],
        'conscientiousness': [],
        'extraversion': [],
        'agreeableness': [],
        'neuroticism': []
    }
    
    combined_text = ' '.join(texts).lower()
    
    # Openness indicators
    if 'creative' in combined_text or 'art' in combined_text:
        indicators['openness'].append("Shows interest in creative activities")
    if 'learn' in combined_text or 'curious' in combined_text:
        indicators['openness'].append("Demonstrates curiosity and learning orientation")
    
    # Conscientiousness indicators
    if any(word in combined_text for word in ['plan', 'organize', 'schedule']):
        indicators['conscientiousness'].append("Shows planning and organizational tendencies")
    if any(word in combined_text for word in ['goal', 'achieve', 'complete']):
        indicators['conscientiousness'].append("Demonstrates goal-oriented behavior")
    
    # Extraversion indicators
    if any(word in combined_text for word in ['friends', 'party', 'social']):
        indicators['extraversion'].append("Shows social engagement preferences")
    if combined_text.count('!') > len(texts):
        indicators['extraversion'].append("Uses enthusiastic language patterns")
    
    # Agreeableness indicators
    if any(word in combined_text for word in ['help', 'support', 'care']):
        indicators['agreeableness'].append("Shows helping and supportive behavior")
    if any(word in combined_text for word in ['thank', 'please', 'sorry']):
        indicators['agreeableness'].append("Uses polite and considerate language")
    
    # Neuroticism indicators
    if any(word in combined_text for word in ['stress', 'worry', 'anxious']):
        indicators['neuroticism'].append("Expresses stress and anxiety concerns")
    if any(word in combined_text for word in ['terrible', 'awful', 'worst']):
        indicators['neuroticism'].append("Uses emotionally intense negative language")
    
    return indicators

def create_personality_profile(scores: Dict) -> Dict:
    """
    Create a comprehensive personality profile.
    """
    profile = {}
    
    for trait, data in scores.items():
        score = data['score']
        level = data['level']
        
        profile[trait] = {
            'score': score,
            'level': level,
            'percentile': min(99, max(1, int(score))),
            'description': get_trait_description(trait, level)
        }
    
    return profile

def get_trait_description(trait: str, level: str) -> str:
    """
    Get description for each trait level.
    """
    descriptions = {
        'openness': {
            'high': 'Creative, curious, and open to new experiences',
            'medium': 'Moderately open to new ideas and experiences',
            'low': 'Prefers familiar routines and conventional approaches'
        },
        'conscientiousness': {
            'high': 'Organized, disciplined, and goal-oriented',
            'medium': 'Reasonably organized with moderate self-discipline',
            'low': 'More spontaneous and flexible in approach'
        },
        'extraversion': {
            'high': 'Outgoing, energetic, and socially engaged',
            'medium': 'Balanced between social and solitary activities',
            'low': 'More reserved and prefers quieter environments'
        },
        'agreeableness': {
            'high': 'Cooperative, trusting, and empathetic',
            'medium': 'Generally cooperative with balanced skepticism',
            'low': 'More competitive and skeptical of others'
        },
        'neuroticism': {
            'high': 'More emotionally reactive and stress-sensitive',
            'medium': 'Moderate emotional stability',
            'low': 'Emotionally stable and resilient'
        }
    }
    
    return descriptions.get(trait, {}).get(level, 'No description available')

def identify_dominant_traits(scores: Dict) -> List[str]:
    """
    Identify the most prominent personality traits.
    """
    trait_scores = [(trait, data['score']) for trait, data in scores.items()]
    trait_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 2-3 traits that are significantly higher
    dominant = []
    for i, (trait, score) in enumerate(trait_scores):
        if i < 2 or (i < 3 and score > 50):
            dominant.append(trait)
    
    return dominant

def generate_personality_insights(results: Dict) -> List[str]:
    """
    Generate human-readable personality insights.
    """
    insights = []
    
    profile = results.get('personality_profile', {})
    dominant_traits = results.get('dominant_traits', [])
    
    # Overall personality summary
    if dominant_traits:
        trait_names = [trait.replace('_', ' ').title() for trait in dominant_traits]
        insights.append(f"Dominant personality traits: {', '.join(trait_names)}")
    
    # Specific trait insights
    for trait, data in profile.items():
        level = data['level']
        score = data['score']
        
        if level == 'high' and score > 70:
            trait_name = trait.replace('_', ' ').title()
            insights.append(f"Shows strong {trait_name}: {data['description']}")
    
    # Behavioral predictions
    openness_score = profile.get('openness', {}).get('score', 0)
    conscientiousness_score = profile.get('conscientiousness', {}).get('score', 0)
    
    if openness_score > 60 and conscientiousness_score > 60:
        insights.append("Likely to be innovative while maintaining organized approach")
    
    extraversion_score = profile.get('extraversion', {}).get('score', 0)
    agreeableness_score = profile.get('agreeableness', {}).get('score', 0)
    
    if extraversion_score > 60 and agreeableness_score > 60:
        insights.append("Tends to be socially engaging and collaborative")
    
    neuroticism_score = profile.get('neuroticism', {}).get('score', 0)
    if neuroticism_score < 30:
        insights.append("Demonstrates emotional stability and resilience")
    elif neuroticism_score > 70:
        insights.append("May be more sensitive to stress and emotional challenges")
    
    return insights
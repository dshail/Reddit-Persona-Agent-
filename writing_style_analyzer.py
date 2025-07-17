import re
import string
from typing import Dict, List
from collections import Counter
import statistics

def analyze_writing_style(user_data: Dict) -> Dict:
    """
    Comprehensive writing style analysis including linguistic patterns,
    vocabulary complexity, and communication style.
    """
    results = {
        'linguistic_metrics': {},
        'vocabulary_analysis': {},
        'punctuation_patterns': {},
        'formality_analysis': {},
        'communication_style': {},
        'writing_insights': []
    }
    
    # Combine all text content
    all_texts = []
    for section, items in user_data.items():
        for item in items:
            all_texts.append(item['text'])
    
    if not all_texts:
        return results
    
    # Analyze linguistic metrics
    results['linguistic_metrics'] = analyze_linguistic_metrics(all_texts)
    
    # Vocabulary analysis
    results['vocabulary_analysis'] = analyze_vocabulary_complexity(all_texts)
    
    # Punctuation patterns
    results['punctuation_patterns'] = analyze_punctuation_usage(all_texts)
    
    # Formality analysis
    results['formality_analysis'] = analyze_formality_level(all_texts)
    
    # Communication style
    results['communication_style'] = analyze_communication_style(all_texts)
    
    # Generate insights
    results['writing_insights'] = generate_writing_insights(results)
    
    return results

def analyze_linguistic_metrics(texts: List[str]) -> Dict:
    """
    Analyze basic linguistic metrics like sentence length, word count, etc.
    """
    metrics = {
        'avg_sentence_length': 0,
        'avg_word_length': 0,
        'sentences_per_post': 0,
        'words_per_post': 0,
        'readability_score': 0
    }
    
    all_sentences = []
    all_words = []
    
    for text in texts:
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        all_sentences.extend(sentences)
        
        # Split into words
        words = re.findall(r'\b\w+\b', text.lower())
        all_words.extend(words)
    
    if all_sentences:
        sentence_lengths = [len(s.split()) for s in all_sentences]
        metrics['avg_sentence_length'] = statistics.mean(sentence_lengths)
        metrics['sentences_per_post'] = len(all_sentences) / len(texts)
    
    if all_words:
        word_lengths = [len(word) for word in all_words]
        metrics['avg_word_length'] = statistics.mean(word_lengths)
        metrics['words_per_post'] = len(all_words) / len(texts)
        
        # Simple readability score (Flesch-like)
        avg_sentence_len = metrics['avg_sentence_length']
        avg_word_len = metrics['avg_word_length']
        metrics['readability_score'] = 206.835 - (1.015 * avg_sentence_len) - (84.6 * (avg_word_len / 4.7))
    
    return metrics

def analyze_vocabulary_complexity(texts: List[str]) -> Dict:
    """
    Analyze vocabulary richness and complexity.
    """
    analysis = {
        'unique_words': 0,
        'vocabulary_richness': 0,
        'complex_words_ratio': 0,
        'most_common_words': [],
        'rare_words_count': 0
    }
    
    all_words = []
    for text in texts:
        words = re.findall(r'\b\w+\b', text.lower())
        all_words.extend(words)
    
    if not all_words:
        return analysis
    
    word_counts = Counter(all_words)
    unique_words = len(word_counts)
    total_words = len(all_words)
    
    analysis['unique_words'] = unique_words
    analysis['vocabulary_richness'] = unique_words / total_words if total_words > 0 else 0
    
    # Complex words (more than 6 characters)
    complex_words = [word for word in all_words if len(word) > 6]
    analysis['complex_words_ratio'] = len(complex_words) / total_words if total_words > 0 else 0
    
    # Most common words (excluding common stop words)
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'a', 'an'}
    
    filtered_words = {word: count for word, count in word_counts.items() 
                     if word not in stop_words and len(word) > 2}
    analysis['most_common_words'] = list(Counter(filtered_words).most_common(10))
    
    # Rare words (appearing only once)
    analysis['rare_words_count'] = sum(1 for count in word_counts.values() if count == 1)
    
    return analysis

def analyze_punctuation_usage(texts: List[str]) -> Dict:
    """
    Analyze punctuation and special character usage patterns.
    """
    patterns = {
        'exclamation_ratio': 0,
        'question_ratio': 0,
        'ellipsis_usage': 0,
        'emoji_usage': 0,
        'caps_usage': 0,
        'punctuation_density': 0
    }
    
    total_chars = 0
    exclamations = 0
    questions = 0
    ellipses = 0
    emojis = 0
    caps_words = 0
    total_words = 0
    punctuation_count = 0
    
    # Emoji pattern (basic)
    emoji_pattern = re.compile(r'[😀-🙏🌀-🗿🚀-🛿🇀-🇿]+')
    
    for text in texts:
        total_chars += len(text)
        exclamations += text.count('!')
        questions += text.count('?')
        ellipses += text.count('...')
        emojis += len(emoji_pattern.findall(text))
        
        # Count punctuation
        punctuation_count += sum(1 for char in text if char in string.punctuation)
        
        # Count capitalized words
        words = text.split()
        total_words += len(words)
        caps_words += sum(1 for word in words if word.isupper() and len(word) > 1)
    
    if total_chars > 0:
        patterns['exclamation_ratio'] = exclamations / total_chars
        patterns['question_ratio'] = questions / total_chars
        patterns['ellipsis_usage'] = ellipses / len(texts)
        patterns['emoji_usage'] = emojis / len(texts)
        patterns['punctuation_density'] = punctuation_count / total_chars
    
    if total_words > 0:
        patterns['caps_usage'] = caps_words / total_words
    
    return patterns

def analyze_formality_level(texts: List[str]) -> Dict:
    """
    Analyze the formality level of writing.
    """
    formality = {
        'formality_score': 0,
        'contractions_ratio': 0,
        'slang_usage': 0,
        'formal_words_ratio': 0,
        'formality_level': 'neutral'
    }
    
    # Common contractions
    contractions = ["don't", "won't", "can't", "shouldn't", "wouldn't", "couldn't", 
                   "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't",
                   "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
                   "i'll", "you'll", "he'll", "she'll", "it'll", "we'll", "they'll"]
    
    # Formal words
    formal_words = ["therefore", "however", "furthermore", "moreover", "consequently",
                   "nevertheless", "nonetheless", "accordingly", "subsequently", "thus",
                   "hence", "indeed", "certainly", "particularly", "specifically"]
    
    # Slang/informal words
    slang_words = ["lol", "omg", "wtf", "tbh", "imo", "imho", "fyi", "btw", "afaik",
                  "gonna", "wanna", "gotta", "kinda", "sorta", "yeah", "nah", "yep"]
    
    total_words = 0
    contraction_count = 0
    formal_count = 0
    slang_count = 0
    
    for text in texts:
        words = re.findall(r'\b\w+\b', text.lower())
        total_words += len(words)
        
        text_lower = text.lower()
        contraction_count += sum(1 for contraction in contractions if contraction in text_lower)
        formal_count += sum(1 for formal in formal_words if formal in text_lower)
        slang_count += sum(1 for slang in slang_words if slang in text_lower)
    
    if total_words > 0:
        formality['contractions_ratio'] = contraction_count / total_words
        formality['formal_words_ratio'] = formal_count / total_words
        formality['slang_usage'] = slang_count / total_words
        
        # Calculate formality score
        formality_score = (formal_count * 2) - (contraction_count + slang_count * 2)
        formality['formality_score'] = formality_score / total_words if total_words > 0 else 0
        
        # Determine formality level
        if formality['formality_score'] > 0.01:
            formality['formality_level'] = 'formal'
        elif formality['formality_score'] < -0.01:
            formality['formality_level'] = 'informal'
        else:
            formality['formality_level'] = 'neutral'
    
    return formality

def analyze_communication_style(texts: List[str]) -> Dict:
    """
    Analyze overall communication style and patterns.
    """
    style = {
        'assertiveness': 0,
        'politeness': 0,
        'enthusiasm': 0,
        'analytical_tendency': 0,
        'storytelling_tendency': 0,
        'question_asking_tendency': 0
    }
    
    # Assertive words/phrases
    assertive_patterns = ["i think", "i believe", "in my opinion", "clearly", "obviously", 
                         "definitely", "absolutely", "certainly", "must", "should"]
    
    # Polite words/phrases
    polite_patterns = ["please", "thank you", "thanks", "sorry", "excuse me", 
                      "would you", "could you", "may i", "if you don't mind"]
    
    # Enthusiastic words/phrases
    enthusiastic_patterns = ["amazing", "awesome", "fantastic", "incredible", "love", 
                           "excited", "thrilled", "wonderful", "brilliant", "excellent"]
    
    # Analytical words/phrases
    analytical_patterns = ["analysis", "data", "research", "study", "evidence", 
                          "statistics", "conclusion", "hypothesis", "methodology"]
    
    # Storytelling indicators
    storytelling_patterns = ["story", "happened", "experience", "remember", "once", 
                           "suddenly", "then", "after", "before", "during"]
    
    total_texts = len(texts)
    
    for text in texts:
        text_lower = text.lower()
        
        # Count pattern occurrences
        style['assertiveness'] += sum(1 for pattern in assertive_patterns if pattern in text_lower)
        style['politeness'] += sum(1 for pattern in polite_patterns if pattern in text_lower)
        style['enthusiasm'] += sum(1 for pattern in enthusiastic_patterns if pattern in text_lower)
        style['analytical_tendency'] += sum(1 for pattern in analytical_patterns if pattern in text_lower)
        style['storytelling_tendency'] += sum(1 for pattern in storytelling_patterns if pattern in text_lower)
        
        # Count questions
        style['question_asking_tendency'] += text.count('?')
    
    # Normalize by number of texts
    for key in style:
        style[key] = style[key] / total_texts if total_texts > 0 else 0
    
    return style

def generate_writing_insights(results: Dict) -> List[str]:
    """
    Generate human-readable insights from writing style analysis.
    """
    insights = []
    
    # Linguistic insights
    metrics = results.get('linguistic_metrics', {})
    if metrics.get('avg_sentence_length', 0) > 20:
        insights.append("Tends to write in long, complex sentences")
    elif metrics.get('avg_sentence_length', 0) < 10:
        insights.append("Prefers short, concise sentences")
    
    if metrics.get('readability_score', 0) > 60:
        insights.append("Writing is generally easy to read")
    elif metrics.get('readability_score', 0) < 30:
        insights.append("Writing tends to be complex and challenging")
    
    # Vocabulary insights
    vocab = results.get('vocabulary_analysis', {})
    if vocab.get('vocabulary_richness', 0) > 0.7:
        insights.append("Uses a rich and diverse vocabulary")
    elif vocab.get('vocabulary_richness', 0) < 0.3:
        insights.append("Tends to repeat common words and phrases")
    
    if vocab.get('complex_words_ratio', 0) > 0.2:
        insights.append("Frequently uses sophisticated vocabulary")
    
    # Formality insights
    formality = results.get('formality_analysis', {})
    if formality.get('formality_level') == 'formal':
        insights.append("Maintains a formal writing style")
    elif formality.get('formality_level') == 'informal':
        insights.append("Uses casual, conversational language")
    
    # Communication style insights
    comm_style = results.get('communication_style', {})
    if comm_style.get('enthusiasm', 0) > 1:
        insights.append("Shows high enthusiasm in communication")
    
    if comm_style.get('question_asking_tendency', 0) > 2:
        insights.append("Frequently asks questions and seeks input")
    
    if comm_style.get('analytical_tendency', 0) > 0.5:
        insights.append("Demonstrates analytical thinking patterns")
    
    if comm_style.get('storytelling_tendency', 0) > 1:
        insights.append("Often shares personal experiences and stories")
    
    # Punctuation insights
    punct = results.get('punctuation_patterns', {})
    if punct.get('exclamation_ratio', 0) > 0.01:
        insights.append("Uses exclamation points frequently for emphasis")
    
    if punct.get('emoji_usage', 0) > 1:
        insights.append("Regularly incorporates emojis in communication")
    
    return insights
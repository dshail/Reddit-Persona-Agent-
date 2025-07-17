import re
from typing import Dict, List, Tuple
from datetime import datetime
import pandas as pd
from collections import Counter, defaultdict

def analyze_sentiment_and_behavior(user_data: Dict) -> Dict:
    """
    Analyze sentiment, emotions, and behavioral patterns from user data.
    """
    results = {
        'sentiment_scores': [],
        'emotion_analysis': {},
        'behavioral_patterns': {},
        'activity_timeline': [],
        'subreddit_analysis': {},
        'engagement_patterns': {}
    }
    
    # Combine all text content
    all_content = []
    for section, items in user_data.items():
        for item in items:
            all_content.append({
                'text': item['text'],
                'type': section,
                'permalink': item['permalink']
            })
    
    # Analyze sentiment using keyword-based approach
    results['sentiment_scores'] = analyze_sentiment_keywords(all_content)
    
    # Analyze emotions
    results['emotion_analysis'] = analyze_emotions(all_content)
    
    # Behavioral pattern detection
    results['behavioral_patterns'] = detect_behavioral_patterns(all_content)
    
    # Subreddit analysis
    results['subreddit_analysis'] = analyze_subreddit_patterns(all_content)
    
    # Engagement patterns
    results['engagement_patterns'] = analyze_engagement_patterns(all_content)
    
    return results

def analyze_sentiment_keywords(content: List[Dict]) -> List[Dict]:
    """Simple keyword-based sentiment analysis."""
    positive_words = ['love', 'great', 'awesome', 'amazing', 'excellent', 'fantastic', 
                     'wonderful', 'good', 'best', 'happy', 'excited', 'perfect']
    negative_words = ['hate', 'terrible', 'awful', 'bad', 'worst', 'horrible', 
                     'disgusting', 'annoying', 'frustrated', 'angry', 'disappointed']
    
    sentiment_scores = []
    for item in content:
        text = item['text'].lower()
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count + neg_count > 0:
            sentiment = (pos_count - neg_count) / (pos_count + neg_count)
        else:
            sentiment = 0
            
        sentiment_scores.append({
            'text_preview': item['text'][:100],
            'sentiment': sentiment,
            'type': item['type']
        })
    
    return sentiment_scores

def analyze_emotions(content: List[Dict]) -> Dict:
    """Analyze emotional patterns in content."""
    emotion_keywords = {
        'joy': ['happy', 'excited', 'thrilled', 'delighted', 'cheerful', 'joyful'],
        'anger': ['angry', 'furious', 'mad', 'irritated', 'annoyed', 'frustrated'],
        'sadness': ['sad', 'depressed', 'disappointed', 'upset', 'down', 'blue'],
        'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified'],
        'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
        'disgust': ['disgusted', 'revolted', 'sick', 'nauseated', 'repulsed']
    }
    
    emotion_counts = defaultdict(int)
    total_texts = len(content)
    
    for item in content:
        text = item['text'].lower()
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                emotion_counts[emotion] += 1
    
    # Convert to percentages
    emotion_percentages = {
        emotion: (count / total_texts) * 100 
        for emotion, count in emotion_counts.items()
    }
    
    return emotion_percentages

def detect_behavioral_patterns(content: List[Dict]) -> Dict:
    """Detect behavioral patterns from content."""
    patterns = {
        'question_asker': 0,
        'advice_giver': 0,
        'storyteller': 0,
        'debater': 0,
        'supporter': 0
    }
    
    for item in content:
        text = item['text'].lower()
        
        # Question asker
        if '?' in text or text.startswith(('how', 'what', 'why', 'when', 'where', 'who')):
            patterns['question_asker'] += 1
            
        # Advice giver
        if any(phrase in text for phrase in ['you should', 'try this', 'i recommend', 'advice']):
            patterns['advice_giver'] += 1
            
        # Storyteller
        if len(text) > 200 and any(phrase in text for phrase in ['story', 'happened', 'experience']):
            patterns['storyteller'] += 1
            
        # Debater
        if any(phrase in text for phrase in ['disagree', 'wrong', 'actually', 'however', 'but']):
            patterns['debater'] += 1
            
        # Supporter
        if any(phrase in text for phrase in ['agree', 'exactly', 'this', 'support', 'yes']):
            patterns['supporter'] += 1
    
    total = len(content)
    return {k: (v/total)*100 for k, v in patterns.items()}

def analyze_subreddit_patterns(content: List[Dict]) -> Dict:
    """Analyze subreddit engagement patterns."""
    subreddit_pattern = r'/r/(\w+)'
    subreddits = []
    
    for item in content:
        matches = re.findall(subreddit_pattern, item['permalink'])
        subreddits.extend(matches)
    
    subreddit_counts = Counter(subreddits)
    return dict(subreddit_counts.most_common(10))

def analyze_engagement_patterns(content: List[Dict]) -> Dict:
    """Analyze engagement patterns."""
    post_lengths = []
    comment_lengths = []
    
    for item in content:
        length = len(item['text'])
        if item['type'] == 'posts':
            post_lengths.append(length)
        else:
            comment_lengths.append(length)
    
    return {
        'avg_post_length': sum(post_lengths) / len(post_lengths) if post_lengths else 0,
        'avg_comment_length': sum(comment_lengths) / len(comment_lengths) if comment_lengths else 0,
        'total_posts': len(post_lengths),
        'total_comments': len(comment_lengths),
        'engagement_ratio': len(comment_lengths) / (len(post_lengths) + len(comment_lengths)) if (len(post_lengths) + len(comment_lengths)) > 0 else 0
    }
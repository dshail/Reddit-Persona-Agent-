import re
from typing import Dict, List, Tuple
from collections import Counter
import numpy as np

# For full LDA implementation, you'd use sklearn
# pip install scikit-learn
try:
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def analyze_topics(user_data: Dict, n_topics: int = 5) -> Dict:
    """
    Extract main topics that the user discusses using LDA topic modeling.
    """
    results = {
        'topics': [],
        'topic_distribution': {},
        'dominant_topics': [],
        'topic_keywords': {},
        'content_categorization': {},
        'topic_insights': []
    }
    
    # Combine all text content
    documents = []
    for section, items in user_data.items():
        for item in items:
            if len(item['text'].strip()) > 50:  # Filter out very short texts
                documents.append(item['text'])
    
    if len(documents) < 3:
        results['topic_insights'] = ["Not enough content for meaningful topic analysis"]
        return results
    
    if SKLEARN_AVAILABLE:
        results = perform_lda_analysis(documents, n_topics)
    else:
        # Fallback: keyword-based topic detection
        results = perform_keyword_based_analysis(documents)
    
    results['topic_insights'] = generate_topic_insights(results)
    return results

def perform_lda_analysis(documents: List[str], n_topics: int) -> Dict:
    """
    Perform LDA topic modeling using scikit-learn.
    """
    results = {
        'topics': [],
        'topic_distribution': {},
        'dominant_topics': [],
        'topic_keywords': {},
        'content_categorization': {}
    }
    
    try:
        # Preprocess documents
        processed_docs = [preprocess_text(doc) for doc in documents]
        processed_docs = [doc for doc in processed_docs if len(doc.split()) > 5]
        
        if len(processed_docs) < 3:
            return results
        
        # Create document-term matrix
        vectorizer = CountVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        
        doc_term_matrix = vectorizer.fit_transform(processed_docs)
        
        # Perform LDA
        lda = LatentDirichletAllocation(
            n_components=min(n_topics, len(processed_docs)),
            random_state=42,
            max_iter=10
        )
        
        lda.fit(doc_term_matrix)
        
        # Extract topics and keywords
        feature_names = vectorizer.get_feature_names_out()
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topic_weights = [topic[i] for i in top_words_idx]
            
            results['topics'].append({
                'topic_id': topic_idx,
                'keywords': top_words,
                'weights': topic_weights
            })
            
            results['topic_keywords'][f'Topic {topic_idx + 1}'] = top_words[:5]
        
        # Get document-topic distribution
        doc_topic_dist = lda.transform(doc_term_matrix)
        
        # Find dominant topics
        topic_sums = doc_topic_dist.sum(axis=0)
        dominant_topic_idx = topic_sums.argmax()
        results['dominant_topics'] = [dominant_topic_idx]
        
        # Topic distribution
        for i, topic_sum in enumerate(topic_sums):
            results['topic_distribution'][f'Topic {i + 1}'] = float(topic_sum / topic_sums.sum())
        
        # Categorize content by dominant topic
        for doc_idx, doc in enumerate(processed_docs):
            dominant_topic = doc_topic_dist[doc_idx].argmax()
            if f'Topic {dominant_topic + 1}' not in results['content_categorization']:
                results['content_categorization'][f'Topic {dominant_topic + 1}'] = []
            results['content_categorization'][f'Topic {dominant_topic + 1}'].append(doc[:100] + "...")
        
    except Exception as e:
        print(f"LDA analysis failed: {e}")
        return perform_keyword_based_analysis(documents)
    
    return results

def perform_keyword_based_analysis(documents: List[str]) -> Dict:
    """
    Fallback topic analysis using keyword clustering.
    """
    results = {
        'topics': [],
        'topic_distribution': {},
        'dominant_topics': [],
        'topic_keywords': {},
        'content_categorization': {}
    }
    
    # Predefined topic categories with keywords
    topic_categories = {
        'Technology': ['tech', 'software', 'computer', 'programming', 'code', 'app', 'digital', 'ai', 'machine learning', 'data'],
        'Gaming': ['game', 'gaming', 'play', 'player', 'console', 'pc', 'xbox', 'playstation', 'nintendo', 'steam'],
        'Sports': ['sport', 'team', 'player', 'game', 'match', 'season', 'league', 'football', 'basketball', 'soccer'],
        'Entertainment': ['movie', 'film', 'show', 'tv', 'series', 'actor', 'music', 'song', 'album', 'concert'],
        'Politics': ['political', 'government', 'election', 'vote', 'policy', 'president', 'congress', 'law', 'rights'],
        'Finance': ['money', 'investment', 'stock', 'market', 'crypto', 'bitcoin', 'trading', 'economy', 'financial'],
        'Health': ['health', 'medical', 'doctor', 'hospital', 'medicine', 'fitness', 'exercise', 'diet', 'wellness'],
        'Education': ['school', 'university', 'student', 'teacher', 'education', 'learning', 'study', 'course', 'degree'],
        'Relationships': ['relationship', 'dating', 'marriage', 'family', 'friend', 'love', 'partner', 'couple'],
        'Lifestyle': ['life', 'lifestyle', 'hobby', 'travel', 'food', 'cooking', 'home', 'fashion', 'style']
    }
    
    # Count topic relevance for each document
    topic_scores = {topic: 0 for topic in topic_categories}
    topic_content = {topic: [] for topic in topic_categories}
    
    for doc in documents:
        doc_lower = doc.lower()
        doc_topic_scores = {}
        
        for topic, keywords in topic_categories.items():
            score = sum(1 for keyword in keywords if keyword in doc_lower)
            doc_topic_scores[topic] = score
            topic_scores[topic] += score
        
        # Assign document to dominant topic
        if any(doc_topic_scores.values()):
            dominant_topic = max(doc_topic_scores, key=doc_topic_scores.get)
            topic_content[dominant_topic].append(doc[:100] + "...")
    
    # Filter out topics with no content
    active_topics = {topic: score for topic, score in topic_scores.items() if score > 0}
    
    if active_topics:
        total_score = sum(active_topics.values())
        
        # Create results
        for i, (topic, score) in enumerate(sorted(active_topics.items(), key=lambda x: x[1], reverse=True)):
            results['topics'].append({
                'topic_id': i,
                'keywords': topic_categories[topic][:5],
                'weights': [score / total_score] * 5
            })
            
            results['topic_keywords'][topic] = topic_categories[topic][:5]
            results['topic_distribution'][topic] = score / total_score
            results['content_categorization'][topic] = topic_content[topic][:3]
        
        # Find dominant topic
        dominant_topic = max(active_topics, key=active_topics.get)
        results['dominant_topics'] = [dominant_topic]
    
    return results

def preprocess_text(text: str) -> str:
    """
    Preprocess text for topic modeling.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_key_phrases(documents: List[str], n_phrases: int = 20) -> List[Tuple[str, int]]:
    """
    Extract key phrases from documents using n-gram analysis.
    """
    # Simple n-gram extraction
    all_text = ' '.join(documents).lower()
    
    # Extract 2-grams and 3-grams
    words = re.findall(r'\b\w+\b', all_text)
    
    bigrams = []
    trigrams = []
    
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if len(bigram) > 6:  # Filter short phrases
            bigrams.append(bigram)
    
    for i in range(len(words) - 2):
        trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
        if len(trigram) > 10:  # Filter short phrases
            trigrams.append(trigram)
    
    # Count frequencies
    phrase_counts = Counter(bigrams + trigrams)
    
    # Filter out common stop phrases
    stop_phrases = {'i think', 'you know', 'i mean', 'i guess', 'i feel', 'i want', 'i need'}
    filtered_phrases = {phrase: count for phrase, count in phrase_counts.items() 
                       if phrase not in stop_phrases and count > 1}
    
    return list(Counter(filtered_phrases).most_common(n_phrases))

def generate_topic_insights(results: Dict) -> List[str]:
    """
    Generate human-readable insights from topic analysis.
    """
    insights = []
    
    if not results.get('topics'):
        insights.append("Unable to identify distinct topics from the content")
        return insights
    
    # Dominant topic insights
    if results.get('dominant_topics'):
        dominant = results['dominant_topics'][0]
        if isinstance(dominant, int) and results.get('topics'):
            if dominant < len(results['topics']):
                topic_keywords = results['topics'][dominant].get('keywords', [])
                insights.append(f"Primary discussion topics include: {', '.join(topic_keywords[:3])}")
        elif isinstance(dominant, str):
            insights.append(f"Most frequently discusses: {dominant}")
    
    # Topic diversity
    if results.get('topic_distribution'):
        num_active_topics = len([v for v in results['topic_distribution'].values() if v > 0.1])
        if num_active_topics > 3:
            insights.append("Shows diverse interests across multiple topics")
        elif num_active_topics <= 2:
            insights.append("Tends to focus on specific topic areas")
    
    # Content categorization insights
    if results.get('content_categorization'):
        categories_with_content = [cat for cat, content in results['content_categorization'].items() if content]
        if len(categories_with_content) > 1:
            insights.append(f"Active in {len(categories_with_content)} different topic areas")
    
    return insights
import re
from typing import Dict, List, Tuple
from collections import Counter, defaultdict

def analyze_social_interactions(user_data: Dict) -> Dict:
    """
    Analyze social interaction patterns and network connections.
    """
    results = {
        'interaction_patterns': {},
        'mentioned_users': {},
        'reply_behavior': {},
        'community_engagement': {},
        'social_metrics': {},
        'network_insights': []
    }
    
    # Extract all content for analysis
    all_content = []
    for section, items in user_data.items():
        for item in items:
            all_content.append({
                'text': item['text'],
                'permalink': item['permalink'],
                'type': section
            })
    
    # Analyze user mentions and interactions
    results['mentioned_users'] = extract_user_mentions(all_content)
    
    # Analyze reply behavior
    results['reply_behavior'] = analyze_reply_patterns(all_content)
    
    # Analyze community engagement
    results['community_engagement'] = analyze_community_engagement(all_content)
    
    # Calculate social metrics
    results['social_metrics'] = calculate_social_metrics(results)
    
    # Analyze interaction patterns
    results['interaction_patterns'] = analyze_interaction_patterns(all_content)
    
    # Generate insights
    results['network_insights'] = generate_network_insights(results)
    
    return results

def extract_user_mentions(content: List[Dict]) -> Dict:
    """
    Extract and analyze user mentions from content.
    """
    mentions = {
        'direct_mentions': [],
        'reply_targets': [],
        'frequent_interactions': {},
        'mention_frequency': 0
    }
    
    # Pattern to match Reddit usernames
    username_pattern = r'/?u/([A-Za-z0-9_-]+)'
    
    all_mentioned_users = []
    
    for item in content:
        text = item['text']
        
        # Find username mentions
        found_mentions = re.findall(username_pattern, text)
        all_mentioned_users.extend(found_mentions)
        
        # Check if this is a reply (starts with addressing someone)
        if text.strip().startswith('@') or any(text.lower().startswith(phrase) for phrase in ['hey ', 'hi ', 'hello ']):
            mentions['reply_targets'].append(text[:50] + "...")
    
    # Count mention frequency
    if all_mentioned_users:
        user_counts = Counter(all_mentioned_users)
        mentions['frequent_interactions'] = dict(user_counts.most_common(10))
        mentions['mention_frequency'] = len(all_mentioned_users) / len(content)
        mentions['direct_mentions'] = list(set(all_mentioned_users))
    
    return mentions

def analyze_reply_patterns(content: List[Dict]) -> Dict:
    """
    Analyze how the user responds to others and engages in conversations.
    """
    patterns = {
        'reply_indicators': 0,
        'conversation_starters': 0,
        'supportive_responses': 0,
        'disagreement_responses': 0,
        'question_responses': 0,
        'engagement_style': 'neutral'
    }
    
    # Reply indicators
    reply_phrases = ['thanks for', 'thank you for', 'i agree', 'you\'re right', 'good point', 
                    'i disagree', 'actually', 'however', 'but', 'on the other hand']
    
    # Supportive phrases
    supportive_phrases = ['great job', 'well done', 'awesome', 'amazing', 'love this', 
                         'this is great', 'fantastic', 'brilliant', 'perfect', 'exactly']
    
    # Disagreement phrases
    disagreement_phrases = ['i disagree', 'wrong', 'not true', 'actually no', 'that\'s incorrect',
                           'i don\'t think', 'not really', 'i doubt', 'unlikely', 'probably not']
    
    # Question starters
    question_starters = ['what do you', 'how do you', 'why do you', 'when did you', 
                        'where did you', 'who do you', 'have you ever', 'do you think']
    
    total_items = len(content)
    
    for item in content:
        text = item['text'].lower()
        
        # Count reply indicators
        patterns['reply_indicators'] += sum(1 for phrase in reply_phrases if phrase in text)
        
        # Count supportive responses
        patterns['supportive_responses'] += sum(1 for phrase in supportive_phrases if phrase in text)
        
        # Count disagreement responses
        patterns['disagreement_responses'] += sum(1 for phrase in disagreement_phrases if phrase in text)
        
        # Count questions (conversation starters)
        if any(starter in text for starter in question_starters) or text.count('?') > 0:
            patterns['question_responses'] += 1
        
        # Check if starting conversations
        if len(text) > 100 and not any(phrase in text for phrase in reply_phrases):
            patterns['conversation_starters'] += 1
    
    # Normalize by total content
    for key in ['reply_indicators', 'supportive_responses', 'disagreement_responses', 'question_responses']:
        patterns[key] = patterns[key] / total_items if total_items > 0 else 0
    
    # Determine engagement style
    if patterns['supportive_responses'] > patterns['disagreement_responses'] * 2:
        patterns['engagement_style'] = 'supportive'
    elif patterns['disagreement_responses'] > patterns['supportive_responses'] * 2:
        patterns['engagement_style'] = 'challenging'
    elif patterns['question_responses'] > 0.3:
        patterns['engagement_style'] = 'inquisitive'
    else:
        patterns['engagement_style'] = 'neutral'
    
    return patterns

def analyze_community_engagement(content: List[Dict]) -> Dict:
    """
    Analyze engagement with different communities and subreddits.
    """
    engagement = {
        'subreddit_activity': {},
        'community_diversity': 0,
        'engagement_depth': {},
        'cross_community_behavior': {}
    }
    
    # Extract subreddit information from permalinks
    subreddit_pattern = r'/r/([A-Za-z0-9_]+)/'
    subreddit_activity = defaultdict(int)
    subreddit_content_length = defaultdict(list)
    
    for item in content:
        permalink = item['permalink']
        text_length = len(item['text'])
        
        # Extract subreddit from permalink
        subreddit_match = re.search(subreddit_pattern, permalink)
        if subreddit_match:
            subreddit = subreddit_match.group(1)
            subreddit_activity[subreddit] += 1
            subreddit_content_length[subreddit].append(text_length)
    
    # Calculate metrics
    engagement['subreddit_activity'] = dict(Counter(subreddit_activity).most_common(10))
    engagement['community_diversity'] = len(subreddit_activity)
    
    # Calculate engagement depth (average content length per subreddit)
    for subreddit, lengths in subreddit_content_length.items():
        if lengths:
            engagement['engagement_depth'][subreddit] = sum(lengths) / len(lengths)
    
    # Analyze cross-community behavior
    if len(subreddit_activity) > 1:
        total_posts = sum(subreddit_activity.values())
        most_active_subreddit_posts = max(subreddit_activity.values())
        concentration_ratio = most_active_subreddit_posts / total_posts
        
        if concentration_ratio > 0.7:
            engagement['cross_community_behavior']['type'] = 'focused'
            engagement['cross_community_behavior']['description'] = 'Primarily active in one community'
        elif concentration_ratio < 0.3:
            engagement['cross_community_behavior']['type'] = 'diverse'
            engagement['cross_community_behavior']['description'] = 'Actively participates across multiple communities'
        else:
            engagement['cross_community_behavior']['type'] = 'balanced'
            engagement['cross_community_behavior']['description'] = 'Balanced participation across communities'
    
    return engagement

def analyze_interaction_patterns(content: List[Dict]) -> Dict:
    """
    Analyze overall interaction patterns and social behavior.
    """
    patterns = {
        'interaction_frequency': 0,
        'response_length_avg': 0,
        'social_cues_usage': {},
        'collaboration_indicators': 0,
        'help_seeking_behavior': 0,
        'help_offering_behavior': 0
    }
    
    # Social cues
    social_cues = {
        'greetings': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
        'gratitude': ['thank you', 'thanks', 'appreciate', 'grateful'],
        'apologies': ['sorry', 'apologize', 'my bad', 'excuse me'],
        'politeness': ['please', 'would you', 'could you', 'if you don\'t mind']
    }
    
    # Help-related phrases
    help_seeking = ['can someone help', 'need help', 'please help', 'how do i', 'what should i do']
    help_offering = ['i can help', 'let me help', 'here\'s how', 'try this', 'i recommend']
    
    collaboration_phrases = ['let\'s work together', 'we should', 'together we can', 'team up', 'collaborate']
    
    total_interactions = 0
    total_length = 0
    
    for item in content:
        text = item['text'].lower()
        text_length = len(item['text'])
        total_length += text_length
        
        # Check for interaction indicators (replies, mentions, questions)
        if any(indicator in text for indicator in ['@', 'u/', '?', 'reply', 'response']):
            total_interactions += 1
        
        # Count social cues
        for cue_type, phrases in social_cues.items():
            if cue_type not in patterns['social_cues_usage']:
                patterns['social_cues_usage'][cue_type] = 0
            patterns['social_cues_usage'][cue_type] += sum(1 for phrase in phrases if phrase in text)
        
        # Count help-related behavior
        patterns['help_seeking_behavior'] += sum(1 for phrase in help_seeking if phrase in text)
        patterns['help_offering_behavior'] += sum(1 for phrase in help_offering if phrase in text)
        
        # Count collaboration indicators
        patterns['collaboration_indicators'] += sum(1 for phrase in collaboration_phrases if phrase in text)
    
    # Calculate averages
    total_content = len(content)
    patterns['interaction_frequency'] = total_interactions / total_content if total_content > 0 else 0
    patterns['response_length_avg'] = total_length / total_content if total_content > 0 else 0
    
    # Normalize social cues by total content
    for cue_type in patterns['social_cues_usage']:
        patterns['social_cues_usage'][cue_type] = patterns['social_cues_usage'][cue_type] / total_content
    
    return patterns

def calculate_social_metrics(results: Dict) -> Dict:
    """
    Calculate overall social engagement metrics.
    """
    metrics = {
        'social_engagement_score': 0,
        'community_integration_score': 0,
        'interaction_diversity_score': 0,
        'helpfulness_score': 0
    }
    
    # Social engagement score (based on mentions, replies, social cues)
    mention_freq = results.get('mentioned_users', {}).get('mention_frequency', 0)
    interaction_freq = results.get('interaction_patterns', {}).get('interaction_frequency', 0)
    social_cues_total = sum(results.get('interaction_patterns', {}).get('social_cues_usage', {}).values())
    
    metrics['social_engagement_score'] = min(100, (mention_freq + interaction_freq + social_cues_total) * 50)
    
    # Community integration score
    community_diversity = results.get('community_engagement', {}).get('community_diversity', 0)
    cross_community_type = results.get('community_engagement', {}).get('cross_community_behavior', {}).get('type', 'focused')
    
    diversity_bonus = min(20, community_diversity * 2)
    if cross_community_type == 'diverse':
        diversity_bonus += 30
    elif cross_community_type == 'balanced':
        diversity_bonus += 20
    
    metrics['community_integration_score'] = min(100, diversity_bonus + 30)
    
    # Interaction diversity score
    reply_patterns = results.get('reply_behavior', {})
    supportive = reply_patterns.get('supportive_responses', 0)
    questions = reply_patterns.get('question_responses', 0)
    disagreements = reply_patterns.get('disagreement_responses', 0)
    
    diversity_score = (supportive + questions + disagreements) * 100
    metrics['interaction_diversity_score'] = min(100, diversity_score)
    
    # Helpfulness score
    help_offering = results.get('interaction_patterns', {}).get('help_offering_behavior', 0)
    collaboration = results.get('interaction_patterns', {}).get('collaboration_indicators', 0)
    
    metrics['helpfulness_score'] = min(100, (help_offering + collaboration) * 50)
    
    return metrics

def generate_network_insights(results: Dict) -> List[str]:
    """
    Generate human-readable insights from social network analysis.
    """
    insights = []
    
    # Mention patterns
    mentioned_users = results.get('mentioned_users', {})
    if mentioned_users.get('frequent_interactions'):
        top_interaction = list(mentioned_users['frequent_interactions'].keys())[0]
        insights.append(f"Frequently interacts with u/{top_interaction}")
    
    if mentioned_users.get('mention_frequency', 0) > 0.1:
        insights.append("Actively mentions and engages with other users")
    elif mentioned_users.get('mention_frequency', 0) < 0.05:
        insights.append("Tends to post independently with limited direct user interactions")
    
    # Community engagement
    community_engagement = results.get('community_engagement', {})
    community_diversity = community_engagement.get('community_diversity', 0)
    
    if community_diversity > 10:
        insights.append(f"Actively participates in {community_diversity}+ different communities")
    elif community_diversity > 5:
        insights.append("Engages with multiple communities regularly")
    elif community_diversity <= 2:
        insights.append("Focuses primarily on specific communities")
    
    # Engagement style
    reply_behavior = results.get('reply_behavior', {})
    engagement_style = reply_behavior.get('engagement_style', 'neutral')
    
    if engagement_style == 'supportive':
        insights.append("Shows supportive and encouraging interaction style")
    elif engagement_style == 'challenging':
        insights.append("Tends to engage in debates and express disagreements")
    elif engagement_style == 'inquisitive':
        insights.append("Frequently asks questions and seeks information")
    
    # Social metrics
    social_metrics = results.get('social_metrics', {})
    engagement_score = social_metrics.get('social_engagement_score', 0)
    
    if engagement_score > 70:
        insights.append("Demonstrates high social engagement and interaction")
    elif engagement_score < 30:
        insights.append("Shows limited social interaction patterns")
    
    # Helpfulness
    helpfulness_score = social_metrics.get('helpfulness_score', 0)
    if helpfulness_score > 50:
        insights.append("Often offers help and assistance to others")
    
    # Community behavior
    cross_community = community_engagement.get('cross_community_behavior', {})
    if cross_community.get('type') == 'diverse':
        insights.append("Maintains diverse interests across multiple communities")
    elif cross_community.get('type') == 'focused':
        insights.append("Shows strong loyalty to specific communities")
    
    return insights
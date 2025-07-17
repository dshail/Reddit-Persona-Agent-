import re
from typing import Dict, List
from datetime import datetime, timezone
from collections import defaultdict, Counter
import pandas as pd

def analyze_activity_timeline(user_data: Dict) -> Dict:
    """
    Analyze posting patterns by time of day, day of week, and activity trends.
    """
    results = {
        'hourly_activity': {},
        'daily_activity': {},
        'activity_patterns': {},
        'peak_hours': [],
        'activity_insights': []
    }
    
    # Extract timestamps from permalinks (Reddit format analysis)
    timestamps = extract_timestamps_from_content(user_data)
    
    if not timestamps:
        # Fallback: analyze based on content patterns
        results = analyze_content_based_activity(user_data)
        return results
    
    # Analyze hourly patterns
    hourly_counts = defaultdict(int)
    daily_counts = defaultdict(int)
    
    for timestamp in timestamps:
        hour = timestamp.hour
        day = timestamp.strftime('%A')
        hourly_counts[hour] += 1
        daily_counts[day] += 1
    
    results['hourly_activity'] = dict(hourly_counts)
    results['daily_activity'] = dict(daily_counts)
    
    # Identify peak activity hours
    sorted_hours = sorted(hourly_counts.items(), key=lambda x: x[1], reverse=True)
    results['peak_hours'] = [hour for hour, count in sorted_hours[:3]]
    
    # Activity pattern analysis
    results['activity_patterns'] = analyze_activity_patterns(hourly_counts, daily_counts)
    
    # Generate insights
    results['activity_insights'] = generate_activity_insights(results)
    
    return results

def extract_timestamps_from_content(user_data: Dict) -> List[datetime]:
    """
    Extract timestamps from Reddit content (limited by API access).
    This is a simplified version - in practice, you'd need Reddit API timestamps.
    """
    timestamps = []
    
    # For now, we'll simulate based on content analysis
    # In a real implementation, you'd extract from Reddit API response
    
    return timestamps

def analyze_content_based_activity(user_data: Dict) -> Dict:
    """
    Analyze activity patterns based on content characteristics.
    """
    results = {
        'posting_frequency': 'moderate',
        'content_length_patterns': {},
        'engagement_style': 'balanced',
        'activity_insights': []
    }
    
    all_content = []
    for section, items in user_data.items():
        all_content.extend(items)
    
    # Analyze content length patterns
    lengths = [len(item['text']) for item in all_content]
    if lengths:
        avg_length = sum(lengths) / len(lengths)
        results['content_length_patterns'] = {
            'average_length': avg_length,
            'short_posts': sum(1 for l in lengths if l < 100),
            'medium_posts': sum(1 for l in lengths if 100 <= l < 500),
            'long_posts': sum(1 for l in lengths if l >= 500)
        }
    
    # Analyze posting frequency
    total_posts = len(all_content)
    if total_posts > 100:
        results['posting_frequency'] = 'high'
    elif total_posts > 20:
        results['posting_frequency'] = 'moderate'
    else:
        results['posting_frequency'] = 'low'
    
    # Generate insights
    results['activity_insights'] = [
        f"User has {results['posting_frequency']} posting frequency",
        f"Average content length: {results['content_length_patterns'].get('average_length', 0):.0f} characters",
        f"Prefers {'short' if results['content_length_patterns'].get('short_posts', 0) > total_posts/2 else 'detailed'} posts"
    ]
    
    return results

def analyze_activity_patterns(hourly_counts: Dict, daily_counts: Dict) -> Dict:
    """
    Analyze activity patterns to determine user behavior.
    """
    patterns = {}
    
    # Determine if user is more active during day or night
    day_hours = sum(hourly_counts.get(h, 0) for h in range(6, 18))
    night_hours = sum(hourly_counts.get(h, 0) for h in list(range(0, 6)) + list(range(18, 24)))
    
    if day_hours > night_hours:
        patterns['time_preference'] = 'day_active'
    else:
        patterns['time_preference'] = 'night_active'
    
    # Weekend vs weekday activity
    weekend_activity = daily_counts.get('Saturday', 0) + daily_counts.get('Sunday', 0)
    weekday_activity = sum(daily_counts.get(day, 0) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    
    if weekend_activity > weekday_activity / 2.5:  # Accounting for 5 weekdays vs 2 weekend days
        patterns['schedule_type'] = 'weekend_heavy'
    else:
        patterns['schedule_type'] = 'weekday_heavy'
    
    return patterns

def generate_activity_insights(results: Dict) -> List[str]:
    """
    Generate human-readable insights from activity analysis.
    """
    insights = []
    
    if results['peak_hours']:
        peak_hour = results['peak_hours'][0]
        if 6 <= peak_hour <= 12:
            insights.append("Most active during morning hours")
        elif 12 <= peak_hour <= 18:
            insights.append("Most active during afternoon hours")
        elif 18 <= peak_hour <= 22:
            insights.append("Most active during evening hours")
        else:
            insights.append("Most active during late night/early morning hours")
    
    if results['activity_patterns'].get('time_preference') == 'night_active':
        insights.append("Tends to be more active during nighttime")
    else:
        insights.append("Tends to be more active during daytime")
    
    if results['activity_patterns'].get('schedule_type') == 'weekend_heavy':
        insights.append("Shows increased activity on weekends")
    else:
        insights.append("Maintains consistent weekday activity")
    
    return insights
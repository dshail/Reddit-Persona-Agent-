#!/usr/bin/env python3

from activity_analyzer import analyze_activity_timeline
from writing_style_analyzer import analyze_writing_style
from topic_analyzer import analyze_topics
from social_network_analyzer import analyze_social_interactions
from personality_analyzer import analyze_big_five_personality

# Test with sample data
sample_data = {
    'posts': [
        {'text': 'I love programming and creating new software applications. It is amazing how technology can solve real-world problems!', 'permalink': '/r/programming/comments/test1/'},
        {'text': 'Just finished reading a fascinating book about artificial intelligence. The future is exciting!', 'permalink': '/r/books/comments/test2/'}
    ],
    'comments': [
        {'text': 'Great point! I totally agree with your analysis. Thanks for sharing this insight.', 'permalink': '/r/technology/comments/test3/'},
        {'text': 'Actually, I think there might be another perspective to consider here. What do you think about this?', 'permalink': '/r/discussion/comments/test4/'}
    ]
}

print('🧪 Testing Advanced Features...\n')

print('1. Testing Activity Analysis...')
try:
    activity_result = analyze_activity_timeline(sample_data)
    print(f'   ✅ Activity insights: {len(activity_result.get("activity_insights", []))} insights generated')
    print(f'   📊 Posting frequency: {activity_result.get("posting_frequency", "unknown")}')
except Exception as e:
    print(f'   ❌ Error: {e}')

print('\n2. Testing Writing Style Analysis...')
try:
    writing_result = analyze_writing_style(sample_data)
    print(f'   ✅ Writing insights: {len(writing_result.get("writing_insights", []))} insights generated')
    if writing_result.get('formality_analysis'):
        print(f'   📝 Formality level: {writing_result["formality_analysis"]["formality_level"]}')
except Exception as e:
    print(f'   ❌ Error: {e}')

print('\n3. Testing Topic Analysis...')
try:
    topic_result = analyze_topics(sample_data)
    print(f'   ✅ Topic insights: {len(topic_result.get("topic_insights", []))} insights generated')
    if topic_result.get('topic_keywords'):
        print(f'   🏷️ Topics found: {len(topic_result["topic_keywords"])}')
except Exception as e:
    print(f'   ❌ Error: {e}')

print('\n4. Testing Social Network Analysis...')
try:
    social_result = analyze_social_interactions(sample_data)
    print(f'   ✅ Social insights: {len(social_result.get("network_insights", []))} insights generated')
    if social_result.get('social_metrics'):
        engagement = social_result['social_metrics'].get('social_engagement_score', 0)
        print(f'   👥 Social engagement score: {engagement:.1f}/100')
except Exception as e:
    print(f'   ❌ Error: {e}')

print('\n5. Testing Personality Analysis...')
try:
    personality_result = analyze_big_five_personality(sample_data)
    print(f'   ✅ Personality insights: {len(personality_result.get("personality_insights", []))} insights generated')
    if personality_result.get('dominant_traits'):
        print(f'   🎭 Dominant traits: {", ".join(personality_result["dominant_traits"])}')
except Exception as e:
    print(f'   ❌ Error: {e}')

print('\n🎉 Feature testing completed!')
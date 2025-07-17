
import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reddit_scraper import scrape_reddit_user
from persona_chain import generate_user_persona
from utils import save_persona_to_file, generate_persona_pdf
from persona_comparison import compare_personas
from sentiment_analyzer import analyze_sentiment_and_behavior
from activity_analyzer import analyze_activity_timeline
from writing_style_analyzer import analyze_writing_style
from topic_analyzer import analyze_topics
from social_network_analyzer import analyze_social_interactions
from personality_analyzer import analyze_big_five_personality

st.set_page_config(page_title="Reddit Persona Agent", page_icon="🧠", layout="wide")

# Sidebar for navigation
st.sidebar.title("🧠 Reddit Persona Agent")
mode = st.sidebar.selectbox(
    "Choose Mode:",
    ["Single User Analysis", "Compare Two Users", "Advanced Analytics"]
)

if mode == "Single User Analysis":
    st.title("🧠 Reddit User Persona Generator")
    
    url = st.text_input("Enter Reddit profile URL", "https://www.reddit.com/user/spez/")
    
    if st.button("Generate Persona"):
        if url:
            with st.spinner("🔍 Scraping Reddit user data..."):
                user_data = scrape_reddit_user(url)
            
            if not user_data["posts"] and not user_data["comments"]:
                st.error("❌ No user data found. Please check the Reddit URL.")
            else:
                username = url.strip("/").split("/")[-1]
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📋 Persona", "📊 Analytics", "💾 Downloads"])
                
                with tab1:
                    with st.spinner("🧬 Generating user persona..."):
                        persona_output = generate_user_persona(user_data)
                    
                    st.success(f"✅ Persona created for user '{username}'")
                    st.text_area("Generated Persona", persona_output, height=500)
                
                with tab2:
                    with st.spinner("📊 Analyzing behavioral patterns..."):
                        analytics = analyze_sentiment_and_behavior(user_data)
                    
                    # Display analytics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Sentiment Analysis")
                        if analytics['sentiment_scores']:
                            sentiments = [item['sentiment'] for item in analytics['sentiment_scores']]
                            avg_sentiment = sum(sentiments) / len(sentiments)
                            st.metric("Average Sentiment", f"{avg_sentiment:.2f}")
                            
                            # Sentiment distribution
                            fig = px.histogram(x=sentiments, title="Sentiment Distribution")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("😊 Emotion Analysis")
                        if analytics['emotion_analysis']:
                            emotions_df = pd.DataFrame(list(analytics['emotion_analysis'].items()), 
                                                     columns=['Emotion', 'Percentage'])
                            fig = px.bar(emotions_df, x='Emotion', y='Percentage', 
                                       title="Emotional Patterns")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Behavioral patterns
                    st.subheader("🎭 Behavioral Patterns")
                    if analytics['behavioral_patterns']:
                        patterns_df = pd.DataFrame(list(analytics['behavioral_patterns'].items()), 
                                                 columns=['Pattern', 'Percentage'])
                        fig = px.pie(patterns_df, values='Percentage', names='Pattern', 
                                   title="Communication Patterns")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Subreddit analysis
                    st.subheader("📱 Subreddit Activity")
                    if analytics['subreddit_analysis']:
                        subreddit_df = pd.DataFrame(list(analytics['subreddit_analysis'].items()), 
                                                  columns=['Subreddit', 'Count'])
                        fig = px.bar(subreddit_df.head(10), x='Count', y='Subreddit', 
                                   orientation='h', title="Top Subreddits")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Word cloud
                    st.subheader("☁️ Word Cloud")
                    all_text = " ".join([item['text'] for section in user_data.values() 
                                       for item in section])
                    if all_text:
                        wordcloud = WordCloud(width=800, height=400, 
                                            background_color='white').generate(all_text)
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                
                with tab3:
                    st.subheader("💾 Download Options")
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Text file download
                        st.download_button(
                            label="📄 Download as TXT",
                            data=persona_output,
                            file_name=f"{username}_persona.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        # PDF file download
                        with st.spinner("📄 Generating PDF..."):
                            pdf_data = generate_persona_pdf(username, persona_output)
                        
                        st.download_button(
                            label="📑 Download as PDF",
                            data=pdf_data,
                            file_name=f"{username}_persona.pdf",
                            mime="application/pdf"
                        )
        else:
            st.warning("Please enter a Reddit profile URL")

elif mode == "Compare Two Users":
    st.title("⚖️ Compare Two Reddit Users")
    
    col1, col2 = st.columns(2)
    
    with col1:
        url1 = st.text_input("First Reddit User URL", "https://www.reddit.com/user/spez/")
    
    with col2:
        url2 = st.text_input("Second Reddit User URL", "https://www.reddit.com/user/JayBong2k/")
    
    if st.button("Compare Users"):
        if url1 and url2:
            with st.spinner("🔍 Analyzing both users..."):
                comparison_result = compare_personas(url1, url2)
            
            st.success("✅ Comparison completed!")
            st.text_area("Comparison Report", comparison_result, height=600)
            
            # Download comparison report
            username1 = url1.strip("/").split("/")[-1]
            username2 = url2.strip("/").split("/")[-1]
            
            st.download_button(
                label="📄 Download Comparison Report",
                data=comparison_result,
                file_name=f"{username1}_vs_{username2}_comparison.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please enter both Reddit profile URLs")

elif mode == "Advanced Analytics":
    st.title("📊 Advanced Reddit Analytics Dashboard")
    
    url = st.text_input("Enter Reddit profile URL for advanced analysis", 
                       "https://www.reddit.com/user/spez/")
    
    if st.button("Run Advanced Analysis"):
        if url:
            with st.spinner("🔍 Scraping and analyzing data..."):
                user_data = scrape_reddit_user(url)
            
            username = url.strip("/").split("/")[-1]
            st.success(f"✅ Advanced analysis completed for {username}")
            
            # Run all advanced analyses
            with st.spinner("🧠 Running comprehensive analysis..."):
                sentiment_analysis = analyze_sentiment_and_behavior(user_data)
                activity_analysis = analyze_activity_timeline(user_data)
                writing_analysis = analyze_writing_style(user_data)
                topic_analysis = analyze_topics(user_data)
                social_analysis = analyze_social_interactions(user_data)
                personality_analysis = analyze_big_five_personality(user_data)
            
            # Create comprehensive dashboard with tabs
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📊 Overview", "🎭 Personality", "📝 Writing Style", 
                "🏷️ Topics", "👥 Social Network", "⏰ Activity Patterns"
            ])
            
            with tab1:
                st.subheader("📊 Comprehensive Overview")
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Posts", sentiment_analysis['engagement_patterns']['total_posts'])
                with col2:
                    st.metric("Total Comments", sentiment_analysis['engagement_patterns']['total_comments'])
                with col3:
                    avg_sentiment = sum([item['sentiment'] for item in sentiment_analysis['sentiment_scores']]) / len(sentiment_analysis['sentiment_scores']) if sentiment_analysis['sentiment_scores'] else 0
                    st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
                with col4:
                    social_score = social_analysis['social_metrics'].get('social_engagement_score', 0)
                    st.metric("Social Engagement", f"{social_score:.0f}/100")
                
                # Sentiment timeline
                if sentiment_analysis['sentiment_scores']:
                    st.subheader("📈 Sentiment Timeline")
                    sentiment_data = pd.DataFrame(sentiment_analysis['sentiment_scores'])
                    fig = px.line(sentiment_data, y='sentiment', title="Sentiment Over Time")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Emotion heatmap
                if sentiment_analysis['emotion_analysis']:
                    st.subheader("🌡️ Emotion Heatmap")
                    emotions = list(sentiment_analysis['emotion_analysis'].keys())
                    values = list(sentiment_analysis['emotion_analysis'].values())
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=[values],
                        x=emotions,
                        y=['Intensity'],
                        colorscale='Viridis'
                    ))
                    fig.update_layout(title="Emotional Intensity Heatmap")
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.subheader("🎭 Big Five Personality Analysis")
                
                if personality_analysis['personality_scores']:
                    # Personality radar chart
                    traits = list(personality_analysis['personality_scores'].keys())
                    scores = [personality_analysis['personality_scores'][trait]['score'] for trait in traits]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=scores,
                        theta=[trait.title() for trait in traits],
                        fill='toself',
                        name='Personality Profile'
                    ))
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100]
                            )),
                        showlegend=True,
                        title="Big Five Personality Traits"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Personality insights
                    st.subheader("🔍 Personality Insights")
                    for insight in personality_analysis['personality_insights']:
                        st.write(f"• {insight}")
                    
                    # Detailed scores
                    col1, col2 = st.columns(2)
                    with col1:
                        for trait in traits[:3]:
                            data = personality_analysis['personality_scores'][trait]
                            st.metric(
                                trait.title(), 
                                f"{data['score']:.0f}/100", 
                                delta=data['level'].title()
                            )
                    
                    with col2:
                        for trait in traits[3:]:
                            data = personality_analysis['personality_scores'][trait]
                            st.metric(
                                trait.title(), 
                                f"{data['score']:.0f}/100", 
                                delta=data['level'].title()
                            )
            
            with tab3:
                st.subheader("📝 Writing Style Analysis")
                
                if writing_analysis['linguistic_metrics']:
                    # Writing metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Avg Sentence Length", f"{writing_analysis['linguistic_metrics']['avg_sentence_length']:.1f} words")
                        st.metric("Avg Word Length", f"{writing_analysis['linguistic_metrics']['avg_word_length']:.1f} chars")
                    
                    with col2:
                        st.metric("Readability Score", f"{writing_analysis['linguistic_metrics']['readability_score']:.0f}")
                        st.metric("Words per Post", f"{writing_analysis['linguistic_metrics']['words_per_post']:.0f}")
                    
                    with col3:
                        vocab_richness = writing_analysis['vocabulary_analysis']['vocabulary_richness']
                        st.metric("Vocabulary Richness", f"{vocab_richness:.2f}")
                        formality = writing_analysis['formality_analysis']['formality_level']
                        st.metric("Formality Level", formality.title())
                
                # Communication style
                if writing_analysis['communication_style']:
                    st.subheader("💬 Communication Style")
                    comm_style = writing_analysis['communication_style']
                    
                    style_df = pd.DataFrame([
                        {'Style': 'Assertiveness', 'Score': comm_style['assertiveness']},
                        {'Style': 'Politeness', 'Score': comm_style['politeness']},
                        {'Style': 'Enthusiasm', 'Score': comm_style['enthusiasm']},
                        {'Style': 'Analytical', 'Score': comm_style['analytical_tendency']},
                        {'Style': 'Storytelling', 'Score': comm_style['storytelling_tendency']}
                    ])
                    
                    fig = px.bar(style_df, x='Style', y='Score', title="Communication Style Profile")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Writing insights
                st.subheader("✍️ Writing Insights")
                for insight in writing_analysis['writing_insights']:
                    st.write(f"• {insight}")
            
            with tab4:
                st.subheader("🏷️ Topic Analysis")
                
                if topic_analysis['topic_keywords']:
                    # Topic distribution
                    if topic_analysis['topic_distribution']:
                        topics_df = pd.DataFrame(list(topic_analysis['topic_distribution'].items()), 
                                               columns=['Topic', 'Weight'])
                        fig = px.pie(topics_df, values='Weight', names='Topic', 
                                   title="Topic Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Topic keywords
                    st.subheader("🔑 Key Topics & Keywords")
                    for topic, keywords in topic_analysis['topic_keywords'].items():
                        st.write(f"**{topic}:** {', '.join(keywords)}")
                    
                    # Topic insights
                    st.subheader("💡 Topic Insights")
                    for insight in topic_analysis['topic_insights']:
                        st.write(f"• {insight}")
                else:
                    st.info("Not enough content for meaningful topic analysis")
            
            with tab5:
                st.subheader("👥 Social Network Analysis")
                
                # Social metrics
                social_metrics = social_analysis['social_metrics']
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Social Engagement", f"{social_metrics['social_engagement_score']:.0f}/100")
                with col2:
                    st.metric("Community Integration", f"{social_metrics['community_integration_score']:.0f}/100")
                with col3:
                    st.metric("Interaction Diversity", f"{social_metrics['interaction_diversity_score']:.0f}/100")
                with col4:
                    st.metric("Helpfulness", f"{social_metrics['helpfulness_score']:.0f}/100")
                
                # Community engagement
                if social_analysis['community_engagement']['subreddit_activity']:
                    st.subheader("📱 Community Activity")
                    subreddit_data = social_analysis['community_engagement']['subreddit_activity']
                    subreddit_df = pd.DataFrame(list(subreddit_data.items()), 
                                              columns=['Subreddit', 'Activity'])
                    fig = px.bar(subreddit_df.head(10), x='Activity', y='Subreddit', 
                               orientation='h', title="Top Active Subreddits")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Social insights
                st.subheader("🤝 Social Insights")
                for insight in social_analysis['network_insights']:
                    st.write(f"• {insight}")
            
            with tab6:
                st.subheader("⏰ Activity Patterns")
                
                # Activity insights
                st.subheader("📅 Activity Insights")
                for insight in activity_analysis['activity_insights']:
                    st.write(f"• {insight}")
                
                # Content patterns
                if activity_analysis.get('content_length_patterns'):
                    st.subheader("📊 Content Length Distribution")
                    patterns = activity_analysis['content_length_patterns']
                    
                    length_data = pd.DataFrame([
                        {'Type': 'Short Posts (<100 chars)', 'Count': patterns['short_posts']},
                        {'Type': 'Medium Posts (100-500 chars)', 'Count': patterns['medium_posts']},
                        {'Type': 'Long Posts (>500 chars)', 'Count': patterns['long_posts']}
                    ])
                    
                    fig = px.pie(length_data, values='Count', names='Type', 
                               title="Post Length Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Posting frequency
                posting_freq = activity_analysis.get('posting_frequency', 'unknown')
                st.metric("Posting Frequency", posting_freq.title())
        else:
            st.warning("Please enter a Reddit profile URL")

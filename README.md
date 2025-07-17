# 🧠 Reddit Persona Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-blue)](https://www.langchain.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-FF6B35.svg)](https://openrouter.ai/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](tests/)
[![Streamlit](https://img.shields.io/badge/Streamlit-GUI-red)](https://streamlit.io/)

> **Advanced AI-powered behavioral analysis platform** that generates comprehensive user personas from Reddit profiles using cutting-edge NLP, machine learning, and LLM technologies.

---

## 🚀 **Key Features**

### **Core Functionality**
- 🔍 **Reddit Data Scraping** - Automated extraction of posts & comments via PRAW API
- 🧠 **AI Persona Generation** - LangChain + OpenRouter LLM integration
- 🔗 **Source Citations** - Every insight backed by specific Reddit posts
- 💾 **Multi-format Export** - PDF, TXT, and comprehensive reports
- 🖥️ **Dual Interface** - CLI and advanced Streamlit web GUI

### **Advanced Analytics Suite**
- 🎭 **Big Five Personality Analysis** - Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- 📝 **Writing Style Profiling** - Linguistic patterns, vocabulary complexity, formality analysis
- 🏷️ **Topic Modeling** - LDA-based topic extraction and content categorization
- 👥 **Social Network Analysis** - Interaction patterns, community engagement, social metrics
- ⏰ **Activity Timeline Analysis** - Posting patterns, peak hours, behavioral trends
- 😊 **Sentiment & Emotion Analysis** - Emotional profiling and sentiment tracking

### **Interactive Visualizations**
- 📊 **Personality Radar Charts** - Big Five trait visualization
- 🌡️ **Emotion Heatmaps** - Emotional intensity mapping
- ☁️ **Word Clouds** - Visual content representation
- 📈 **Sentiment Timelines** - Emotional trends over time
- 🥧 **Topic Distribution** - Content categorization charts

---

## ⚙️ **Installation & Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/your-username/reddit-persona-agent.git
cd reddit-persona-agent
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Environment Configuration**
```bash
cp .env.example .env
```

Update `.env` with your API credentials:
```ini
OPENROUTER_API_KEY=your_openrouter_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=reddit-persona-agent/1.0
```

---

## 🚀 **Usage**

### **CLI Mode**

**Basic Analysis:**
```bash
python app.py
# or
python app.py --url https://www.reddit.com/user/username/
```

**Advanced Comprehensive Analysis:**
```bash
python app.py --advanced --url https://www.reddit.com/user/username/
```

### **Web GUI Mode**
```bash
streamlit run gui/streamlit_app.py
```

**Available Modes:**
- 🧠 **Single User Analysis** - Complete persona generation with analytics
- ⚖️ **Compare Two Users** - Side-by-side behavioral comparison
- 📊 **Advanced Analytics** - Comprehensive 6-tab analysis dashboard

---

## 📁 **Project Structure**

```
reddit-persona-agent/
│
├── 🎯 Core Components
│   ├── app.py                      # Enhanced CLI with advanced features
│   ├── persona_chain.py            # LangChain LLM integration
│   ├── reddit_scraper.py           # Reddit API data extraction
│   └── utils.py                    # Utilities & PDF generation
│
├── 🧠 Advanced Analytics Modules
│   ├── personality_analyzer.py     # Big Five personality analysis
│   ├── writing_style_analyzer.py   # Linguistic pattern analysis
│   ├── topic_analyzer.py           # LDA topic modeling
│   ├── social_network_analyzer.py  # Social interaction analysis
│   ├── activity_analyzer.py        # Activity timeline analysis
│   └── sentiment_analyzer.py       # Emotion & sentiment analysis
│
├── 🖥️ User Interfaces
│   └── gui/streamlit_app.py        # Advanced web dashboard
│
├── 🧪 Testing & Utilities
│   ├── tests/                      # Unit tests
│   ├── test_features.py           # Feature validation
│   └── persona_comparison.py      # User comparison tools
│
├── 📊 Data & Configuration
│   ├── prompts/persona_prompt.txt  # LLM prompt templates
│   ├── output/                     # Generated reports
│   ├── .env.example               # Environment template
│   └── requirements.txt           # Python dependencies
│
└── 📚 Documentation
    └── README.md                  # This file
```

---

## 📊 **Sample Output**

### **Basic Persona**
```yaml
👤 Name: Alex Chen (fictitious)
📅 Age: 28-32 years old
💼 Occupation: Software Developer
🎮 Interests: Gaming, AI/ML, Cryptocurrency, Open Source
🗣️ Personality: Analytical, Curious, Community-oriented
📍 Location: Urban tech hub (inferred)

📌 Key Insights:
• Shows high technical expertise in programming discussions
• Actively participates in 15+ different communities
• Demonstrates supportive communication style
• Most active during evening hours (7-11 PM)
```

### **Advanced Analytics**
```yaml
🎭 Personality Profile (Big Five):
• Openness: 85/100 (High) - Creative and intellectually curious
• Conscientiousness: 72/100 (High) - Organized and goal-oriented
• Extraversion: 45/100 (Medium) - Balanced social engagement
• Agreeableness: 78/100 (High) - Cooperative and empathetic
• Neuroticism: 23/100 (Low) - Emotionally stable

📝 Writing Style: Formal-technical, rich vocabulary, analytical
🏷️ Main Topics: Technology (35%), Gaming (25%), Finance (20%)
👥 Social Behavior: High community integration, helpful contributor
⏰ Activity: Peak hours 7-11 PM, weekend-heavy posting
😊 Emotional Profile: Predominantly positive (78% positive sentiment)
```

---

## 🧪 **Testing**

**Run Feature Tests:**
```bash
python test_features.py
```

**Run Unit Tests:**
```bash
pytest tests/
```

---

## 🧱 **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI/LLM** | OpenRouter API, LangChain | Persona generation & analysis |
| **NLP** | scikit-learn, NLTK patterns | Topic modeling & text analysis |
| **Data Science** | pandas, numpy | Data processing & analytics |
| **Visualization** | Plotly, matplotlib, wordcloud | Interactive charts & graphs |
| **Web Framework** | Streamlit | Advanced GUI dashboard |
| **Reddit API** | PRAW | Data extraction |
| **Document Generation** | ReportLab | PDF export functionality |

---

## 🎯 **Use Cases**

- **🔬 Research** - Academic studies on online behavior patterns
- **📈 Marketing** - Social media audience analysis and segmentation  
- **🛡️ Security** - Digital forensics and user profiling
- **🎮 Gaming** - Community management and player behavior analysis
- **💼 HR** - Social media background screening (ethical use)
- **🧠 Psychology** - Digital personality assessment research

---

## 🔮 **Advanced Features Roadmap**

- ✅ **Big Five Personality Analysis** - Complete psychological profiling
- ✅ **Topic Modeling with LDA** - Automated content categorization
- ✅ **Social Network Analysis** - Community interaction mapping
- ✅ **Writing Style Analysis** - Linguistic pattern recognition
- ✅ **Activity Timeline Analysis** - Behavioral pattern detection
- ✅ **Multi-user Comparison** - Side-by-side analysis
- ✅ **Interactive Dashboard** - Advanced web interface
- ✅ **PDF Export** - Professional report generation

**Future Enhancements:**
- 🔄 **Real-time Analysis** - Live data streaming
- 🌐 **Multi-platform Support** - Twitter, LinkedIn integration
- 🤖 **API Endpoints** - RESTful service architecture
- 📧 **Automated Reporting** - Scheduled analysis delivery
- 🔒 **Privacy Controls** - GDPR compliance features

---

## 🧑‍💻 **Contributors**

**Shailendra Dhakad** - *Creator & Lead Developer*
- 🧠 AI/ML Architecture
- 📊 Advanced Analytics Implementation  
- 🖥️ Full-stack Development

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 **Contributing**

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ **Ethical Usage**

This tool is designed for:
- ✅ Research and academic purposes
- ✅ Personal profile analysis (with consent)
- ✅ Community behavior studies
- ✅ Content strategy development

**Please ensure:**
- 🔒 Respect user privacy and Reddit's terms of service
- 📋 Obtain appropriate permissions for research use
- 🛡️ Use responsibly and ethically
- 📊 Consider data anonymization for sensitive applications

---

**Made with ❤️ using AI, Python, and curiosity about human behavior in digital spaces.**
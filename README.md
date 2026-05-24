# WhatsApp Insight 📊

A premium WhatsApp Chat Analyzer built with Python and Streamlit. Transform your exported chat history into interactive visual intelligence.

## ✨ Features

- **Premium UI**: Glassmorphic dark-theme design with modern aesthetics.
- **Interactive Reports**: Powered by Plotly for zoomable and hoverable charts.
- **Deep Insights**:
  - **Message Volume**: Daily and monthly trends.
  - **Activity Mapping**: Identify the busiest days and hours.
  - **User Comparison**: Compare activity across group members.
  - **Content Analysis**: Wordclouds and common word frequency (with Hinglish filtering).
  - **Emoji Sentiment**: Analyze the most used emojis.

## 🚀 Getting Started

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/ShaikhWahid99/Whatsapp-Chat-Analyzer.git
cd Whatsapp-Chat-Analyzer

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

## 📱 How to Export Your Chat
1. Open the WhatsApp chat you want to analyze.
2. Tap the three dots (Menu) > **More** > **Export chat**.
3. Select **Without Media** for a faster export.
4. Upload the generated `.txt` file to the app.

## 🛠️ Tech Stack
- **Dashboard**: Streamlit
- **Data Processing**: Pandas, Regex
- **Visualization**: Plotly, Matplotlib, Seaborn
- **NLP**: WordCloud, URLExtract, Emoji

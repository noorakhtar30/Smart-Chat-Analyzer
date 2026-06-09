import pandas as pd
from datetime import datetime
import helper
import streamlit as st
import base64
import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv



class WhatsAppChatBot:
    def __init__(self):
        self.chat_history = []

        # SVG-based profile logos (customize colors as needed)
        self.user_logo = self._generate_svg_icon("U", "#25D366")  # Green for user
        self.bot_logo = self._generate_svg_icon("B", "#128C7E")  # Teal for bot

        # Load environment variables from .env file
        load_dotenv('.envapi')

        # Initialize Google Generative AI API
        # Try to get API key from environment variables first
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        # Try to get from Streamlit secrets only if available
        try:
            if not api_key:
                api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        except (FileNotFoundError, AttributeError):
            # Secrets not available, continue without them
            pass

        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.llm_available = True
                # Initialize the model
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                st.success("Connected to Google Gemini API successfully!")
            except Exception as e:
                st.error(f"Failed to initialize Gemini API: {e}")
                self.llm_available = False
        else:
            self.llm_available = False
            st.warning("Gemini API key not found. Using rule-based responses only.")

    def _generate_svg_icon(self, initial, bg_color):
        """Generate a circular SVG profile icon with initial"""
        svg = f"""
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="16" fill="{bg_color}"/>
            <text x="16" y="21" font-family="Arial" font-size="14" 
                  fill="white" text-anchor="middle" font-weight="bold">{initial}</text>
        </svg>
        """
        return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

    def render_chat(self):
        """Render chat with profile logos"""
        chat_html = """
        <style>
            .chat-container {
                height: 400px;
                overflow-y: auto;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 10px;
                margin-bottom: 10px;
            }
            .message-row {
                display: flex;
                margin: 10px 0;
                align-items: flex-start;
            }
            .user-row {
                justify-content: flex-end;
            }
            .bot-row {
                justify-content: flex-start;
            }
            .profile-logo {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                margin: 0 8px;
                flex-shrink: 0;
            }
            .user-message {
                background: #DCF8C6;
                padding: 8px 12px;
                border-radius: 15px 15px 0 15px;
                max-width: 70%;
                font-size: 14px;
                word-wrap: break-word;
            }
            .bot-message {
                background: #ECECEC;
                padding: 8px 12px;
                border-radius: 15px 15px 15px 0;
                max-width: 70%;
                font-size: 14px;
                word-wrap: break-word;
            }
        </style>
        <div class="chat-container">
        """

        for message in self.chat_history:
            if message['is_user']:
                chat_html += f"""
                <div class="message-row user-row">
                    <div class="user-message">{message['message']}</div>
                    <img src="{self.user_logo}" class="profile-logo" />
                </div>
                """
            else:
                chat_html += f"""
                <div class="message-row bot-row">
                    <img src="{self.bot_logo}" class="profile-logo" />
                    <div class="bot-message">{message['message']}</div>
                </div>
                """

        chat_html += "</div>"
        return chat_html

    def generate_llm_response(self, user_input: str, selected_user: str, df: pd.DataFrame) -> Optional[str]:
        """Generate a response using Google's Generative AI API with access to chat analysis data"""
        if not self.llm_available:
            return None

        try:
            # Prepare context about the chat data
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

            # Create a system prompt
            system_prompt = f"""You are a helpful WhatsApp chat analysis assistant. 
            You're analyzing a chat with the following statistics:
            - Total messages: {num_messages}
            - Total words: {words}
            - Media files shared: {num_media_messages}
            - Links shared: {num_links}

            You have access to various analysis functions through the helper module.
            Provide helpful, concise responses about the chat data.
            If you're asked about something not related to chat analysis, politely redirect.
            """

            # Add conversation history
            conversation_history = ""
            for msg in self.chat_history[-6:]:  # Last 6 messages
                role = "User" if msg["is_user"] else "Assistant"
                conversation_history += f"{role}: {msg['message']}\n"

            # Combine everything
            full_prompt = f"{system_prompt}\n\n{conversation_history}\nUser: {user_input}\nAssistant:"

            # Generate response
            response = self.model.generate_content(full_prompt)

            return response.text.strip()

        except Exception as e:
            st.error(f"Error calling Gemini API: {e}")
            return None

    def generate_rule_based_response(self, user_input, selected_user, df):
        """Original rule-based response system (as fallback)"""
        user_input = user_input.lower().strip()
        response = ""

        # Get basic stats for responses
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Greetings
        if any(word in user_input for word in ["hi", "hello", "hey", "hola"]):
            return "Hello! I'm your WhatsApp Chat Analyzer bot. I can help you analyze your chat data. " \
                   "You can ask me about message statistics, active users, word clouds, and more!"

        # Help menu
        if "help" in user_input or "what can you do" in user_input:
            return "I can help you analyze your WhatsApp chat data. Here are some things you can ask:\n" \
                   "- Total messages/words/media/links\n" \
                   "- Most active user/day/month\n" \
                   "- Show me the word cloud\n" \
                   "- Conversation starters\n" \
                   "- Sentiment analysis\n" \
                   "- Message timeline\n" \
                   "- Response times\n" \
                   "- Inactive users"

        # Basic stats
        if "total messages" in user_input or "how many messages" in user_input:
            return f"There are {num_messages} total messages in this chat."

        if "total words" in user_input or "how many words" in user_input:
            return f"There are {words} total words in this chat."

        if "media" in user_input or "photos" in user_input or "videos" in user_input:
            return f"{num_media_messages} media files (photos/videos) were shared in this chat."

        if "links" in user_input or "urls" in user_input:
            return f"{num_links} links were shared in this chat."

        # Active users analysis
        if "most active user" in user_input or "who talked most" in user_input:
            if selected_user != "Overall":
                return "You're viewing analysis for a specific user. Switch to 'Overall' to see most active users."
            x, new_df = helper.most_busy_users(df)
            return f"The most active users are:\n{new_df.to_string(index=False)}"

        # Timeline questions
        if "timeline" in user_input or "message frequency" in user_input:
            return "Showing message timeline (check the charts section for visualizations). " \
                   f"On average, there are {num_messages / len(df['only_date'].unique()):.1f} messages per day."

        # Word cloud
        if "word cloud" in user_input or "common words" in user_input:
            return "Here's the word cloud showing most frequently used words (check the visualization). " \
                   "You can also ask about 'most common words' for a detailed list."

        # Emoji analysis
        if "emoji" in user_input or "most used emoji" in user_input:
            emoji_df = helper.emoji_helper(selected_user, df)
            return f"The most used emojis are:\n{emoji_df.head().to_string(index=False)}"

        # Sentiment analysis
        if "sentiment" in user_input or "mood" in user_input or "tone" in user_input:
            return "Showing sentiment analysis (check the visualization). " \
                   "This analyzes whether messages are generally positive, negative or neutral."

        # Conversation starters
        if "started" in user_input or "initiated" in user_input:
            starters_df = helper.conversation_starters(df)
            return f"These users started the most conversations:\n{starters_df.head().to_string(index=False)}"

        # Response times
        if "response" in user_input or "reply" in user_input or "answer" in user_input:
            response_df = helper.response_time_analysis(df)
            if not response_df.empty:
                return f"Average response times:\n{response_df.to_string(index=False)}"
            return "Not enough data to calculate response times."

        # Inactive users
        if "inactive" in user_input or "not active" in user_input:
            inactive_users = helper.find_inactive_users(df, days=7)
            if inactive_users:
                return f"These users have been inactive for 7+ days: {', '.join(inactive_users)}"
            return "All users have been active recently!"

        # Date filtering questions
        if "when" in user_input or "date" in user_input or "time" in user_input:
            timeline = helper.monthly_timeline(selected_user, df)
            peak_month = timeline.loc[timeline['message'].idxmax()]
            return f"The busiest month was {peak_month['time']} with {peak_month['message']} messages."

        # Default response
        return "I'm not sure I understand. Try asking about:\n" \
               "- Message statistics\n" \
               "- Most active users\n" \
               "- Word cloud\n" \
               "- Sentiment analysis\n" \
               "Or type 'help' for more options."

    def generate_response(self, user_input, selected_user, df):
        """Generate response using Gemini API first, fall back to rule-based if needed"""
        # Try Gemini API first
        gemini_response = self.generate_llm_response(user_input, selected_user, df)

        if gemini_response:
            return gemini_response
        else:
            # Fall back to rule-based system
            return self.generate_rule_based_response(user_input, selected_user, df)

    def add_to_history(self, message, is_user):
        self.chat_history.append({
            "message": message,
            "is_user": is_user,
            "time": datetime.now().strftime("%H:%M")
        })

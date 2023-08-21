**Top Tracks Analysis**
This is a web application project that displays the analysis/summary of a user recent top tracks on Spotify

**Tech stack**
- React.js 
- Python 
- Flask 
- OpenAI 
- SQLite 
- Spotify Web API

**Description**
- The React frontend prompts the user for number of tracks they want to include in summary/analysis and the time range (short, medium, or    long term).
- Flask backend authenticates the user's Spotify account and retrieve data using Spotify Web API.
- The data is then restructured and passed into ChatGPT model to get the analysis. The analysis mainly includes the summary of the user's music preferences and a prediction of the user's mood.

**Limitations**
- The application currently can only analyze my personal Spotify data because I have not implemented sessions and any other approaches to protect the user's privacy
- Single functionality, looking to add more components to this application

**Next Step**:
- I will be adding a user login page and track the user's history of analysis
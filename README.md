# WhatsApp Wrap  
**WhatsApp Wrap** is a tool designed to analyze your WhatsApp chat data. By uploading your exported chat files, you can gain insights into your messaging habits, including participant activity, word usage, and emoji trends.
To access the tool visit: https://whatsappwrap-dhruvitagrawal.streamlit.app/

## Features  
- **Participant Analysis**: Discover who you message the most.  
- **Word Cloud Generation**: Visualize frequently used words in your chats.  
- **Emoji Analysis**: Understand your emoji usage and preferences.  
- **Interactive Visualizations**: Explore your data through engaging charts and graphs.  

## Installation  
To run WhatsApp Wrap locally, follow these steps:  
1. **Clone the repository**:
  '''bash
git clone https://github.com/Dhruvit-Agrawal/whatsapp-wrap.git
cd whatsapp-wrap

3. **Set up a virtual environment (optional but recommended)**:
  '''python  
python -m venv env
source env/bin/activate # On Windows use env\Scripts\activate

4. **Install the required packages**:
  '''python
pip install -r requirements.txt


## Usage  
1. **Export your WhatsApp chat** as a text file:  
- Open the chat you want to analyze.  
- Tap on the three dots in the top right corner.  
- Select "More" > "Export Chat".  
- Choose "Without Media".  

2. **Run the application**:
'''python
streamlit run app.py



4. **Upload the exported chat file** in the app interface.  

5. **Select a user** from the dropdown menu and click the **"Show Analysis"** button to view insights.  

## Contributing  
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.  

1. Fork the repository.  
2. Create a new branch (`git checkout -b feature-branch`).  
3. Make your changes and commit them (`git commit -m 'Add new feature'`).  
4. Push to the branch (`git push origin feature-branch`).  
5. Open a pull request.  


## Acknowledgments  
- Thanks to [Streamlit](https://streamlit.io/) for providing an easy way to build web applications with Python.  


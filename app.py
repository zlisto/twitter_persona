import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import StringIO
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Page configuration
st.set_page_config(
    page_title="TweetRealm",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define custom CSS for the app
def local_css():
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --pink-color: #ec489a;
            --green-color: #1e8449;
            --purple-color: #9c27b0;
            --gradient-header: linear-gradient(90deg, var(--pink-color), var(--purple-color), var(--green-color));
        }
        
        /* Header styling */
        .main-header {
            background: var(--gradient-header);
            padding: 1.5rem 0;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            margin: 0;
            font-weight: bold;
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
        }
        
        /* Upload area styling */
        .upload-area {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: 2px solid;
            border-image: linear-gradient(45deg, var(--pink-color), var(--green-color)) 1;
            border-radius: 0.5rem;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .upload-title {
            background: var(--gradient-header);
            -webkit-background-clip: text;
            color: transparent;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        
        /* Table styling */
        .dataframe {
            width: 100%;
            border-collapse: collapse;
        }
        
        .dataframe th {
            background: linear-gradient(90deg, rgba(236, 72, 154, 0.1), rgba(30, 132, 73, 0.1));
            color: #444;
            padding: 0.5rem 1rem;
            text-align: left;
            font-size: 0.9rem;
            text-transform: uppercase;
        }
        
        .dataframe tr:nth-child(odd) {
            background: linear-gradient(90deg, rgba(236, 72, 154, 0.05), rgba(255, 255, 255, 0.05));
        }
        
        .dataframe tr:nth-child(even) {
            background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(30, 132, 73, 0.05));
        }
        
        /* Hiding Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Adjusting default Streamlit elements */
        .stAlert > div {
            border-image: linear-gradient(45deg, var(--pink-color), var(--green-color)) 1;
            border-width: 2px;
            border-style: solid;
        }
        
        /* Background images for left and right sides */
        .left-bg, .right-bg {
            position: fixed;
            top: 0;
            height: 100%;
            width: 20%;
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.15;
            z-index: -1;
            pointer-events: none;
        }
        
        .left-bg {
            left: 0;
            background-position: left center;
        }
        
        .right-bg {
            right: 0;
            background-position: right center;
        }
        
        /* Styling for the city background */
        .city-bg {
            position: fixed;
            bottom: 0;
            left: 25%;
            width: 50%;
            height: 30%;
            background-size: 80% auto;
            background-position: bottom center;
            background-repeat: no-repeat;
            opacity: 0.1;
            z-index: -1;
            pointer-events: none;
        }
        
        /* Custom file uploader */
        .custom-uploader {
            border: 2px dashed rgba(156, 39, 176, 0.4);
            border-radius: 0.5rem;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
            background: rgba(255, 255, 255, 0.6);
            transition: all 0.3s;
        }
        
        .custom-uploader:hover {
            border-color: var(--purple-color);
            background: rgba(255, 255, 255, 0.8);
        }
        
        /* Footer styling */
        .footer {
            background: var(--gradient-header);
            padding: 1rem 0;
            text-align: center;
            color: white;
            border-radius: 0.5rem;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to encode images as base64 for CSS background
def get_image_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

# Function to create background images
def add_background_images():
    # URLs would be used in production, but we need local placeholders for now
    # Let's create simple placeholder images
    
    # Create directory for images if it doesn't exist
    os.makedirs("temp_images", exist_ok=True)
    
    # Create a simple pink blossom image
    blossom = Image.new('RGBA', (400, 800), (0, 0, 0, 0))
    for i in range(50):
        x = np.random.randint(0, 400)
        y = np.random.randint(0, 800)
        size = np.random.randint(10, 30)
        color = (255, 182, 193, np.random.randint(100, 200))
        blossom.paste(Image.new('RGBA', (size, size), color), (x, y), Image.new('RGBA', (size, size), color))
    blossom.save("temp_images/blossom.png")
    
    # Create a simple green branches image
    branches = Image.new('RGBA', (400, 800), (0, 0, 0, 0))
    for i in range(30):
        x = np.random.randint(0, 400)
        y = np.random.randint(0, 800)
        width = np.random.randint(5, 15)
        height = np.random.randint(30, 100)
        color = (34, 139, 34, np.random.randint(100, 200))
        branches.paste(Image.new('RGBA', (width, height), color), (x, y))
    branches.save("temp_images/branches.png")
    
    # Create a simple city silhouette
    city = Image.new('RGBA', (800, 300), (0, 0, 0, 0))
    for i in range(20):
        x = np.random.randint(0, 700)
        y = 100
        width = np.random.randint(30, 80)
        height = np.random.randint(100, 200)
        color = (100, 100, 100, 150)
        city.paste(Image.new('RGBA', (width, height), color), (x, y))
    city.save("temp_images/city.png")
    
    # Convert images to base64 for CSS
    blossom_b64 = get_image_as_base64("temp_images/blossom.png")
    branches_b64 = get_image_as_base64("temp_images/branches.png")
    city_b64 = get_image_as_base64("temp_images/city.png")
    
    # Add the background images
    st.markdown(f"""
    <div class="left-bg" style="background-image: url('{blossom_b64}');"></div>
    <div class="right-bg" style="background-image: url('{branches_b64}');"></div>
    <div class="city-bg" style="background-image: url('{city_b64}');"></div>
    """, unsafe_allow_html=True)

# Header component
def header():
    st.markdown("""
    <div class="main-header">
        <h1>TweetRealm</h1>
        <p>Where Good & Wicked Tweets Collide</p>
    </div>
    """, unsafe_allow_html=True)

# Footer component
def footer():
    st.markdown(f"""
    <div class="footer">
        <p>TweetRealm &copy; {pd.Timestamp.now().year} | The Magic of East and West Combined</p>
    </div>
    """, unsafe_allow_html=True)

# Function to color text based on engagement
def color_tweets(val, engagement, index):
    # Style alternating rows with pink or green theme
    if index % 2 == 0:
        # Pink (Glinda) theme
        hue = 330  # Pink
        saturation = 60 + (min(engagement, 1) * 40)  # 60% to 100%
        lightness = 70 - (min(engagement, 1) * 20)   # 70% to 50%
    else:
        # Green (Witch) theme
        hue = 120  # Green
        saturation = 50 + (min(engagement, 1) * 50)  # 50% to 100%
        lightness = 25 + (min(engagement, 1) * 15)   # 25% to 40%
    
    # Convert HSL to RGB to Hex
    rgb = mcolors.hsv_to_rgb([hue/360, saturation/100, lightness/100])
    hex_color = mcolors.rgb2hex(rgb)
    
    # Add text-shadow for higher engagement
    shadow = ''
    weight = 400 + int(min(engagement, 1) * 300)
    
    if engagement > 0.2:
        shadow_size = 3 + int(min(engagement, 1) * 5)
        shadow_color = hex_color + "40"  # 40% opacity
        shadow = f"text-shadow: 0 0 {shadow_size}px {shadow_color};"
    
    return f'color: {hex_color}; font-weight: {weight}; {shadow}'

# Function to style engagement badges
def style_engagement_badge(val, engagement, index):
    # Style alternating rows with pink or green theme
    if index % 2 == 0:
        # Pink (Glinda) theme
        hue = 330  # Pink
        saturation = 60 + (min(engagement, 1) * 40)  # 60% to 100%
        lightness = 70 - (min(engagement, 1) * 20)   # 70% to 50%
    else:
        # Green (Witch) theme
        hue = 120  # Green
        saturation = 50 + (min(engagement, 1) * 50)  # 50% to 100%
        lightness = 25 + (min(engagement, 1) * 15)   # 25% to 40%
    
    # Convert HSL to RGB to Hex
    rgb = mcolors.hsv_to_rgb([hue/360, saturation/100, lightness/100])
    hex_color = mcolors.rgb2hex(rgb)
    
    # Add box-shadow for higher engagement
    shadow = ''
    if engagement > 0.1:
        shadow_size = 3 + int(min(engagement, 1) * 6)
        shadow_color = hex_color + "40"  # 40% opacity
        shadow = f"box-shadow: 0 0 {shadow_size}px {shadow_color};"
    
    # Background with low opacity
    bg_color = hex_color + "30"  # 30% opacity
    
    return f'''
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 0.375rem;
    background-color: {bg_color};
    color: {hex_color};
    font-weight: bold;
    {shadow}
    '''

# Function to process the uploaded CSV
def process_csv(uploaded_file):
    # Read the CSV
    df = pd.read_csv(uploaded_file)
    
    # Check for required columns
    required_columns = ['text', 'favorite_count', 'view_count']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}. Please ensure your CSV has text, favorite_count, and view_count columns.")
        return None
    
    # Calculate engagement
    df['favorite_count'] = df['favorite_count'].fillna(0).astype(int)
    df['view_count'] = df['view_count'].fillna(1).astype(int)
    df['view_count'] = df['view_count'].apply(lambda x: max(x, 1))  # Prevent division by zero
    df['engagement'] = df['favorite_count'] / df['view_count']
    
    return df

# Function to display the styled dataframe
def display_styled_data(df):
    # Format the numbers in favorite_count and view_count
    df['favorite_count_fmt'] = df['favorite_count'].apply(lambda x: f"{x:,}")
    df['view_count_fmt'] = df['view_count'].apply(lambda x: f"{x:,}")
    df['engagement_fmt'] = df['engagement'].apply(lambda x: f"{x*100:.2f}%")
    
    # Create a stylable dataframe with just the columns we want to display
    display_df = df[['text', 'favorite_count_fmt', 'view_count_fmt', 'engagement_fmt']].rename(
        columns={
            'text': 'Tweet', 
            'favorite_count_fmt': 'Favorites', 
            'view_count_fmt': 'Views', 
            'engagement_fmt': 'Engagement'
        }
    )
    
    # Apply styling
    styled_df = display_df.style.apply(
        lambda row: [
            color_tweets(row['Tweet'], df.iloc[row.name]['engagement'], row.name),
            '',
            '',
            style_engagement_badge(row['Engagement'], df.iloc[row.name]['engagement'], row.name)
        ],
        axis=1
    )
    
    # Display the styled dataframe
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

# Main app function
def main():
    # Apply CSS and background images
    local_css()
    add_background_images()
    
    # Display header
    header()
    
    # File uploader section
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    if st.session_state.data is None:
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        st.markdown('<h2 class="upload-title">Upload Your Magical Tweets</h2>', unsafe_allow_html=True)
        st.markdown("""
        <p>Drag and drop a CSV file below, or click to browse files.
        Your CSV should have columns: text, favorite_count, and view_count.</p>
        <div class="custom-uploader">
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="file_uploader")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            df = process_csv(uploaded_file)
            if df is not None:
                st.session_state.data = df
                st.session_state.filename = uploaded_file.name
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Display the data with a new upload button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <h2 style="background: linear-gradient(90deg, #ec489a, #1e8449); 
                      -webkit-background-clip: text; 
                      color: transparent; 
                      font-weight: bold;">
                ✨ Analyzing: {st.session_state.filename}
            </h2>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Upload New File", key="new_file"):
                st.session_state.data = None
                st.experimental_rerun()
        
        # Display the styled dataframe
        display_styled_data(st.session_state.data)
    
    # Display footer
    footer()

if __name__ == "__main__":
    main()
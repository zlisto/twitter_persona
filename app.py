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
    page_title="Emerald TweetCity",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define custom CSS for the app
def local_css():
    st.markdown("""
    <style>
        /* Main theme colors from Wizard of Oz */
        :root {
            --emerald-green: #00A651;
            --ruby-red: #E31B23;
            --yellow-brick: #F8D568;
            --witch-purple: #6B3FA0;
            --scarecrow-tan: #F2CC8F;
            --tin-man-silver: #C0C0C0;
            --lion-gold: #D4AF37;
            --poppy-red: #FF5C5C;
            --oz-gradient: linear-gradient(90deg, var(--emerald-green), var(--yellow-brick), var(--ruby-red));
        }
        
        /* Wizard of Oz font styles */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Lato', sans-serif;
            background-color: #FFFBF0;  /* Slightly off-white like aged pages of a book */
        }
        
        h1, h2, h3, h4 {
            font-family: 'Playfair Display', serif;
        }
        
        /* Header styling - Emerald City inspired */
        .main-header {
            background: var(--oz-gradient);
            padding: 2rem 0;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                45deg,
                rgba(255, 255, 255, 0.1),
                rgba(255, 255, 255, 0.1) 10px,
                rgba(255, 255, 255, 0.2) 10px,
                rgba(255, 255, 255, 0.2) 20px
            );
        }
        
        .main-header h1 {
            color: white;
            font-size: 3rem;
            margin: 0;
            font-weight: bold;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            position: relative;
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
            font-style: italic;
            position: relative;
        }
        
        /* Upload area styling - Yellow Brick Road */
        .upload-area {
            background: linear-gradient(135deg, var(--scarecrow-tan), var(--yellow-brick));
            border: 3px solid var(--lion-gold);
            border-radius: 0.5rem;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
            position: relative;
        }
        
        .upload-area::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                90deg,
                rgba(255, 215, 0, 0.1),
                rgba(255, 215, 0, 0.1) 20px,
                rgba(255, 215, 0, 0.2) 20px,
                rgba(255, 215, 0, 0.2) 40px
            );
            border-radius: 0.25rem;
            z-index: 0;
        }
        
        .upload-area > * {
            position: relative;
            z-index: 1;
        }
        
        .upload-title {
            color: var(--witch-purple);
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
        }
        
        /* Table styling - Emerald City records */
        .dataframe {
            width: 100%;
            border-collapse: collapse;
            border: 2px solid var(--emerald-green);
            font-family: 'Lato', sans-serif;
        }
        
        .dataframe th {
            background: var(--emerald-green);
            color: white;
            padding: 0.75rem 1rem;
            text-align: left;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .dataframe tr:nth-child(odd) {
            background: linear-gradient(90deg, rgba(248, 213, 104, 0.2), rgba(255, 255, 255, 0.2));
        }
        
        .dataframe tr:nth-child(even) {
            background: linear-gradient(90deg, rgba(192, 192, 192, 0.2), rgba(0, 166, 81, 0.1));
        }
        
        .dataframe td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(0, 166, 81, 0.2);
        }
        
        /* Hiding Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Adjusting default Streamlit elements */
        .stAlert > div {
            border: 2px solid var(--ruby-red);
            border-radius: 0.5rem;
        }
        
        /* Wizard of Oz themed background elements */
        .yellow-brick-road {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 10%;
            background: linear-gradient(0deg, var(--yellow-brick), transparent);
            opacity: 0.3;
            z-index: -1;
            pointer-events: none;
        }
        
        .emerald-city-bg {
            position: fixed;
            bottom: 10%;
            left: 25%;
            width: 50%;
            height: 30%;
            background-size: 100% auto;
            background-position: bottom center;
            background-repeat: no-repeat;
            opacity: 0.15;
            z-index: -1;
            pointer-events: none;
        }
        
        .rainbow-arc {
            position: fixed;
            top: 0;
            right: 0;
            width: 25%;
            height: 50%;
            background: linear-gradient(
                to right,
                rgba(255,0,0,0.1),
                rgba(255,165,0,0.1),
                rgba(255,255,0,0.1),
                rgba(0,128,0,0.1),
                rgba(0,0,255,0.1),
                rgba(75,0,130,0.1),
                rgba(238,130,238,0.1)
            );
            border-radius: 0 0 0 100%;
            opacity: 0.3;
            z-index: -1;
            pointer-events: none;
        }
        
        .poppy-field-left {
            position: fixed;
            bottom: 10%;
            left: 0;
            width: 20%;
            height: 20%;
            opacity: 0.2;
            z-index: -1;
            pointer-events: none;
        }
        
        .tornado-right {
            position: fixed;
            top: 20%;
            right: 5%;
            width: 10%;
            height: 40%;
            opacity: 0.1;
            z-index: -1;
            pointer-events: none;
            animation: rotate 20s infinite linear;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Custom file uploader - Ruby Slippers style */
        .custom-uploader {
            border: 3px dashed var(--ruby-red);
            border-radius: 0.5rem;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
            background: rgba(255, 255, 255, 0.6);
            transition: all 0.3s;
            position: relative;
        }
        
        .custom-uploader:hover {
            border-color: var(--ruby-red);
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 15px var(--ruby-red);
        }
        
        .custom-uploader::before, .custom-uploader::after {
            content: "👠";
            position: absolute;
            font-size: 1.5rem;
            bottom: -0.5rem;
        }
        
        .custom-uploader::before {
            left: 2rem;
        }
        
        .custom-uploader::after {
            right: 2rem;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--emerald-green);
            color: white;
            font-family: 'Playfair Display', serif;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        
        .stButton > button:hover {
            background-color: var(--witch-purple);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Footer styling - Yellow Brick Road */
        .footer {
            background: linear-gradient(90deg, var(--yellow-brick), var(--lion-gold), var(--yellow-brick));
            padding: 1rem 0;
            text-align: center;
            color: var(--witch-purple);
            border-radius: 0.5rem;
            margin-top: 2rem;
            font-family: 'Playfair Display', serif;
            position: relative;
            overflow: hidden;
        }
        
        .footer::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                90deg,
                rgba(255, 215, 0, 0.1),
                rgba(255, 215, 0, 0.1) 20px,
                rgba(255, 215, 0, 0.2) 20px,
                rgba(255, 215, 0, 0.2) 40px
            );
        }
    </style>
    """, unsafe_allow_html=True)

# Function to encode images as base64 for CSS background
def get_image_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

# Function to create Wizard of Oz themed background images
def add_background_images():
    # Create directory for images if it doesn't exist
    os.makedirs("oz_images", exist_ok=True)
    
    # Create a simple Emerald City silhouette
    emerald_city = Image.new('RGBA', (800, 400), (0, 0, 0, 0))
    # Main castle/tower shapes
    for i in range(7):
        x = 100 + i * 100
        width = 60
        height = 150 + np.random.randint(-30, 50)
        color = (0, 166, 81, 100)  # Emerald green with transparency
        
        # Draw tower
        tower = Image.new('RGBA', (width, height), color)
        emerald_city.paste(tower, (x, 400 - height), tower)
        
        # Add tower top
        top_width = width + 20
        top_height = 40
        top = Image.new('RGBA', (top_width, top_height), color)
        emerald_city.paste(top, (x - 10, 400 - height - top_height), top)
        
        # Add spire for some towers
        if i % 2 == 0:
            spire_width = 20
            spire_height = 60
            spire = Image.new('RGBA', (spire_width, spire_height), color)
            emerald_city.paste(spire, (x + width//2 - spire_width//2, 400 - height - top_height - spire_height), spire)
    emerald_city.save("oz_images/emerald_city.png")
    
    # Create a poppy field (red dots pattern)
    poppy_field = Image.new('RGBA', (400, 300), (0, 0, 0, 0))
    for i in range(100):
        x = np.random.randint(0, 400)
        y = np.random.randint(100, 300)
        size = np.random.randint(5, 15)
        color = (227, 27, 35, np.random.randint(100, 200))  # Ruby red with transparency
        poppy = Image.new('RGBA', (size, size), color)
        poppy_field.paste(poppy, (x, y), poppy)
    poppy_field.save("oz_images/poppy_field.png")
    
    # Create a simple tornado shape
    tornado = Image.new('RGBA', (200, 500), (0, 0, 0, 0))
    # Draw tornado as a series of ovals decreasing in size
    for i in range(10):
        y_pos = i * 50
        width = 150 - (i * 10)
        height = 80
        # Create oval shape
        oval = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        # Draw the oval
        for x in range(width):
            for y in range(height):
                # Calculate distance from center
                dx = x - width/2
                dy = y - height/2
                distance = (dx**2/(width/2)**2 + dy**2/(height/2)**2)**0.5
                
                if distance <= 1:
                    # Gradient from center to edge
                    alpha = int(100 * (1 - distance))
                    oval.putpixel((x, y), (100, 100, 100, alpha))
        
        # Position the oval in the tornado image
        offset_x = (200 - width) // 2
        tornado.paste(oval, (offset_x, y_pos), oval)
    tornado.save("oz_images/tornado.png")
    
    # Convert images to base64 for CSS
    emerald_city_b64 = get_image_as_base64("oz_images/emerald_city.png")
    poppy_field_b64 = get_image_as_base64("oz_images/poppy_field.png")
    tornado_b64 = get_image_as_base64("oz_images/tornado.png")
    
    # Add the background images
    st.markdown(f"""
    <div class="yellow-brick-road"></div>
    <div class="emerald-city-bg" style="background-image: url('{emerald_city_b64}');"></div>
    <div class="rainbow-arc"></div>
    <div class="poppy-field-left" style="background-image: url('{poppy_field_b64}');"></div>
    <div class="tornado-right" style="background-image: url('{tornado_b64}');"></div>
    """, unsafe_allow_html=True)

# Header component
def header():
    st.markdown("""
    <div class="main-header">
        <h1>Emerald TweetCity</h1>
        <p>"There's no place like home for your tweets"</p>
    </div>
    """, unsafe_allow_html=True)

# Footer component
def footer():
    st.markdown(f"""
    <div class="footer">
        <p>Follow the Yellow Brick Road of Data &copy; {pd.Timestamp.now().year} | Somewhere Over the Rainbow</p>
    </div>
    """, unsafe_allow_html=True)

# Function to color text based on engagement with Wizard of Oz color scheme
def color_tweets(val, engagement, index):
    # Style alternating rows with different Oz character themes
    if index % 4 == 0:
        # Emerald City theme (green)
        hue = 140  # Emerald Green
        saturation = 60 + (min(engagement, 1) * 40)  # 60% to 100%
        lightness = 30 - (min(engagement, 1) * 10)   # 30% to 20%
    elif index % 4 == 1:
        # Ruby Slippers theme (red)
        hue = 0  # Ruby Red
        saturation = 80 + (min(engagement, 1) * 20)  # 80% to 100%
        lightness = 45 - (min(engagement, 1) * 15)   # 45% to 30%
    elif index % 4 == 2:
        # Yellow Brick Road theme
        hue = 45  # Golden Yellow
        saturation = 70 + (min(engagement, 1) * 30)  # 70% to 100%
        lightness = 50 - (min(engagement, 1) * 10)   # 50% to 40%
    else:
        # Wicked Witch theme (purple)
        hue = 270  # Purple
        saturation = 60 + (min(engagement, 1) * 40)  # 60% to 100%
        lightness = 30 - (min(engagement, 1) * 10)   # 30% to 20%
    
    # Convert HSL to RGB to Hex
    rgb = mcolors.hsv_to_rgb([hue/360, saturation/100, lightness/100])
    hex_color = mcolors.rgb2hex(rgb)
    
    # Add text-shadow for higher engagement - magical effect
    shadow = ''
    weight = 400 + int(min(engagement, 1) * 300)
    
    if engagement > 0.2:
        shadow_size = 2 + int(min(engagement, 1) * 4)
        shadow_color = hex_color + "60"  # 60% opacity
        shadow = f"text-shadow: 0 0 {shadow_size}px {shadow_color};"
    
    return f'color: {hex_color}; font-weight: {weight}; {shadow} font-family: "Playfair Display", serif;'

# Function to style engagement badges with Wizard of Oz themes
def style_engagement_badge(val, engagement, index):
    # Style alternating rows with different Oz character themes
    if index % 4 == 0:
        # Emerald City theme (green)
        background = "#00A65160"  # Emerald with transparency
        text_color = "#00A651"
        border = "#00A651"
    elif index % 4 == 1:
        # Ruby Slippers theme (red)
        background = "#E31B2340"  # Ruby with transparency
        text_color = "#E31B23"
        border = "#E31B23"
    elif index % 4 == 2:
        # Yellow Brick Road theme
        background = "#F8D56840"  # Yellow with transparency
        text_color = "#B8860B"  # Darker gold for readability
        border = "#D4AF37"
    else:
        # Wicked Witch theme (purple)
        background = "#6B3FA040"  # Purple with transparency
        text_color = "#6B3FA0"
        border = "#6B3FA0"
    
    # Add magical glow effect for higher engagement
    glow = ''
    if engagement > 0.1:
        glow_size = 3 + int(min(engagement, 1) * 7)
        glow_color = text_color + "50"  # 50% opacity
        glow = f"box-shadow: 0 0 {glow_size}px {glow_color};"
    
    return f'''
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 0.375rem;
    background-color: {background};
    color: {text_color};
    border: 1px solid {border};
    font-weight: bold;
    font-family: "Playfair Display", serif;
    {glow}
    '''

# Function to process the uploaded CSV
def process_csv(uploaded_file):
    # Read the CSV
    df = pd.read_csv(uploaded_file)
    
    # Check for required columns
    required_columns = ['text', 'favorite_count', 'view_count']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}. Your CSV should have text, favorite_count, and view_count columns.")
        return None
    
    # Calculate engagement
    df['favorite_count'] = df['favorite_count'].fillna(0).astype(int)
    df['view_count'] = df['view_count'].fillna(1).astype(int)
    df['view_count'] = df['view_count'].apply(lambda x: max(x, 1))  # Prevent division by zero
    df['engagement'] = df['favorite_count'] / df['view_count']
    
    return df

# Function to display the styled dataframe with Oz themes
def display_styled_data(df):
    # Format the numbers in favorite_count and view_count
    df['favorite_count_fmt'] = df['favorite_count'].apply(lambda x: f"{x:,}")
    df['view_count_fmt'] = df['view_count'].apply(lambda x: f"{x:,}")
    df['engagement_fmt'] = df['engagement'].apply(lambda x: f"{x*100:.2f}%")
    
    # Create a stylable dataframe with just the columns we want to display
    display_df = df[['text', 'favorite_count_fmt', 'view_count_fmt', 'engagement_fmt']].rename(
        columns={
            'text': 'Tweet', 
            'favorite_count_fmt': 'Hearts', 
            'view_count_fmt': 'Eyes', 
            'engagement_fmt': 'Magic Power'
        }
    )
    
    # Apply Wizard of Oz styling
    styled_df = display_df.style.apply(
        lambda row: [
            color_tweets(row['Tweet'], df.iloc[row.name]['engagement'], row.name),
            '',
            '',
            style_engagement_badge(row['Magic Power'], df.iloc[row.name]['engagement'], row.name)
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
        st.markdown('<h2 class="upload-title">Click Your Ruby Slippers Together & Upload Your Tweets</h2>', unsafe_allow_html=True)
        st.markdown("""
        <p>Follow the Yellow Brick Road and drop your CSV file below, or click to choose a file.
        Your CSV should have columns: text, favorite_count, and view_count.</p>
        <div class="custom-uploader">
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="file_uploader")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            with st.spinner("The Great Oz is processing your data..."):
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
            <h2 style="color: var(--emerald-green); 
                      font-family: 'Playfair Display', serif;
                      text-shadow: 0 1px 3px rgba(0, 166, 81, 0.3);
                      font-weight: bold;">
                🧙 The Great and Powerful Oz Analyzes: {st.session_state.filename}
            </h2>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🧪 Try Another Spell", key="new_file"):
                st.session_state.data = None
                st.rerun()
        
        # Display the styled dataframe
        display_styled_data(st.session_state.data)
    
        # Add a quote from the movie
        st.markdown("""
        <div style="text-align: center; font-style: italic; margin: 2rem 0; 
                    color: var(--witch-purple); font-family: 'Playfair Display', serif;">
            "Pay no attention to that man behind the curtain. The Great Oz has spoken!"
        </div>
        """, unsafe_allow_html=True)
    
    # Display footer
    footer()

if __name__ == "__main__":
    main()
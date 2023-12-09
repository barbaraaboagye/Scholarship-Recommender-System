import pandas as pd
import numpy as np
import streamlit as st
from fuzzywuzzy import fuzz
from annotated_text import annotated_text





st.sidebar.header("User input details") 


def front_page():
    st.subheader("Hi there! I am :blue[Barbara Aboagye 👷🏾] - _This is my first web app_ 💃🏿 ")
    st.title("Welcome to the School and Scholarship Search App (3SA)! 😊")
    st.write('_3SA will help you find schools and sholarships in your field of study in 5 secs._')
    #st.divider()

    st.subheader("📘 How to use",divider = "rainbow")
    st.write("To find scholarships, please follow these steps:")
    st.write("1. Enter the field you are looking for a scholarship in.")
    st.write("2. Select the level of scholarship you are interested in (e.g., BSc, MSc, PhD, etc).")
    st.write("3. Click the 'Find Scholarships' button to see the recommendations.")
    st.write("4. Share with your friends!")

def callback():
    st.session_state.find_scholarships_button = True
    
    
    
def input_parameters():
    scholarship_df = pd.read_csv('scholarship_df.csv')
    fields = [''] + sorted(scholarship_df['Area of specialisation'].unique())
    levels = [''] + sorted(scholarship_df['Level needed'].unique())
    countries = [''] + sorted(scholarship_df['Country'].unique())
    
    # Use st.sidebar.text_input and st.sidebar.selectbox with the default values
    field = st.sidebar.selectbox("What field are you looking for a scholarship in?",fields)
    user_specialization = field.lower()

    level = st.sidebar.selectbox("Select a level", levels)
    level = level.lower()
    
    # Optional: Allow user to input country
    country = st.sidebar.selectbox("Select a country (Optional)",countries)
    #country = st.sidebar.text_input("What country are you looking for a scholarship in? (Optional)")
    country = country.lower()

    find_scholarships_button = st.sidebar.button("Find Scholarships", on_click=callback)
    
    contact_information()

    return user_specialization, level, find_scholarships_button,country


def SSA(user_specialization, level, find_scholarships_button,country):
    st.title('📝 Results')
    # Initialize variables
    specializations = []
    recommended_scholarships = pd.DataFrame()  # Initialize an empty DataFrame

    if find_scholarships_button:
        scholarship_df = pd.read_csv('scholarship_df.csv')

        # Convert the 'Area of Specialization' column in the DataFrame to lowercase for case-insensitive matching
        scholarship_df['Area of specialisation'] = scholarship_df['Area of specialisation'].str.lower()

        # Filter scholarships based on the chosen level and country
        #filtered_scholarships = scholarship_df[(scholarship_df['Level needed'].str.lower() == level) & (scholarship_df['Country'].str.lower() == country.lower())]
        # Filter scholarships based on the chosen level
        filtered_scholarships = scholarship_df[scholarship_df['Level needed'].str.lower() == level]

     # Optionally filter scholarships based on the country
        if country and country != '':
            filtered_scholarships = filtered_scholarships[filtered_scholarships['Country'].str.lower() == country.lower()]

        
        # Update the list of specializations
        specializations = filtered_scholarships['Area of specialisation'].unique().tolist()

        # Initialize a dictionary to store similarity scores
        similarity_scores = {}

        # Calculate similarity scores between the user's input and specializations
        for spec in specializations:
            similarity_score = fuzz.partial_ratio(user_specialization, spec.lower())
            similarity_scores[spec] = similarity_score

        # Sort specializations by similarity score in descending order
        sorted_specializations = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

        # Extract matched specializations with a similarity score threshold (e.g., 80)
        threshold = 80  # Adjust as needed
        matched_specializations = [spec for spec, score in sorted_specializations if score >= threshold]

        # Filter scholarships based on matched specializations
        recommended_scholarships = filtered_scholarships[filtered_scholarships['Area of specialisation'].isin(matched_specializations)]

        # Remove duplicate scholarships based on their names
        recommended_scholarships = recommended_scholarships.drop_duplicates(subset=['Name'])

    # Display the first 10 scholarships only if find_scholarships_button is True
   
    num_scholarships = len(recommended_scholarships)

    if num_scholarships > 0:
        st.write(f"I have {num_scholarships} suggestions for you in {user_specialization} for {level} opportunities.\n Here are the scholarships/universities to start your search:\n ")
            
        for i, (index, scholarship) in enumerate(recommended_scholarships.head(10).iterrows(), start=1):
            st.write(f" {i}.{scholarship['Name']}")
                
        # Display "Read More" button if there are more than 10 scholarships
        if num_scholarships > 10:
            with st.expander("View More") :
            #read_more_button = st.button("Read More")
            
            #if read_more_button:
                    # Display the rest of the scholarships
                for i, (index, scholarship) in enumerate(recommended_scholarships.iloc[10:].iterrows(), start=11):
                    st.write(f"{i}. {scholarship['Name']}")
    else:
        st.write(f"There is currently no scholarships in {user_specialization} for {level.upper()} at this moment in the database. Try a closely related field or type *All disciplines* for your field of interest.")


    
def contact_information():
    st.sidebar.header("Contact Information")
    st.sidebar.write("Contact me and let's be friends:")
    st.sidebar.write("- Youtube: [@BarbaraAboagye](https://www.youtube.com/channel/UCEYKFq7ZEg81GYxpzNqYZ4Q)")
    st.sidebar.write("- Instagram:[@asantewaa_aboagye](https://www.instagram.com/asantewaa_aboagye)")
    st.sidebar.write("- Twitter: [@awesome_ama](https://twitter.com/@awesome_ama)")
    st.sidebar.write("- Email:[Barbara](mailto:barbaraaboagye2@gmail.com)")

def buy_me_coffee_button():
    st.sidebar.write("This database was prepared by Barbara Aboagye.")
    st.sidebar.write("### Support Barbara")

    # Custom "Buy Me a Coffee" button with HTML and CSS
    st.sidebar.markdown("""
        <style>
            .bmc-button img {
                width: 150px !important;
                margin-bottom: 40px !important;
                box-shadow: none !important;
                border: none !important;
                vertical-align: middle !important;
            }
        </style>
        <a href="https://www.buymeacoffee.com/amas" target="_blank" class="bmc-button">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee">
        </a>
    """, unsafe_allow_html=True)

        





def video():
    st.title("📹 Useful Videos for Graduate School Application ")

    # Example 1: Embedding a video from a URL
    st.header("Writing an award winning CV and Statement of purpose")
    video_url_1 = "https://youtu.be/1UMizceVMuA?si=6y7IsBx2FgjL3SX9"
    video_url_2 = "https://www.youtube.com/watch?v=eNptCxlr3tk&list=PLebQgfnH5Iquqx3H2Y3WZS7qi9zgcPq-Q"
    video_url_3 = "https://youtu.be/NmhnIoYK_8Y?si=pwF9E5OM_4ZVbN8j"
    video_url_4 = 'https://youtu.be/4lJZ6vyDaKI?si=unq0AwZ13fGvVZxH'

    # Using columns to display videos side by side
    col1, col2 = st.columns(2)

    with col1:
        st.video(video_url_1)

    with col2:
        st.video(video_url_2)
        
        
    st.header("Writing a cold email and preparing for a graduate school interview")
    col3, col4 = st.columns(2)
    
    with col3:
        st.video(video_url_3)
        
    with col4:
        st.video(video_url_4)

#if __name__ == "__main__":
         #input_parameters()
         #video()

front_page = front_page()
user_specialization,level,find_scholarships_button,country = input_parameters()
#df2 = SSA(user_specialization,level,find_scholarships_button,country)
if find_scholarships_button:
    df2 = SSA(user_specialization, level, find_scholarships_button,country)
else:
    df2 = pd.DataFrame()  # Initialize an empty DataFrame
#contact = contact_information()


st.write ("""  # 🔍 What do you do next with this information? 
          """)

st.write ("""  
          - Copy the name of the university or scholarship, paste into Google, add the name of your area of field of interest and the link will pop up.
            - Example : Google "University of Toronto scholarship Planning" to obtain the link and requirements or 
            -  Google : University of Toronto Planning Graduate
        - Read the admission requirements, gather the documents, cold email, pay application fee if neccessary and apply
          """)

vid = video()
support = buy_me_coffee_button()








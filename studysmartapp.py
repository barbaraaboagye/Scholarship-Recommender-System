import pandas as pd
import numpy as np
import streamlit as st
from fuzzywuzzy import fuzz





st.sidebar.header("User input details") 


def front_page():
   
    st.title("Welcome to the School and Scholarship Search App (3SA)!")
    st.write('Find schools and sholarships in your field of study in 5 secs')
    st.write("To find scholarships, please follow these steps:")
    st.write("1. Enter the field you are looking for a scholarship in.")
    st.write("2. Select the level of scholarship you are interested in (e.g., BSc, MSc, PhD).")
    st.write("3. Click the 'Find Scholarships' button to see the recommendations.")
    st.write("Discover opportunities and share with friends!")

def callback():
    st.session_state.find_scholarships_button = True
    
    
def input_parameters():
    # Use st.sidebar.text_input and st.sidebar.selectbox with the default values
    field = st.sidebar.text_input("What field are you looking for a scholarship in?")
    user_specialization = field.lower()

    level = st.sidebar.selectbox("What level?", (' ', 'Diploma', 'BSc', 'MSc', 'MBA', 'LLM', 'MPH', 'MA', 'MFA', 'MPHIL', 'PhD', 'Post doc'))
    level = level.lower()

    find_scholarships_button = st.sidebar.button("Find Scholarships", on_click=callback)

   contact_information()

    return user_specialization, level, find_scholarships_button


def SSA(user_specialization, level, find_scholarships_button):
    st.title('Results')
    # Initialize variables
    specializations = []
    recommended_scholarships = pd.DataFrame()  # Initialize an empty DataFrame

    if find_scholarships_button:
        scholarship_df = pd.read_csv('scholarship_df.csv')

        # Convert the 'Area of Specialization' column in the DataFrame to lowercase for case-insensitive matching
        scholarship_df['Area of specialisation'] = scholarship_df['Area of specialisation'].str.lower()

        # Filter scholarships based on the chosen level
        filtered_scholarships = scholarship_df[scholarship_df['Level needed'].str.lower() == level]

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
    if find_scholarships_button:
        num_scholarships = len(recommended_scholarships)

        if num_scholarships > 0:
            st.write(f"I have {num_scholarships} suggestions for you in {user_specialization} for {level} opportunities.\n Here are the scholarships/universities to start your search:\n ")
            
            for i, (index, scholarship) in enumerate(recommended_scholarships.head(10).iterrows(), start=1):
                st.write(f" {i}.{scholarship['Name']}")
                
            # Display "Read More" button if there are more than 10 scholarships
            if num_scholarships > 10:
                read_more_button = st.button("Read More")
                if read_more_button:
                    # Display the rest of the scholarships
                    for i, (index, scholarship) in enumerate(recommended_scholarships.iloc[10:].iterrows(), start=11):
                        st.write(f"{i}. {scholarship['Name']}")
        else:
            st.write(f"There is currently no scholarships in {user_specialization} for {level.upper()} at this moment in the database. Try a closely related field or type *All disciplines* for your field of interest.")


    
def contact_information():
    st.sidebar.header("Contact Information")
    st.sidebar.write("This database was prepared by Barbara Aboagye.")
    st.sidebar.write("Contact me and let's be friends:")
    
    st.sidebar.write("- Youtube: [@BarbaraAboagye](https://www.youtube.com/channel/UCEYKFq7ZEg81GYxpzNqYZ4Q)")
    st.sidebar.write("- Instagram: [@asantewaa_aboagye](https://www.instagram.com/asantewaa_aboagye)")
    st.sidebar.write("- Twitter: [@awesome_ama](https://twitter.com/@awesome_ama)")
    st.sidebar.write("- Email:[Barbara](barbaraaboagye2@gmail.com)")


def video():
    st.title("Useful Videos for Graduate School Application ")

    # Example 1: Embedding a video from a URL
    st.header("Writing an award winning CV and Statement of purpose")
    video_url_1 = "https://youtu.be/1UMizceVMuA?si=6y7IsBx2FgjL3SX9"
    video_url_2 = "https://www.youtube.com/watch?v=eNptCxlr3tk&list=PLebQgfnH5Iquqx3H2Y3WZS7qi9zgcPq-Q"

    # Using columns to display videos side by side
    col1, col2 = st.columns(2)

    with col1:
        st.video(video_url_1)

    with col2:
        st.video(video_url_2)

#if __name__ == "__main__":
         #input_parameters()
         #video()

front_page = front_page()
user_specialization,level,find_scholarships_button = input_parameters()
df2 = SSA(user_specialization,level,find_scholarships_button)
#contact = contact_information()


st.write ("""  # What do you do next with this information? 
          """)

st.write ("""  
          - Copy the name of the university or scholarship, paste into Google, add the name of your area of field of interest and the link will pop up.
            - Example : Google "University of Toronto scholarship Planning" to obtain the link and requirements or 
            -  Google : University of Toronto Planning Graduate
        - Read the admission requirements, gather the documents, cold email, pay application fee if neccessary and apply
          """)

vid = video()

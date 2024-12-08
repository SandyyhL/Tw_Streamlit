import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter


st.title("Visual Analysis")
st.write("In this page, we will walk through visual analysis of tradwife videos. I first used **Pyktok** package to download all the videos fo the selected account as MP4 and saved them locally.")
st.write("With these MP4 files, we can conduct visual analysis with Google Vision API. However, before this step, we need to ensure we captures " +
         "representative frames of the videos.")

st.subheader("Subtracting Frames 🖼️")

st.write("Step 1: Use Google Video API to detect frame changes. See the blow code reference:")
code_snippet = """
from google.cloud import videointelligence // To use Google API, you need to set up in advance. Visit Google API website to learn how to set up.

def detect_shot_changes(video_path):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SHOT_CHANGE_DETECTION]

    with io.open(video_path, "rb") as movie:
        input_content = movie.read()

    operation = video_client.annotate_video(
        request={"features": features, "input_content": input_content}
    )
    print("\\nProcessing video for shot change annotations:")

    result = operation.result(timeout=90)
    print("\\nFinished processing.")

    # first result is retrieved because a single video was processed
    shot_changes = []
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = shot.start_time_offset.total_seconds()
        end_time = shot.end_time_offset.total_seconds()
        shot_changes.append((start_time, end_time))
        print("\\tShot {}: {} to {}".format(i, start_time, end_time))
    
    return shot_changes
"""
st.code(code_snippet, language="python")

st.write("")
st.write("Step 2: Extract frames from the detected shots. Here, I extract frames from the mid point of every shot.")

code_snippet = """
import cv2

def extract_frames(video_path, timestamps, output_folder):
    ""
    Extracts frames from a video at specified timestamps and saves them with filenames based on the timestamp.

    Parameters:
    - video_path (str): The path to the input video file.
    - timestamps (List[Tuple[float, float]]): A list of (start, end) tuples in seconds.
    - output_folder (str): The folder to save the extracted frames.

    Saves:
    - .jpg files named according to their exact timestamp.
    ""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    video_id = os.path.splitext(os.path.basename(video_path))[0].split('_')[-1]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, (start, end) in enumerate(timestamps):
        # Calculate the middle frame time between the start and end timestamp
        frame_time = (start + end) / 2  
        
        # Set the position of the video capture to the specified time
        cap.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)
        ret, frame = cap.read()
        
        if ret:
            # Create a filename based on the timestamp
            frame_filename = f"{video_id}_{frame_time:.2f}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)
            
            # Save the frame as a .jpg file
            cv2.imwrite(frame_path, frame)
            print(f"Saved frame at {frame_path}")
    
    # Release the video capture object
    cap.release()
"""

st.code(code_snippet, language="python")

st.subheader("Testing Frame Extraction 🧪")

st.write("With these function, we can now test run it on some of our videos!")
st.write("For the purpose of this research, I wrote a helper function and a Main() to execute the collection and organize the frame files.")

code_snippet = """
def get_all_mp4_files_in_subfolders(parent_folder):
    # Dictionary to store folder paths and their mp4 files
    folder_mp4_files = []

    for root, dirs, files in os.walk(parent_folder):
        # Filter only mp4 files in the current folder
        mp4_files = [os.path.join(root, file) for file in files if file.endswith('.mp4')]
        
        if mp4_files:  # Add the folder and its mp4 files to the dictionary
            #folder_mp4_files[root] = mp4_files
            folder_mp4_files = mp4_files

    return folder_mp4_files


## Main

main_folder = "/Users/sandyliu/Desktop/pyktok_video_data" // Change to your directory

folders = next(os.walk(main_folder))[1]
all_folders = [os.path.join(main_folder, folder) for folder in folders]


for folder in all_folders:
    #create a new folder for the extracted frames
    user = folder.split("/")[-1]
    frame_saving_path = f"/Users/sandyliu/Desktop/pyktok_video_frames_data/{user}"

    if user == "jennifer__tate__":
        continue

    all_mp4_urls = get_all_mp4_files_in_subfolders(folder)

    for mp4_url in all_mp4_urls:
        print(mp4_url)
        shot_changes = detect_shot_changes(mp4_url)
        extract_frames(mp4_url, shot_changes, frame_saving_path)
    
    print(f"Finished: {user}")"""

st.code(code_snippet, language="python")

st.subheader("Analysis 📈")

st.write("With these code files, we can now conduct some analysis by using Google Vision API, which analyzes a picture and provides keywords associated, color scheme analysis and more.")
st.write("To use Google Vision API, you can use the code snippet below.")

code_snippet="""

def detect_labels(path):
    "Detects labels in the file."
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print("Labels:")

    result = []
    for label in labels:
        print(label.description)
        result.append((label.description, label.score))

    if response.error.message:
        raise Exception(
            "For more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return result
"""

st.code(code_snippet, language="python")

df = pd.read_csv("/Users/sandyliu/Thesis/Streamlit/label_counts.csv")

# Display data
st.title("Ranked Bar Chart of Popular Hashtags from Frame Labels")
st.write("### Data Preview")
st.dataframe(df)

# Visualize data as a ranked bar chart
st.write("### Ranked Bar Chart")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df["Label"].head(10), df["Count"].head(10), color="skyblue")
ax.set_title("Top 10 Labels from Frames (Ranked)")
ax.set_xlabel("Labels")
ax.set_ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)
import streamlit as st
from utils import *

def get_highest_priority(strings):
    def priority_score(s):
        score = 0
        if 'orig' in s:
            score += 4  # 2^2
        if s.startswith('en'):
            score += 2  # 2^1
        if s == 'en':
            score += 1  # 2^0
        return score

    if not strings:
        return None

    return max(strings, key=priority_score)

# ----------------------------------
with st.sidebar:
    method = st.selectbox(label="Summarizing method", options=summarizing_prompts.keys())

# ----------------------------------
video_url = st.text_input(label="Link",placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


if video_url != "":
    # Getting Youtube Info
    info = get_video_info(video_url)

    # Selecting best lang
    subs = {}
    for l in info['subtitles'].keys():
        if l.startswith('en') or l.startswith('es'):
            for sub in info['subtitles'][l]:
                if sub['ext'] == 'vtt':
                    subs[l] = sub
    lang = get_highest_priority(subs.keys())


    # Showing video info
    st.write(f"### {info['title']}")
    st.write(f"**Duration:** {seconds_to_time(info['duration'])} **Views:** {numeric_to_human(info['views'])}")
    st.image(info['thumbnail'])

    # Preparing prompt
    prompt = prepare_prompt(method=method)


    # Writing syntesized text.
    st.write("---")
    st.write(syn := summarize(prompt, text := get_subs(subs[lang])))

    # Preparing download bottons.
    st.write("---")
    c1,c2,c3 = st.columns(3)
    c1.download_button(label="Raw",data=text,file_name=f"{info['title']}.txt",use_container_width=True)
    c2.download_button(label="PDF",data='',file_name=f"{info['title']}.pdf",use_container_width=True)
    c3.download_button(label="Text",data=syn,file_name=f"{info['title']}.md",use_container_width=True)
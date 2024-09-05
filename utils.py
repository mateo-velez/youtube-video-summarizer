from typing import List
import yt_dlp
import requests
import streamlit as st
from openai import OpenAI
import m3u8


@st.cache_data(persist=True)
def get_video_info(url):
    """
    Returns a dictionary with the image thumbnail in binary, the title, duration, views, and available subtitles of a video.
    
    Args:
    url (str): The URL of the video.
    
    Returns:
    dict: A dictionary containing video information with keys:
        - 'thumbnail': Binary data of the thumbnail image
        - 'title': String title of the video
        - 'duration': Float duration of the video in seconds
        - 'views': Integer number of views
        - 'subtitles': Dictionary of available subtitles, where keys are language codes and values are lists of subtitle formats
    """
    ydl_opts = {
        'writesubtitles': True,
        'allsubtitles': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
    thumbnail_url = info['thumbnail']
    thumbnail_binary = requests.get(thumbnail_url).content
    
    # Extract subtitle information
    subtitles = info.get('subtitles', {})
    # Some platforms use 'automatic_captions' for auto-generated subtitles
    automatic_captions = info.get('automatic_captions', {})
    
    # Merge both types of subtitles
    all_subtitles = {**subtitles, **automatic_captions}
    return {
        'thumbnail': thumbnail_binary,
        'title': info['title'],
        'duration': info['duration'],
        'views': info['view_count'],
        'subtitles': all_subtitles
    }


    
@st.cache_data(persist=True)
def get_subs(sub_metadata:dict) -> str:
    def process_vtt(vtt: List[str]) -> str:
        lines = vtt
        result = []
        seen = set()
        is_textual = False
        for line in lines:
            if '-->' in line:
                is_textual = True
            elif is_textual:
                s = line.strip()
                if s not in seen:
                    result.append(s)
                    seen.add(s)

                is_textual = False

        return ' '.join(result)

    def download_m3u8_subs(url):
        try:
            # Download the m3u8 file
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the m3u8 content
            playlist = m3u8.loads(response.text)
            
            # Find the subtitle segments
            subtitle_segments = [segment for segment in playlist.segments if segment.uri.endswith('.vtt')]
            
            if not subtitle_segments:
                return "No VTT subtitles found in the m3u8 file."
            
            # Download and concatenate all VTT segments
            vtt_content = ""
            for segment in subtitle_segments:
                segment_url = playlist.base_uri + segment.uri if playlist.base_uri else segment.uri
                segment_response = requests.get(segment_url)
                segment_response.raise_for_status()
                vtt_content += segment_response.text + "\n"
            
            return vtt_content.strip()
        
        except requests.RequestException as e:
            return f"Error downloading subtitles: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    url = sub_metadata['url']
    if sub_metadata.get('protocol') and sub_metadata['protocol'].startswith('m3u8'):
        text = download_m3u8_subs(url)
    elif not sub_metadata.get('protocol'):
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
    else:
        raise ValueError(sub_metadata)
    

    return process_vtt(text.split('\n'))



@st.cache_data(persist=True)
def synthesize(prompt:str, text:str):
    with OpenAI() as client:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=4096
        )
    
    return completion.choices[0].message.content


synthesizing_prompts = {
    "Summary":"Please provide a concise summary of the given text, capturing its main ideas and key arguments. Your summary should be approximately 20% of the original text's length. Focus on the central theme, primary arguments, and significant conclusions. Avoid including minor details or examples unless they are crucial to understanding the main points. Ensure that your summary gives a clear overview of the text's content and purpose.",
    "Key points":"Extract and list the most important points from the given text. Identify crucial facts, central concepts, and pivotal arguments. Present each key point as a brief, clear statement. Aim for 5-7 key points, depending on the text's length and complexity. Include any critical data, statistics, or findings that are fundamental to the text's message. Ensure that someone reading only these key points would grasp the essential information conveyed in the full text.",
    "Q&A":"""Based on the given text, generate a set of 5-7 important questions that cover the main topics and ideas presented. Then, provide concise yet comprehensive answers to each question using information directly from the text. Ensure that the questions and answers together cover the text's key concepts, arguments, and conclusions.

Make sure the questions are diverse and cover different aspects of the text, and that the answers are accurate and informative.

Format your response as:
## [Question]
[Answer]

## [Question]
[Answer]""",
    "Paraphrasing":"""Please rewrite the given text in your own words, maintaining its original meaning and key ideas. Your paraphrased version should:
- Be approximately the same length as the original text
- Use different vocabulary and sentence structures where possible
- Clarify any complex concepts or jargon
- Maintain the original tone and intent of the text
- Ensure all key information and arguments are preserved
- Be easily understandable to a general audience

The goal is to create a version that enhances clarity and comprehension while faithfully representing the original content."""
}

def prepare_prompt(method:str):
    return synthesizing_prompts[method] + "\n\n\Write your output in ENGLISH independent of the input lang."




def numeric_to_human(n:int) -> str:
    assert n >= 0 and n < 10**12, "Value Out of Bounds"
    if n < 10**3:
        return str(n)
    elif n < 10**6:
        return f"{n//10**3}K"
    else:
        return f"{n//10**6}M"
    
def seconds_to_time(n:int) -> str:
    assert n >= 0 and n < 3_600_00, "Value out of bounds"
    if n < 3600:
        return f"{n//60}:{n%60}"
    else:
        return f"{n//3600}:{(n%3600)//60}:{n%60}"
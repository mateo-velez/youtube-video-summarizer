- add more options to the youtube extract captions
    - pdf download button
    - markdwon download button
    - language cations
    - prompt options: summary or rewriting, captions, structure, etc
    - maybe LLM model
    - 

- add informative actions before and after extraction/formating:
    - video info: title, duration, thumbnail, subs available.
    - aproximate cost
    - length subs
    - add actual LLM call cost in tokens and dollars.

- add option to download a list of urls or even a playlist
- allow for url parameter to be passed



Here are specific and detailed prompts for each synthesizing method:

1. **Summary**:
"Please provide a concise summary of the given text, capturing its main ideas and key arguments. Your summary should be approximately 20% of the original text's length. Focus on the central theme, primary arguments, and significant conclusions. Avoid including minor details or examples unless they are crucial to understanding the main points. Ensure that your summary gives a clear overview of the text's content and purpose."

2. **Key Points**:
"Extract and list the most important points from the given text. Identify crucial facts, central concepts, and pivotal arguments. Present each key point as a brief, clear statement. Aim for 5-7 key points, depending on the text's length and complexity. Include any critical data, statistics, or findings that are fundamental to the text's message. Ensure that someone reading only these key points would grasp the essential information conveyed in the full text."

3. **QA (Question and Answer)**:
"Based on the given text, generate a set of 5-7 important questions that cover the main topics and ideas presented. Then, provide concise yet comprehensive answers to each question using information directly from the text. Ensure that the questions and answers together cover the text's key concepts, arguments, and conclusions. Format your response as:

Q1: [Question]
A1: [Answer]

Q2: [Question]
A2: [Answer]

... and so on.

Make sure the questions are diverse and cover different aspects of the text, and that the answers are accurate and informative."

4. **Paraphrasing**:
"Please rewrite the given text in your own words, maintaining its original meaning and key ideas. Your paraphrased version should:
- Be approximately the same length as the original text
- Use different vocabulary and sentence structures where possible
- Clarify any complex concepts or jargon
- Maintain the original tone and intent of the text
- Ensure all key information and arguments are preserved
- Be easily understandable to a general audience

The goal is to create a version that enhances clarity and comprehension while faithfully representing the original content."


---
- main goal is to make the content of the video understandable. Presented in a textual way. So there are two parts:
    - the way it syntentizes the content
        - key point extraction
        - 
    - the way it presents it.
        - language es/en
        - structured
        - 
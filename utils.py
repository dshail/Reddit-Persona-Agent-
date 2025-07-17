import os
import re
from typing import List, Dict
from datetime import datetime


def clean_text(text: str) -> str:
    """
    Clean and normalize the text for LLM input.
    Removes extra spaces, newlines, and markdown artifacts.
    """
    if not text:
        return ""
    # Remove markdown links and formatting
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(texts: List[str], chunk_size: int = 3000) -> List[str]:
    """
    Chunk list of texts into manageable chunks based on character length.
    Useful for feeding into LLMs with token limits.
    """
    chunks = []
    current_chunk = ""

    for text in texts:
        if len(current_chunk) + len(text) < chunk_size:
            current_chunk += "\n\n" + text
        else:
            chunks.append(current_chunk.strip())
            current_chunk = text
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def format_citations(posts: List[Dict[str, str]]) -> str:
    """
    Formats a list of post/comment dictionaries into a citation block.
    """
    citations = []
    for post in posts:
        content = clean_text(post['text'])[:150] + "..." if len(post['text']) > 150 else clean_text(post['text'])
        citations.append(f"- \"{content}\" ([source]({post['permalink']}))")
    return "\n".join(citations)


def save_persona_to_file(username: str, persona_text: str) -> str:
    """
    Saves the generated user persona to a .txt file.
    """
    safe_username = username.replace("/", "_")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{safe_username}_persona.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(persona_text)
    return file_path

def generate_persona_pdf(username: str, persona_text: str) -> bytes:
    """
    Generates a PDF version of the user persona and returns it as bytes.
    """
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from io import BytesIO
    
    # Create a BytesIO buffer to hold the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor='#2E86AB'
    )
    
    # Build the story (content)
    story = []
    
    # Add title
    story.append(Paragraph(f"Reddit User Persona: {username}", title_style))
    story.append(Spacer(1, 12))
    
    # Add timestamp
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    story.append(Paragraph(f"Generated on: {timestamp}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Process the persona text
    lines = persona_text.split('\n')
    for line in lines:
        if line.strip():
            if line.startswith('###'):
                # Main heading
                story.append(Paragraph(line.replace('###', '').strip(), styles['Heading1']))
                story.append(Spacer(1, 12))
            elif line.startswith('**') and line.endswith('**'):
                # Bold text (section headers)
                clean_line = line.replace('**', '').strip()
                story.append(Paragraph(clean_line, styles['Heading2']))
                story.append(Spacer(1, 6))
            elif line.strip().startswith('-'):
                # Bullet points
                story.append(Paragraph(line.strip(), styles['Normal']))
                story.append(Spacer(1, 3))
            else:
                # Regular text
                story.append(Paragraph(line.strip(), styles['Normal']))
                story.append(Spacer(1, 6))
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def save_output_to_file(text: str, username: str) -> str:
    """
    Saves the generated user persona to a .txt file with timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_username = username.replace("/", "_")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{safe_username}_persona_{timestamp}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path

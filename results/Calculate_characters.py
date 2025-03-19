import re
from pathlib import Path

def count_words_in_md(file_path):
    """
    Count words in an English Markdown file
    
    Returns:
        dict: Statistics including total words, sections, headings, etc.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store original content for heading analysis
        original_content = content
        
        # Remove code blocks
        content_without_code = re.sub(r'```[\s\S]*?```', '', content)
        
        # Remove inline code
        content_without_code = re.sub(r'`[^`]*`', '', content_without_code)
        
        # Remove URLs and references
        content_without_code = re.sub(r'http[s]?://\S+', '', content_without_code)
        content_without_code = re.sub(r'\[\d+\]', '', content_without_code)
        
        # Count headings
        headings = re.findall(r'^#{1,6}\s.+$', original_content, re.MULTILINE)
        heading_count = len(headings)
        
        # Count sections (based on ## level headings)
        sections = re.findall(r'^##\s.+$', original_content, re.MULTILINE)
        section_count = len(sections)
        
        # Count words
        words = re.findall(r'\b\w+\b', content_without_code)
        word_count = len(words)
        
        # Count characters (excluding spaces and punctuation)
        char_count = len(re.findall(r'[A-Za-z0-9]', content_without_code))
        
        # Count sentences (roughly)
        sentences = re.split(r'[.!?]+', content_without_code)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Count references
        references = re.findall(r'\[\d+\]', original_content)
        reference_count = len(set(references))  # Count unique references
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'sentence_count': sentence_count,
            'heading_count': heading_count,
            'section_count': section_count,
            'reference_count': reference_count,
            'average_words_per_sentence': round(word_count/sentence_count, 2) if sentence_count > 0 else 0
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

def main():
    file_path = "/home/lzq/results/alphafold3_example/reference_answer.md"  # 文件名
    
    stats = count_words_in_md(file_path)
    if stats:
        print("\n=== Document Statistics ===")
        print(f"Total words: {stats['word_count']}")
        print(f"Total characters: {stats['char_count']}")
        print(f"Total sentences: {stats['sentence_count']}")
        print(f"Total headings: {stats['heading_count']}")
        print(f"Major sections: {stats['section_count']}")
        print(f"Unique references: {stats['reference_count']}")
        print(f"Average words per sentence: {stats['average_words_per_sentence']}")

if __name__ == "__main__":
    main()
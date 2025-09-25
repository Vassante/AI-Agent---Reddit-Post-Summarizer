import re
from typing import List, Dict
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextSummarizer:
    """
    Text summarization using extractive methods (no API keys required)
    """
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess text
        """
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # Remove special characters and extra whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        Extract keywords from text using TF-IDF-like approach
        """
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize and filter
        words = word_tokenize(cleaned_text.lower())
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        # Count word frequencies
        word_freq = Counter(words)
        
        # Return top keywords
        return [word for word, freq in word_freq.most_common(num_keywords)]
    
    def calculate_sentence_scores(self, sentences: List[str], keywords: List[str]) -> Dict[str, float]:
        """
        Calculate scores for sentences based on keyword frequency
        """
        sentence_scores = {}
        
        for sentence in sentences:
            sentence_words = word_tokenize(sentence.lower())
            sentence_words = [word for word in sentence_words if word not in self.stop_words]
            
            score = 0
            for word in sentence_words:
                if word in keywords:
                    score += 1
            
            if len(sentence_words) > 0:
                sentence_scores[sentence] = score / len(sentence_words)
            else:
                sentence_scores[sentence] = 0
                
        return sentence_scores
    
    def summarize_text(self, text: str, num_sentences: int = 3, max_words: int = None, max_paragraphs: int = None) -> str:
        """
        Summarize text using extractive summarization with word/paragraph limits
        """
        if not text or len(text.strip()) < 50:
            return text
        
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Split into sentences with fallback
        try:
            sentences = sent_tokenize(cleaned_text)
        except:
            # Fallback: simple sentence splitting
            sentences = re.split(r'[.!?]+', cleaned_text)
            sentences = [s.strip() for s in sentences if s.strip()]
        
        # If still only 1 sentence, try more aggressive splitting
        if len(sentences) <= 1:
            # Split by common sentence endings and newlines
            sentences = re.split(r'[.!?]+\s+|\n+', cleaned_text)
            sentences = [s.strip() for s in sentences if s.strip() and len(s) > 10]
        
        # If we have a word limit, we should apply it even with few sentences
        if len(sentences) <= num_sentences and not max_words and not max_paragraphs:
            return text
        
        # If we have a word limit but poor sentence splitting, apply direct word limit
        if max_words and len(sentences) <= 2:
            words = cleaned_text.split()
            if len(words) > max_words:
                limited_words = words[:max_words]
                return ' '.join(limited_words)
            else:
                return cleaned_text
        
        # Extract keywords
        keywords = self.extract_keywords(cleaned_text)
        
        # Calculate sentence scores
        sentence_scores = self.calculate_sentence_scores(sentences, keywords)
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Apply word limit if specified
        if max_words:
            selected_sentences = []
            word_count = 0
            for sentence, score in top_sentences:
                sentence_words = len(sentence.split())
                if word_count + sentence_words <= max_words:
                    selected_sentences.append((sentence, score))
                    word_count += sentence_words
                else:
                    break
            top_sentences = selected_sentences
        
        # Apply paragraph limit if specified
        elif max_paragraphs:
            # Group sentences into paragraphs (roughly 3-4 sentences per paragraph)
            sentences_per_paragraph = max(1, len(sentences) // max_paragraphs)
            top_sentences = top_sentences[:max_paragraphs * sentences_per_paragraph]
        
        # Otherwise use sentence limit
        else:
            top_sentences = top_sentences[:num_sentences]
        
        # Sort by original order
        top_sentences.sort(key=lambda x: sentences.index(x[0]))
        
        # Create final summary
        final_summary = ' '.join([sentence for sentence, score in top_sentences])
        
        return final_summary
    
    def summarize_reddit_posts(self, posts: List[Dict], query: str = None, max_words: int = None, max_paragraphs: int = None) -> Dict:
        """
        Summarize multiple Reddit posts with customizable length
        """
        if not posts:
            return {
                'summary': 'No posts found to summarize.',
                'key_points': [],
                'total_posts': 0,
                'query': query
            }
        
        # Combine all text content
        all_text = ""
        post_summaries = []
        
        for post in posts:
            post_text = f"{post.get('title', '')} {post.get('content', '')}"
            if post_text.strip():
                all_text += post_text + " "
                # Create individual post summary
                post_summary = {
                    'title': post.get('title', '')[:100] + '...' if len(post.get('title', '')) > 100 else post.get('title', ''),
                    'summary': self.summarize_text(post_text, num_sentences=2, max_words=max_words//len(posts) if max_words else None),
                    'score': post.get('score', 0),
                    'subreddit': post.get('subreddit', 'unknown'),
                    'url': post.get('permalink', '')
                }
                post_summaries.append(post_summary)
        
        # Create overall summary with user-specified length
        if max_words:
            overall_summary = self.summarize_text(all_text, max_words=max_words)
        elif max_paragraphs:
            overall_summary = self.summarize_text(all_text, max_paragraphs=max_paragraphs)
        else:
            overall_summary = self.summarize_text(all_text, num_sentences=5)
        
        # Extract key points
        key_points = self.extract_keywords(all_text, num_keywords=15)
        
        return {
            'summary': overall_summary,
            'key_points': key_points,
            'post_summaries': post_summaries,
            'total_posts': len(posts),
            'query': query,
            'summary_length': {
                'words': len(overall_summary.split()),
                'paragraphs': len(overall_summary.split('\n\n')) if '\n\n' in overall_summary else 1
            }
        }

class SimpleSummarizer:
    """
    Simple summarizer for when NLTK is not available
    """
    
    def summarize_text(self, text: str, num_sentences: int = 3, max_words: int = None, max_paragraphs: int = None) -> str:
        """
        Simple extractive summarization with word/paragraph limits
        """
        if not text or len(text.strip()) < 50:
            return text
        
        # Split by sentences (simple approach)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= num_sentences:
            return text
        
        # Simple scoring based on word count and position
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = len(sentence.split())  # Word count
            if i == 0:  # First sentence bonus
                score *= 1.5
            sentence_scores.append((sentence, score))
        
        # Sort by score
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Apply word limit if specified
        if max_words:
            print(f"SimpleSummarizer Debug: Applying word limit of {max_words} to {len(sentence_scores)} sentences")
            selected_sentences = []
            word_count = 0
            for sentence, score in sentence_scores:
                sentence_words = len(sentence.split())
                if word_count + sentence_words <= max_words:
                    selected_sentences.append((sentence, score))
                    word_count += sentence_words
                else:
                    break
            sentence_scores = selected_sentences
            print(f"SimpleSummarizer Debug: Selected {len(sentence_scores)} sentences with {word_count} words")
        
        # Apply paragraph limit if specified
        elif max_paragraphs:
            sentences_per_paragraph = max(1, len(sentences) // max_paragraphs)
            sentence_scores = sentence_scores[:max_paragraphs * sentences_per_paragraph]
        
        # Otherwise use sentence limit
        else:
            sentence_scores = sentence_scores[:num_sentences]
        
        # Sort by original order
        sentence_scores.sort(key=lambda x: sentences.index(x[0]))
        
        return '. '.join([sentence for sentence, score in sentence_scores]) + '.'
    
    def summarize_reddit_posts(self, posts: List[Dict], query: str = None, max_words: int = None, max_paragraphs: int = None) -> Dict:
        """
        Summarize multiple Reddit posts using simple method with customizable length
        """
        if not posts:
            return {
                'summary': 'No posts found to summarize.',
                'key_points': [],
                'total_posts': 0,
                'query': query
            }
        
        # Combine all text content
        all_text = ""
        post_summaries = []
        
        for post in posts:
            post_text = f"{post.get('title', '')} {post.get('content', '')}"
            if post_text.strip():
                all_text += post_text + " "
                # Create individual post summary
                post_summary = {
                    'title': post.get('title', '')[:100] + '...' if len(post.get('title', '')) > 100 else post.get('title', ''),
                    'summary': self.summarize_text(post_text, num_sentences=2, max_words=max_words//len(posts) if max_words else None),
                    'score': post.get('score', 0),
                    'subreddit': post.get('subreddit', 'unknown'),
                    'url': post.get('permalink', '')
                }
                post_summaries.append(post_summary)
        
        # Create overall summary with user-specified length
        if max_words:
            overall_summary = self.summarize_text(all_text, max_words=max_words)
        elif max_paragraphs:
            overall_summary = self.summarize_text(all_text, max_paragraphs=max_paragraphs)
        else:
            overall_summary = self.summarize_text(all_text, num_sentences=5)
        
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_freq = Counter(words)
        # Filter out common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        key_points = [word for word, freq in word_freq.most_common(20) if word not in common_words and len(word) > 2][:15]
        
        return {
            'summary': overall_summary,
            'key_points': key_points,
            'post_summaries': post_summaries,
            'total_posts': len(posts),
            'query': query,
            'summary_length': {
                'words': len(overall_summary.split()),
                'paragraphs': len(overall_summary.split('\n\n')) if '\n\n' in overall_summary else 1
            }
        }

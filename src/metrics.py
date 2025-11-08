"""Email metrics and analytics."""

import re
from typing import Dict


class EmailMetrics:
    """Calculate metrics for generated emails."""

    @staticmethod
    def analyze_email(subject: str, body: str) -> Dict[str, any]:
        """
        Analyze email and return metrics.

        Args:
            subject: Email subject line
            body: Email body text

        Returns:
            Dictionary containing various metrics
        """
        # Clean body text (remove extra whitespace)
        clean_body = ' '.join(body.split())

        # Word count
        words = clean_body.split()
        word_count = len(words)

        # Character count (excluding spaces)
        char_count = len(clean_body.replace(' ', ''))
        char_count_with_spaces = len(clean_body)

        # Sentence count
        sentences = re.split(r'[.!?]+', clean_body)
        sentence_count = len([s for s in sentences if s.strip()])

        # Average words per sentence
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0

        # Subject line length
        subject_length = len(subject)
        subject_word_count = len(subject.split())

        # Readability score (simple version - lower is better/easier)
        # Based on average sentence length
        if avg_words_per_sentence <= 15:
            readability = "Excellent"
        elif avg_words_per_sentence <= 20:
            readability = "Good"
        elif avg_words_per_sentence <= 25:
            readability = "Fair"
        else:
            readability = "Complex"

        # Email length assessment
        if word_count <= 150:
            length_assessment = "Ideal"
        elif word_count <= 200:
            length_assessment = "Good"
        elif word_count <= 250:
            length_assessment = "Acceptable"
        else:
            length_assessment = "Too Long"

        return {
            'word_count': word_count,
            'character_count': char_count,
            'character_count_with_spaces': char_count_with_spaces,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'subject_length': subject_length,
            'subject_word_count': subject_word_count,
            'readability': readability,
            'length_assessment': length_assessment
        }

    @staticmethod
    def format_metrics(metrics: Dict[str, any]) -> str:
        """
        Format metrics for display.

        Args:
            metrics: Dictionary of metrics

        Returns:
            Formatted string
        """
        return f"""
Email Metrics:
--------------
Word Count: {metrics['word_count']} ({metrics['length_assessment']})
Character Count: {metrics['character_count']} (with spaces: {metrics['character_count_with_spaces']})
Sentences: {metrics['sentence_count']}
Avg Words/Sentence: {metrics['avg_words_per_sentence']}
Readability: {metrics['readability']}

Subject Line:
-------------
Length: {metrics['subject_length']} characters
Word Count: {metrics['subject_word_count']} words
"""

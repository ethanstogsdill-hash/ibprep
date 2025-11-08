"""Template management for email generation."""

import os
from typing import Dict, List, Tuple


class TemplateManager:
    """Manages email templates and variations."""

    TEMPLATE_DIR = "templates"

    TEMPLATE_TYPES = {
        "cold_outreach": "Initial Cold Outreach",
        "coffee_followup": "Coffee Chat Follow-up",
        "thank_you": "Post-Interview Thank You",
        "referral": "Referral-Based Introduction",
        "alumni": "Alumni Connection"
    }

    TONE_LEVELS = {
        "formal": "FORMAL",
        "warm": "WARM",
        "casual": "CASUAL"
    }

    def __init__(self):
        """Initialize template manager."""
        self.templates = {}
        self.load_templates()

    def load_templates(self):
        """Load all templates from the templates directory."""
        for template_type in self.TEMPLATE_TYPES.keys():
            template_path = os.path.join(self.TEMPLATE_DIR, f"{template_type}.txt")
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    self.templates[template_type] = self._parse_template(f.read())

    def _parse_template(self, content: str) -> Dict[str, any]:
        """Parse template file into subject lines and tone variations."""
        sections = {}
        current_section = None
        current_content = []

        for line in content.split('\n'):
            if line.strip() in ['SUBJECT_LINES:', 'FORMAL:', 'WARM:', 'CASUAL:']:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.strip().rstrip(':')
                current_content = []
            else:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        # Parse subject lines
        subject_lines = []
        if 'SUBJECT_LINES' in sections:
            subject_lines = [
                line.strip('- ').strip()
                for line in sections['SUBJECT_LINES'].split('\n')
                if line.strip().startswith('-')
            ]

        return {
            'subject_lines': subject_lines,
            'FORMAL': sections.get('FORMAL', ''),
            'WARM': sections.get('WARM', ''),
            'CASUAL': sections.get('CASUAL', '')
        }

    def get_template(self, template_type: str, tone: str = "warm") -> Tuple[List[str], str]:
        """
        Get template content for given type and tone.

        Args:
            template_type: Type of email template
            tone: Tone level (formal, warm, casual)

        Returns:
            Tuple of (subject_lines, body_template)
        """
        if template_type not in self.templates:
            raise ValueError(f"Template type '{template_type}' not found")

        tone_key = self.TONE_LEVELS.get(tone.lower(), "WARM")
        template = self.templates[template_type]

        return (
            template['subject_lines'],
            template.get(tone_key, template.get('WARM', ''))
        )

    def get_available_templates(self) -> Dict[str, str]:
        """Get dictionary of available templates."""
        return self.TEMPLATE_TYPES.copy()

    def get_available_tones(self) -> List[str]:
        """Get list of available tone levels."""
        return list(self.TONE_LEVELS.keys())

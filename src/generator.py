"""Core email generation logic."""

import random
from typing import Dict, List, Tuple
from .templates import TemplateManager
from .metrics import EmailMetrics


class EmailGenerator:
    """Generates personalized IB networking emails."""

    # Seniority level to tone mapping (default recommendations)
    SENIORITY_TONE_MAP = {
        "analyst": "casual",
        "associate": "warm",
        "vp": "warm",
        "vice president": "warm",
        "director": "formal",
        "md": "formal",
        "managing director": "formal"
    }

    def __init__(self):
        """Initialize email generator."""
        self.template_manager = TemplateManager()
        self.metrics_calculator = EmailMetrics()

    def generate_email(
        self,
        template_type: str,
        recipient_data: Dict[str, str],
        sender_data: Dict[str, str],
        tone: str = None,
        num_variations: int = 3
    ) -> List[Dict[str, any]]:
        """
        Generate personalized email(s).

        Args:
            template_type: Type of email template to use
            recipient_data: Information about the recipient
            sender_data: Information about the sender
            tone: Tone level (if None, will be auto-determined)
            num_variations: Number of variations to generate

        Returns:
            List of email dictionaries with variations
        """
        # Auto-determine tone if not provided
        if tone is None:
            tone = self._determine_tone(recipient_data)

        # Get template
        subject_lines, body_template = self.template_manager.get_template(
            template_type, tone
        )

        # Combine all data for template filling
        template_data = {**recipient_data, **sender_data}

        # Extract recipient's first name from full name
        if 'name' in recipient_data and 'first_name' not in template_data:
            template_data['first_name'] = recipient_data['name'].split()[0]

        # Generate variations
        emails = []
        num_subjects = min(num_variations, len(subject_lines))

        # Select subject lines (mix of sequential and random for variety)
        selected_subjects = subject_lines[:num_subjects]

        for i, subject_template in enumerate(selected_subjects):
            # Fill in template
            subject = self._fill_template(subject_template, template_data)
            body = self._fill_template(body_template, template_data)

            # Calculate metrics
            metrics = self.metrics_calculator.analyze_email(subject, body)

            emails.append({
                'variation': i + 1,
                'subject': subject,
                'body': body,
                'metrics': metrics,
                'tone': tone,
                'template_type': template_type
            })

        return emails

    def _determine_tone(self, recipient_data: Dict[str, str]) -> str:
        """
        Determine appropriate tone based on recipient data.

        Args:
            recipient_data: Information about recipient

        Returns:
            Tone level string
        """
        # Check relationship type first
        relationship = recipient_data.get('relationship', '').lower()
        if relationship == 'referral':
            return 'warm'
        elif relationship == 'alumni':
            return 'warm'
        elif relationship == 'cold':
            # Check seniority
            seniority = recipient_data.get('seniority', '').lower()
            return self.SENIORITY_TONE_MAP.get(seniority, 'warm')

        # Default to warm
        return 'warm'

    def _fill_template(self, template: str, data: Dict[str, str]) -> str:
        """
        Fill template with provided data.

        Args:
            template: Template string with {variable} placeholders
            data: Dictionary of values to fill in

        Returns:
            Filled template string
        """
        result = template

        # Replace all placeholders
        for key, value in data.items():
            placeholder = '{' + key + '}'
            if placeholder in result:
                result = result.replace(placeholder, str(value))

        # Handle optional fields that might not be filled
        # Replace remaining placeholders with generic text
        generic_replacements = {
            '{deal_mention}': 'recent transactions',
            '{discussion_topic}': 'the industry',
            '{specific_insight}': 'your insights',
            '{specific_followup}': 'our previous discussion',
            '{update_on_your_end}': 'I wanted to share an update on my progress',
            '{timeframe}': 'recently',
            '{referrer_context}': '',
            '{mascot}': 'team'
        }

        for placeholder, default in generic_replacements.items():
            if placeholder in result:
                result = result.replace(placeholder, default)

        return result.strip()

    def get_recipient_template(self) -> Dict[str, str]:
        """Get template dictionary for recipient data."""
        return {
            'name': 'Full Name',
            'title': 'Mr./Ms./Dr.',
            'bank': 'Bank Name',
            'group': 'Coverage/Product Group',
            'seniority': 'Analyst/Associate/VP/MD',
            'relationship': 'Cold/Warm/Referral/Alumni'
        }

    def get_sender_template(self) -> Dict[str, str]:
        """Get template dictionary for sender data."""
        return {
            'your_name': 'Your Full Name',
            'your_school': 'Your University',
            'your_background': 'Your Year/Major'
        }

    def get_optional_fields(self) -> Dict[str, str]:
        """Get optional fields that enhance personalization."""
        return {
            'deal_mention': 'Specific deal or transaction',
            'discussion_topic': 'Topic discussed in previous conversation',
            'specific_insight': 'Specific insight they shared',
            'specific_followup': 'Follow-up item from conversation',
            'update_on_your_end': 'Your update or progress',
            'timeframe': 'When you spoke (e.g., last week, yesterday)',
            'referrer_name': 'Person who referred you',
            'referrer_context': 'How you know the referrer',
            'mascot': 'School mascot/team name'
        }

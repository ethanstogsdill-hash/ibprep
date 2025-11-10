"""LinkedIn contact discovery and scraping utilities."""

import re
import json
from typing import List, Dict, Optional
from urllib.parse import quote_plus


class LinkedInScraper:
    """
    LinkedIn contact discovery tools.

    Note: This uses public profile data and search. For best results,
    use your own LinkedIn account and search manually, then import results.
    """

    def __init__(self):
        """Initialize scraper."""
        pass

    def parse_profile_url(self, url: str) -> Dict[str, str]:
        """
        Extract information from a LinkedIn profile URL.

        Args:
            url: LinkedIn profile URL

        Returns:
            Dictionary with extracted information
        """
        contact_data = {
            'linkedin_url': url,
            'source': 'LinkedIn URL'
        }

        # Extract username from URL
        username_match = re.search(r'linkedin\.com/in/([^/\?]+)', url)
        if username_match:
            contact_data['linkedin_username'] = username_match.group(1)

        return contact_data

    def generate_linkedin_search_url(
        self,
        company: str,
        title_keywords: Optional[str] = None,
        location: Optional[str] = None
    ) -> str:
        """
        Generate a LinkedIn search URL for manual searching.

        Args:
            company: Company name
            title_keywords: Keywords for title (e.g., "analyst", "M&A")
            location: Location string

        Returns:
            LinkedIn search URL
        """
        base_url = "https://www.linkedin.com/search/results/people/?"

        params = []

        # Company
        params.append(f"keywords={quote_plus(company)}")

        # Title keywords
        if title_keywords:
            current_company_filter = f"currentCompany={quote_plus(company)}"
            title_filter = f"title={quote_plus(title_keywords)}"
            params.append(current_company_filter)

        # Location
        if location:
            params.append(f"geoUrn={quote_plus(location)}")

        return base_url + "&".join(params)

    def parse_linkedin_name(self, full_name: str) -> Dict[str, str]:
        """
        Parse a name into first and last name.

        Args:
            full_name: Full name string

        Returns:
            Dictionary with first_name and last_name
        """
        parts = full_name.strip().split()

        return {
            'name': full_name.strip(),
            'first_name': parts[0] if parts else '',
            'last_name': ' '.join(parts[1:]) if len(parts) > 1 else ''
        }

    def extract_title_info(self, title: str) -> Dict[str, str]:
        """
        Extract seniority and role from a job title.

        Args:
            title: Job title string

        Returns:
            Dictionary with seniority and other extracted info
        """
        title_lower = title.lower()

        result = {'title': title}

        # Seniority detection
        if any(word in title_lower for word in ['managing director', 'md']):
            result['seniority'] = 'MD'
        elif any(word in title_lower for word in ['director', 'dir']):
            result['seniority'] = 'Director'
        elif any(word in title_lower for word in ['vice president', 'vp', 'v.p.']):
            result['seniority'] = 'VP'
        elif 'associate' in title_lower and 'vice' not in title_lower:
            result['seniority'] = 'Associate'
        elif 'analyst' in title_lower:
            result['seniority'] = 'Analyst'
        elif any(word in title_lower for word in ['intern', 'summer']):
            result['seniority'] = 'Intern'
        else:
            result['seniority'] = 'Unknown'

        # Division detection
        if any(word in title_lower for word in ['investment banking', 'ib', 'ibd']):
            result['division'] = 'Investment Banking'
        elif 'm&a' in title_lower or 'mergers' in title_lower:
            result['division'] = 'M&A'
        elif 'equity' in title_lower and 'private' in title_lower:
            result['division'] = 'Private Equity'
        elif 'sales' in title_lower or 'trading' in title_lower:
            result['division'] = 'Sales & Trading'
        elif 'research' in title_lower:
            result['division'] = 'Research'
        elif 'restructuring' in title_lower:
            result['division'] = 'Restructuring'

        # Group detection
        if 'tmt' in title_lower or 'tech' in title_lower:
            result['group_name'] = 'TMT'
        elif 'healthcare' in title_lower or 'health' in title_lower:
            result['group_name'] = 'Healthcare'
        elif 'energy' in title_lower:
            result['group_name'] = 'Energy'
        elif 'financial' in title_lower and 'institutions' in title_lower:
            result['group_name'] = 'FIG'
        elif 'consumer' in title_lower or 'retail' in title_lower:
            result['group_name'] = 'Consumer/Retail'
        elif 'industrial' in title_lower:
            result['group_name'] = 'Industrials'
        elif 'real estate' in title_lower:
            result['group_name'] = 'Real Estate'

        return result

    def create_contact_from_manual_entry(
        self,
        name: str,
        bank: str,
        title: str,
        location: str = "",
        linkedin_url: str = "",
        notes: str = ""
    ) -> Dict[str, str]:
        """
        Create a contact dictionary from manual entry.

        Args:
            name: Full name
            bank: Bank name
            title: Job title
            location: Location string
            linkedin_url: LinkedIn profile URL
            notes: Additional notes

        Returns:
            Contact dictionary ready for database
        """
        contact = self.parse_linkedin_name(name)
        contact['bank'] = bank

        # Extract title info
        title_info = self.extract_title_info(title)
        contact.update(title_info)

        # Parse location
        if location:
            location_parts = [p.strip() for p in location.split(',')]
            if len(location_parts) >= 2:
                contact['location_city'] = location_parts[0]
                contact['location_state'] = location_parts[1]
                if len(location_parts) >= 3:
                    contact['location_country'] = location_parts[2]
            elif len(location_parts) == 1:
                contact['location_city'] = location_parts[0]

        if linkedin_url:
            contact['linkedin_url'] = linkedin_url

        if notes:
            contact['notes'] = notes

        contact['source'] = 'Manual Entry'

        return contact


class ContactFinder:
    """Helper class to generate search instructions for finding contacts."""

    SEARCH_TEMPLATES = {
        'linkedin_manual': """
LinkedIn Manual Search Instructions:
====================================

1. Go to LinkedIn and search for people
2. Use these filters:
   - Company: {bank}
   - Title contains: {title_keywords}
   - Location: {location}

3. Look for people with titles like:
   {example_titles}

4. Copy their information and use the "Add Contact" feature in this tool

Search URL: {search_url}
""",

        'google_search': """
Google Search Method:
====================

Search Google for: site:linkedin.com "{bank}" "{division}" "{location}"

Example: site:linkedin.com "Goldman Sachs" "Investment Banking" "New York"

This will show LinkedIn profiles of people at {bank} in {division}.
""",

        'alumni_database': """
Alumni Database Search:
======================

1. Log into your school's alumni database
2. Filter by:
   - Company: {bank}
   - Industry: Investment Banking / Financial Services
   - Location: {location}

3. Export results and import via CSV to this tool
"""
    }

    @staticmethod
    def get_search_instructions(
        bank: str,
        division: str = "",
        location: str = "",
        method: str = "linkedin_manual"
    ) -> str:
        """
        Generate search instructions for finding contacts.

        Args:
            bank: Bank name
            division: Division/group
            location: Location
            method: Search method to use

        Returns:
            Formatted search instructions
        """
        scraper = LinkedInScraper()

        # Generate title keywords based on division
        title_keywords = division if division else "investment banking"

        # Example titles to look for
        example_titles = [
            f"Analyst - {division}" if division else "Investment Banking Analyst",
            f"Associate - {division}" if division else "Investment Banking Associate",
            f"VP - {division}" if division else "Vice President",
        ]

        # Generate search URL
        search_url = scraper.generate_linkedin_search_url(
            bank,
            title_keywords,
            location
        )

        template = ContactFinder.SEARCH_TEMPLATES.get(method, ContactFinder.SEARCH_TEMPLATES['linkedin_manual'])

        return template.format(
            bank=bank,
            division=division,
            title_keywords=title_keywords,
            location=location,
            example_titles='\n   '.join([f"- {t}" for t in example_titles]),
            search_url=search_url
        )

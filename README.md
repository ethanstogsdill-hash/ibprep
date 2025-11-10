# IB Networking Email Generator

A professional-grade Python tool for discovering IB contacts and generating personalized networking emails. Built for recruiting season with quality and personalization in mind.

## 🌐 Web Interface (Recommended - Easiest!)

**Use it in your browser - no command line needed!**

```bash
python web_server.py
```

Browser opens automatically to beautiful web interface where you can:
- ✅ Search contacts by bank/division/location
- ✅ Load 20 sample contacts to test
- ✅ Generate emails for everyone with one click
- ✅ Add new contacts with a form
- ✅ View database statistics

**[📖 Full Web Interface Guide →](WEB_GUIDE.md)**

---

## Command Line Tools (Advanced)

### `discover.py` - Contact Discovery + Email Generator (NEW!)

**What it does**: Input bank + division + location → Get list of contacts + auto-generated emails

```bash
python discover.py

# Example workflow:
# 1. Search: "Goldman Sachs, M&A, New York, NY"
# 2. Results: Found 15 contacts
# 3. Generate: Personalized email for each person
# 4. Export: All emails saved automatically
```

**Perfect for**: Batch outreach, building contact database, targeting specific banks/divisions

📖 **[Read the full Discovery Guide →](DISCOVERY_GUIDE.md)**

---

### `main.py` - Individual Email Generator (Original)

**What it does**: Input contact details → Get customized email variations

```bash
python main.py

# Example workflow:
# 1. Enter: Name, bank, title, etc.
# 2. Generate: 3 email variations
# 3. Review: Metrics and subject lines
# 4. Save: Track and export
```

**Perfect for**: Follow-ups, one-off emails, high-touch customization

---

## Which Tool Should I Use?

| Scenario | Tool | Why |
|----------|------|-----|
| "I want to email everyone in Goldman M&A" | `discover.py` | Search + batch generate |
| "I need to follow up with someone" | `main.py` | More customization |
| "I have a list of 20 targets" | `discover.py` | Bulk generation |
| "I want a thank you email" | `main.py` | Template flexibility |
| "Starting recruiting season" | `discover.py` | Build database |

**Pro tip**: Use **both**! `discover.py` for initial outreach, `main.py` for follow-ups.

## Features

### Core Functionality
- **5 Email Templates**: Cold outreach, coffee follow-up, thank you, referral-based, alumni connection
- **Smart Tone Adjustment**: Automatic tone selection based on seniority and relationship
- **Multiple Variations**: Generate 1-5 variations per recipient with different subject lines
- **Email Metrics**: Word count, character count, readability scores, and length assessment
- **Tracking System**: Track sent emails, responses, and follow-up timing
- **Batch Processing**: Generate emails for multiple recipients from CSV

### Built-in Best Practices
- ✅ Emails kept under 150 words (ideal length)
- ✅ Specific asks (15-20 min call)
- ✅ Professional but personable tone
- ✅ Strong, attention-grabbing subject lines
- ✅ Demonstrates genuine interest

### 🆕 Contact Discovery Features
- **Contact Database**: SQLite database to store and manage IB contacts
- **Smart Search**: Filter by bank, division, group, location, seniority
- **Auto Title Parsing**: Automatically extract seniority/division from job titles
- **Bulk Import**: Import contacts from CSV (alumni databases, recruiter lists)
- **Search Instructions**: Generate LinkedIn/Google search URLs
- **Batch Email Generation**: Generate personalized emails for all matching contacts
- **Database Stats**: Track your network by bank, division, location

## Installation

### Requirements
- Python 3.7 or higher
- No external dependencies (uses Python standard library only)

### Setup
```bash
# Clone or download the repository
git clone <your-repo-url>
cd ibprep

# Make main.py executable (optional)
chmod +x main.py

# Run the application
python main.py
```

## Usage

### Interactive Mode (Recommended)

```bash
python main.py
```

Follow the interactive prompts to:
1. Select email template type
2. Enter recipient information
3. Enter your information
4. Add optional customization
5. Review generated emails with metrics
6. Save and track emails

### Batch Mode

1. Create a CSV file with recipient information:

```csv
name,bank,group,seniority,relationship,deal_mention,tone
John Smith,Goldman Sachs,TMT,Associate,Cold,Microsoft-Activision deal,warm
Jane Doe,Morgan Stanley,Healthcare M&A,VP,Alumni,Pfizer acquisition,
```

2. Run batch generation:
```bash
python main.py
# Select option 2: Batch Generate from CSV
# Enter your CSV filename
```

3. Find generated emails in the `output/` directory

### Generate Sample CSV Template

```bash
python main.py
# Select option 2: Batch Generate from CSV
# Enter 'sample' when prompted for filename
# Edit sample_batch_input.csv with your recipients
```

## Email Templates

### 1. Cold Outreach
Initial contact with someone you haven't met. Best for:
- First-time outreach
- LinkedIn connections
- Industry professionals

**Recommended for**: All seniority levels

### 2. Coffee Follow-up
Following up after an initial conversation. Best for:
- After informational interviews
- Following coffee chats
- Maintaining relationships

**Recommended for**: Continuing conversations

### 3. Thank You
Post-interview or post-conversation gratitude. Best for:
- After informational interviews
- After formal interviews
- After networking events

**Recommended for**: Immediate follow-up (same day)

### 4. Referral-Based Introduction
When someone referred you to a contact. Best for:
- Warm introductions
- Mutual connections
- Leveraging your network

**Recommended for**: All seniority levels (high response rate)

### 5. Alumni Connection
Connecting with school alumni. Best for:
- Same university connections
- Leveraging school networks
- Building alumni relationships

**Recommended for**: Recent grads and current students

## Tone Levels

### Formal
- Use for: MDs, Directors, first-time cold outreach to senior people
- Characteristics: Professional, respectful, traditional structure
- Example: "Dear Mr. Smith, I hope this email finds you well..."

### Warm (Default)
- Use for: Associates, VPs, referral-based contacts
- Characteristics: Professional but friendly, conversational
- Example: "Hi John, My name is..."

### Casual
- Use for: Analysts, alumni connections, warm relationships
- Characteristics: Friendly, approachable, less formal
- Example: "Hi John, Hope you're doing well!..."

**Note**: The system automatically recommends tone based on seniority and relationship type.

## Tracking System

The tool includes a built-in tracking system that:
- Records all sent emails
- Tracks response status
- Suggests follow-up timing
- Provides analytics (response rates, by bank, by type)

### Recommended Follow-up Timing
- Cold outreach: 5 days
- Referral: 4 days
- Alumni: 5 days
- Coffee follow-up: 7 days
- Thank you: 14 days

### View Your Statistics
```bash
python main.py
# Select option 3: View Tracking Stats
```

### Check Pending Follow-ups
```bash
python main.py
# Select option 4: View Pending Follow-ups
```

## Email Metrics

Each generated email includes:
- **Word Count**: Target is ≤150 words (Ideal), ≤200 (Good), ≤250 (Acceptable)
- **Character Count**: Total characters with/without spaces
- **Readability**: Excellent, Good, Fair, or Complex
- **Sentence Count**: Number of sentences
- **Average Words per Sentence**: Measures sentence complexity

## Customization Guide

### Modifying Templates

Templates are stored in `templates/` directory as plain text files. Each template has:
- Subject line options (multiple variations)
- Three tone levels (FORMAL, WARM, CASUAL)
- Placeholder variables in `{brackets}`

To customize:
```bash
# Edit any template file
nano templates/cold_outreach.txt

# Changes take effect immediately (no restart needed)
```

### Available Variables

#### Required Fields
- `{name}` - Recipient's full name
- `{first_name}` - Recipient's first name (auto-extracted)
- `{title}` - Mr./Ms./Dr.
- `{bank}` - Bank name
- `{group}` - Coverage or product group
- `{seniority}` - Job level
- `{your_name}` - Your full name
- `{your_school}` - Your university
- `{your_background}` - Your year/major/role

#### Optional Fields (Template-Specific)
- `{deal_mention}` - Specific deal or transaction
- `{discussion_topic}` - Topic from previous conversation
- `{specific_insight}` - Insight they shared
- `{referrer_name}` - Person who referred you
- `{referrer_context}` - How you know referrer
- `{mascot}` - School mascot/team name
- `{timeframe}` - When you spoke

### Adding New Templates

1. Create a new template file:
```bash
nano templates/my_template.txt
```

2. Use this structure:
```
SUBJECT_LINES:
- Subject line option 1
- Subject line option 2
- Subject line option 3

FORMAL:
[Your formal email body with {variables}]

WARM:
[Your warm email body with {variables}]

CASUAL:
[Your casual email body with {variables}]
```

3. Register in `src/templates.py`:
```python
TEMPLATE_TYPES = {
    # ... existing templates ...
    "my_template": "My Template Description"
}
```

## File Structure

```
ibprep/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies (none needed!)
├── README.md              # This file
├── src/
│   ├── __init__.py
│   ├── cli.py             # Interactive CLI interface
│   ├── generator.py       # Core email generation logic
│   ├── templates.py       # Template management
│   ├── tracker.py         # Email tracking system
│   └── metrics.py         # Analytics and metrics
├── templates/
│   ├── cold_outreach.txt
│   ├── coffee_followup.txt
│   ├── thank_you.txt
│   ├── referral.txt
│   └── alumni.txt
├── data/
│   └── tracking.csv       # Your email tracking database
└── output/                # Batch-generated emails (auto-created)
```

## Tips for Best Results

### Research is Key
- Mention specific deals the bank worked on
- Reference recent news or transactions
- Show genuine interest, not just "I want a job"

### Personalization Matters
- Always mention a specific deal if possible
- Reference shared connections (alumni, mutual contacts)
- Demonstrate you've done your homework

### Timing
- Send emails Tuesday-Thursday, 9 AM - 11 AM or 2 PM - 4 PM
- Avoid Monday mornings and Friday afternoons
- Follow up on the recommended schedule (but don't be pushy)

### Subject Lines
- Keep under 50 characters
- Include school name (alumni connection)
- Be specific but not generic
- The tool generates multiple options - test different ones

### Quality > Quantity
- Don't mass-email with identical content
- Customize each email with specific details
- Track responses to learn what works
- 10 personalized emails > 50 generic ones

## Tracking Data

All tracking data is stored in `data/tracking.csv`. This file includes:
- Date sent
- Recipient details
- Email type and subject
- Response status
- Follow-up dates
- Notes

You can:
- Open in Excel/Google Sheets for analysis
- Import into your CRM
- Share with career services
- Track your networking progress

## Common Use Cases

### Scenario 1: Starting Coffee Chats
```
1. Use "Cold Outreach" or "Alumni" template
2. Tone: Warm or Casual (for analysts/associates)
3. Mention: Recent deal, your specific interest
4. Ask: 15-20 minute call
5. Track: Follow up in 5 days if no response
```

### Scenario 2: Recruiting Season Blast
```
1. Create CSV with 20-30 targets
2. Research each person (deals, background)
3. Use batch mode with customized deal mentions
4. Generate all at once
5. Send over 2-3 days (not all at once)
6. Track responses and follow up
```

### Scenario 3: Post-Interview Follow-up
```
1. Use "Thank You" template
2. Send same day (within 24 hours)
3. Reference specific conversation points
4. Keep brief (even shorter than usual)
5. No need to ask for another meeting
```

### Scenario 4: Leveraging Referrals
```
1. Use "Referral" template
2. Include how you know the referrer
3. Mention referrer suggested specific topics
4. Follow up in 4 days (faster than cold)
5. CC the referrer if appropriate
```

## Troubleshooting

### Issue: Templates not loading
```bash
# Ensure you're in the right directory
cd ibprep
python main.py

# Check templates exist
ls templates/
```

### Issue: CSV batch not working
- Ensure CSV has correct headers
- Check for special characters in names
- Verify file encoding is UTF-8
- Use the sample CSV as reference

### Issue: Tracking file errors
```bash
# Reset tracking (WARNING: deletes existing data)
rm data/tracking.csv
python main.py  # Will recreate empty tracking file
```

## Best Practices Summary

✅ **DO**:
- Personalize every email
- Mention specific deals/interests
- Keep under 150 words
- Use tracking system
- Follow up appropriately
- Test different subject lines
- Read generated emails before sending

❌ **DON'T**:
- Send identical emails to multiple people at same bank
- Use overly formal language for analysts
- Send on weekends or late at night
- Follow up more than twice
- Lie about your background or interests
- Skip proofreading
- Send without customization

## Advanced Features

### Custom Tone Mapping
Edit `src/generator.py` to customize tone recommendations:
```python
SENIORITY_TONE_MAP = {
    "analyst": "casual",      # Change to "warm" if preferred
    "associate": "warm",
    "vp": "warm",            # Change to "formal" if preferred
    # ... etc
}
```

### Custom Follow-up Timing
Edit `src/tracker.py` to adjust follow-up schedules:
```python
FOLLOWUP_TIMING = {
    'cold_outreach': 5,      # Change to 7 for longer wait
    'referral': 4,           # Change to 3 for faster follow-up
    # ... etc
}
```

## Support

For issues, questions, or feature requests:
1. Check this README first
2. Review the template files in `templates/`
3. Check the tracking CSV format
4. Modify templates as needed (they're just text files!)

## License

This tool is for personal use in job searching and networking. Use professionally and ethically.

---

**Good luck with your IB recruiting!** 🚀

Remember: Quality networking emails lead to quality conversations. Take the time to personalize, research, and be genuine. This tool handles the format and structure - you bring the authenticity and effort.

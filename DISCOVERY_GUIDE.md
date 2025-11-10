# Contact Discovery & Email Generator Guide

## What This Does

**Input**: Bank name, division, location
```
Goldman Sachs, M&A, New York, NY
```

**Output**: List of contacts + auto-generated emails for each
```
Found 15 contacts:

1. John Smith - Associate, M&A at Goldman Sachs
   ✅ Email generated and saved

2. Sarah Johnson - Analyst, M&A at Goldman Sachs
   ✅ Email generated and saved

... (13 more)
```

---

## Quick Start (2 Minutes)

### Step 1: Load Sample Data
```bash
python discover.py
# Select option 7: Load Sample Data
# This adds 20 realistic IB contacts to test with
```

### Step 2: Search & Generate Emails
```bash
# Still in the same menu:
# Select option 1: Search Contacts & Generate Emails

# Enter search criteria:
Bank: Goldman Sachs
Division: M&A
City: New York
State: NY
Seniority: [press Enter to skip]

# Found 3 contacts!
# Generate emails? Yes
# Enter your info
# Select email template
# Done! All emails saved to output/batch_discovery/
```

That's it! You now have personalized emails for multiple people.

---

## How It Works

### The Workflow

```
1. BUILD DATABASE
   ↓
   Add contacts manually, import CSV, or load sample data

2. SEARCH CONTACTS
   ↓
   Filter by bank, division, location, seniority

3. AUTO-GENERATE EMAILS
   ↓
   Personalized email for each contact

4. EXPORT & TRACK
   ↓
   Save all emails, add to tracking system
```

---

## Building Your Contact Database

### Option 1: Load Sample Data (For Testing)

```bash
python discover.py
# Option 7: Load Sample Data
```

Adds 20 sample contacts across:
- Goldman Sachs, Morgan Stanley, JP Morgan
- Various divisions: M&A, TMT, Healthcare, etc.
- Different seniorities: Analyst, Associate, VP, MD
- Multiple locations: New York, San Francisco, Chicago, etc.

**Perfect for**: Testing the system, learning the workflow

---

### Option 2: Add Contacts Manually

```bash
python discover.py
# Option 2: Add Contact Manually
```

Enter:
- Full name
- Bank
- Job title (e.g., "Associate - M&A")
- Location (e.g., "New York, NY")
- LinkedIn URL (optional)
- Notes (optional)

The system automatically:
- Extracts first/last name
- Determines seniority from title
- Identifies division and group
- Parses location into city/state

**Perfect for**: Adding individual contacts you found on LinkedIn

---

### Option 3: Import from CSV

```bash
python discover.py
# Option 3: Import Contacts from CSV
# Enter 'sample' to create a template
```

CSV format:
```csv
name,bank,title,division,group_name,seniority,location_city,location_state,linkedin_url,notes
John Doe,Goldman Sachs,Associate - M&A,Investment Banking,M&A,Associate,New York,NY,https://linkedin.com/in/johndoe,Met at conference
Jane Smith,Morgan Stanley,Analyst - Healthcare,Investment Banking,Healthcare,Analyst,SF,CA,,Alumni
```

**Perfect for**: Bulk imports from alumni databases, recruiter lists

---

### Option 4: Get Search Instructions

```bash
python discover.py
# Option 5: Get Search Instructions
```

This generates detailed instructions for finding contacts on:
- **LinkedIn** - Direct search URL + manual search steps
- **Google** - Search strings to find LinkedIn profiles
- **Alumni Database** - How to filter and export

Example output:
```
LinkedIn Manual Search Instructions:
====================================

1. Go to LinkedIn and search for people
2. Use these filters:
   - Company: Goldman Sachs
   - Title contains: M&A
   - Location: New York, NY

3. Look for people with titles like:
   - Analyst - M&A
   - Associate - M&A
   - VP - M&A

Search URL: https://www.linkedin.com/search/results/people/?keywords=Goldman+Sachs...
```

**Perfect for**: Finding new contacts to add to your database

---

## Searching and Generating Emails

### Basic Search

```bash
python discover.py
# Option 1: Search Contacts & Generate Emails
```

**Search by**:
- Bank (partial match works: "Goldman" finds "Goldman Sachs")
- Division (e.g., "M&A", "Investment Banking")
- Group (e.g., "TMT", "Healthcare")
- Location (city and/or state)
- Seniority (Analyst, Associate, VP, MD)

**Leave any field blank to skip it**

### Example Searches

#### 1. All Goldman Sachs M&A in New York
```
Bank: Goldman Sachs
Division: M&A
City: New York
State: NY
```

#### 2. All Healthcare bankers (any bank, any location)
```
Bank: [blank]
Division: [blank]
Group: Healthcare
```

#### 3. All Analysts in San Francisco
```
Seniority: Analyst
City: San Francisco
State: CA
```

#### 4. All Morgan Stanley contacts
```
Bank: Morgan Stanley
[everything else blank]
```

---

## Email Generation Process

Once you find contacts, the system:

### 1. Shows Results
```
Found 5 contact(s):

1. John Smith
   Associate - M&A at Goldman Sachs
   Division: Investment Banking
   Location: New York, NY

2. Sarah Johnson
   ...
```

### 2. Asks for Your Info (Once)
```
Your full name: Jane Doe
Your university: University of Pennsylvania
Your background: Junior studying Finance
```

### 3. Select Email Template
```
1. Initial Cold Outreach
2. Coffee Chat Follow-up
3. Post-Interview Thank You
4. Referral-Based Introduction
5. Alumni Connection

Select template (1-5): 1
```

### 4. Optional Global Deal Mention
```
Global deal mention (applies to all): Microsoft-Activision acquisition
```

### 5. Auto-Generates All Emails
```
🔄 Generating emails for 5 contacts...

✅ John Smith - Goldman Sachs
✅ Sarah Johnson - Goldman Sachs
✅ Michael Chen - Goldman Sachs
✅ Emily Davis - Goldman Sachs
✅ Robert Martinez - Goldman Sachs

🎉 Successfully generated 5 emails!
📁 Saved to: output/batch_discovery/
📊 Added all to tracking system
```

---

## Output Files

### Email Files

Location: `output/batch_discovery/`

Format: `FirstName_LastName_BankName.txt`

Example: `John_Smith_Goldman_Sachs.txt`

Contents:
```
================================================================================
EMAIL VARIATION 1
================================================================================

Subject: Goldman Sachs M&A - Quick Question from University of Pennsylvania Student

Hi John,

My name is Jane Doe, and I'm a Junior studying Finance at University of Pennsylvania.
I'm reaching out because I'm deeply interested in M&A investment banking and have been
following Goldman Sachs's work in the space.

Goldman Sachs's execution on Microsoft-Activision acquisition really caught my attention,
and I'd love to learn more about your experience working in M&A...

--- Metrics ---
Words: 96 (Ideal)
Characters: 576
Readability: Excellent
```

### Tracking

All generated emails are automatically added to your tracking system.

View stats:
```bash
python main.py
# Option 3: View Tracking Stats
```

---

## Real-World Workflow

### Scenario: Targeting Goldman Sachs M&A

#### Week 1: Build Database

**Monday**: Search LinkedIn
```bash
python discover.py
# Option 5: Get Search Instructions
# Bank: Goldman Sachs, Division: M&A, Location: New York, NY
# Follow the generated instructions
# Find 10-15 people on LinkedIn
```

**Tuesday**: Add Contacts
```bash
python discover.py
# Option 2: Add Contact Manually
# Add each person you found (takes 1 min each)
```

Or bulk import:
```bash
# Create CSV with all contacts
python discover.py
# Option 3: Import Contacts from CSV
```

#### Week 1: Generate & Send

**Wednesday**: Generate Emails
```bash
python discover.py
# Option 1: Search & Generate
# Bank: Goldman Sachs, Division: M&A
# Generate all emails at once
```

**Thursday-Friday**: Review and Send
- Open each file in `output/batch_discovery/`
- Customize further if needed
- Send 2-3 per day (don't send all at once!)

#### Week 2: Track & Follow Up

Use the original email generator for follow-ups:
```bash
python main.py
# Check tracking system
# Generate thank you emails for responses
```

---

## Tips for Success

### Finding Contacts

✅ **DO**:
- Use your school's alumni database first
- Search LinkedIn with specific filters
- Ask professors/career services for contacts
- Attend networking events and add people after
- Join relevant LinkedIn groups

❌ **DON'T**:
- Scrape LinkedIn aggressively (against ToS)
- Add fake/unverified contacts
- Use outdated contact lists

### Building Your Database

✅ **Start Small**: 20-30 high-quality contacts > 200 random people

✅ **Keep Updated**: Mark notes when you email someone

✅ **Segment**: Organize by priority (target, backup, reach)

✅ **Verify**: Double-check titles/locations are current

### Generating Emails

✅ **Research First**: Add deal mentions, notes about each person

✅ **Customize**: Don't send identical emails to people at same bank

✅ **Stagger**: Generate all at once, send over 1-2 weeks

✅ **Track**: Use tracking system to avoid double-emailing

### Response Rates

Expected response rates by source:
- **Alumni**: 30-50%
- **Referral**: 50-70%
- **Cold (with research)**: 15-25%
- **Cold (generic)**: 5-10%

Improve rates by:
- Mentioning specific deals
- Showing genuine interest
- Being concise (<150 words)
- Having a clear ask

---

## Advanced Features

### Smart Title Parsing

The system automatically extracts:

**From**: "Associate - Healthcare M&A"
**Extracts**:
- Seniority: Associate
- Division: M&A
- Group: Healthcare

**From**: "VP, Technology Investment Banking"
**Extracts**:
- Seniority: VP
- Division: Investment Banking
- Group: TMT

### Auto-Tone Selection

Based on contact's seniority:
- **Analyst** → Casual tone
- **Associate** → Warm tone
- **VP** → Warm tone
- **Director/MD** → Formal tone

You can override this when generating emails.

### Flexible Search

All searches use partial matching:
- "Goldman" finds "Goldman Sachs"
- "M&A" finds "M&A", "Mergers & Acquisitions"
- "New York" finds "New York, NY"

Case-insensitive.

---

## Database Management

### View All Contacts
```bash
python discover.py
# Option 4: View All Contacts
```

### View Stats
```bash
python discover.py
# Option 6: View Database Stats
```

Example output:
```
Total Contacts: 47

--- Top Banks ---
  Goldman Sachs: 12
  Morgan Stanley: 10
  JP Morgan: 8
  ...

--- Top Divisions ---
  Investment Banking: 32
  M&A: 15
  ...

--- Top Locations ---
  New York, NY: 28
  San Francisco, CA: 8
  ...
```

### Database Location

File: `data/contacts.db`

- SQLite database
- Can open with any SQLite browser
- Backup regularly during recruiting season

---

## Troubleshooting

### "No contacts found matching criteria"

**Solution**:
1. Try broader search (fewer filters)
2. Check spelling of bank name
3. Add more contacts first (options 2, 3, or 7)

### "Error importing CSV"

**Solution**:
1. Check CSV has correct headers
2. Verify file encoding is UTF-8
3. Use `'sample'` to generate template
4. Make sure no special characters in file path

### "Database locked"

**Solution**:
1. Close all instances of the program
2. Delete `data/contacts.db-journal` if it exists
3. Restart

---

## FAQ

**Q: Can this automatically scrape LinkedIn for contacts?**
A: No - that would violate LinkedIn's Terms of Service. Instead, this tool helps you:
- Generate search URLs to find people manually
- Organize contacts you find
- Auto-generate personalized emails

**Q: Where do I get contact data?**
A: Best sources:
1. School alumni database (best!)
2. LinkedIn manual search (add to database)
3. Career services contact lists
4. Networking events
5. Professor/alumni recommendations

**Q: How many contacts should I add?**
A: For one bank/division: 10-20 contacts
For full recruiting: 50-100 high-quality contacts across multiple banks

**Q: Can I edit contacts after adding?**
A: Yes! The database is in `data/contacts.db`. You can:
- Open in SQLite browser to edit
- Re-import from CSV with updated data
- Delete and re-add

**Q: What if someone changed jobs?**
A: Update their entry or add them again with new info. The system allows duplicates.

---

## Integration with Original Email Generator

You have TWO tools now:

### `discover.py` - Contact Discovery
- Find contacts by search
- Batch generate emails
- Database management

### `main.py` - Individual Emails
- Single email generation
- More customization options
- Follow-up emails
- Thank you emails

**Use both!**

Typical workflow:
1. Use `discover.py` to find contacts and generate initial outreach
2. Use `main.py` for follow-ups, thank yous, and one-off emails

---

## Next Steps

1. ✅ Run test: `python test_discovery.py`
2. ✅ Load sample data: `python discover.py` → option 7
3. ✅ Try a search: option 1
4. ✅ Review generated emails in `output/batch_discovery/`
5. ✅ Start building your real database with option 2 or 3

**Pro tip**: Start with sample data to learn the system, then replace with real contacts from your alumni database.

---

Good luck with recruiting! 🚀

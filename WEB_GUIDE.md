# Web Interface Guide

## 🌐 Easy-to-Use Web Interface

No more command line! Use the beautiful web interface in your browser.

## Quick Start (10 Seconds)

```bash
python web_server.py
```

**That's it!** Your browser will automatically open to the interface.

If it doesn't open automatically, go to: **http://localhost:8000**

---

## First Time Setup (30 Seconds)

### Step 1: Start the Server
```bash
cd /home/user/ibprep
python web_server.py
```

### Step 2: Load Sample Data
1. Click the green **"Load Sample Data"** button
2. Wait 2 seconds
3. ✅ 20 contacts loaded!

### Step 3: Search for Contacts
1. Type "Goldman Sachs" in the Bank field
2. Type "M&A" in the Division field
3. Click **"🔍 Search Contacts"**
4. See all matching contacts!

### Step 4: Generate Emails
1. Click **"✉️ Generate Emails for All X Contact(s)"**
2. Fill in your information:
   - Your name
   - Your university
   - Your background (e.g., "Junior studying Finance")
3. Click **"✉️ Generate All Emails"**
4. ✅ Done! All emails saved to `output/batch_discovery/`

---

## Features

### 🔍 Search Tab (Main)
- **Search by**: Bank, Division, Group, Seniority, City, State
- **Live results**: See all matching contacts instantly
- **One-click email generation**: Generate personalized emails for everyone
- **Sample data**: Load 20 test contacts to try it out

### ➕ Add Contact Tab
- Add new contacts one at a time
- Auto-extracts: Seniority, division, group from job title
- Fields: Name, bank, title, location, LinkedIn, notes

### 📊 Stats Tab
- Total contacts in database
- Breakdown by bank
- Breakdown by division
- Breakdown by location

---

## Example Workflow

### Scenario: Target Goldman Sachs M&A NYC

1. **Start server**: `python web_server.py`

2. **Load sample data**: Click green button (if first time)

3. **Search**:
   - Bank: `Goldman Sachs`
   - Division: `M&A`
   - City: `New York`
   - Click Search

4. **Results**: Found 3 contacts
   - John Smith - Analyst
   - Michael Chen - VP
   - Emily Davis - MD

5. **Generate emails**: Click generate button
   - Your name: Jane Doe
   - Your school: UPenn
   - Your background: Junior studying Finance
   - Deal mention: Microsoft-Activision deal
   - Template: Cold Outreach
   - Click Generate

6. **Done!**
   - ✅ 3 emails generated
   - 📁 Saved to `output/batch_discovery/`
   - 📊 Tracked automatically

---

## Screenshots (What You'll See)

### Main Screen
```
┌─────────────────────────────────────────────────┐
│        🎯 IB Contact Finder                     │
│   Find investment banking contacts and          │
│   generate personalized emails                  │
├─────────────────────────────────────────────────┤
│  [🔍 Search] [➕ Add Contact] [📊 Stats]        │
├─────────────────────────────────────────────────┤
│                                                  │
│  👋 First time? Load sample data                │
│  [Load Sample Data]                              │
│                                                  │
│  Bank Name: [Goldman Sachs            ]         │
│  Division:  [M&A                      ]         │
│  Group:     [                         ]         │
│  Seniority: [All Levels ▼             ]         │
│  City:      [New York                 ]         │
│  State:     [NY                       ]         │
│                                                  │
│  [🔍 Search Contacts]  [Clear]                  │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Results
```
┌─────────────────────────────────────────────────┐
│  ✅ Found 3 contact(s)                          │
├─────────────────────────────────────────────────┤
│  John Smith                                      │
│  Analyst - M&A at Goldman Sachs                 │
│  Division: Investment Banking - M&A              │
│  📍 New York, NY                                │
├─────────────────────────────────────────────────┤
│  Michael Chen                                    │
│  VP - Healthcare M&A at Goldman Sachs           │
│  Division: Investment Banking - Healthcare       │
│  📍 New York, NY                                │
├─────────────────────────────────────────────────┤
│  [✉️ Generate Emails for All 3 Contact(s)]     │
└─────────────────────────────────────────────────┘
```

---

## Tips

### For Best Results

1. **Load sample data first** - Test the system before adding real contacts

2. **Start broad, refine later** - Search just "Goldman Sachs" first, then add filters

3. **Leave fields blank** - Only fill in what you want to filter by

4. **Use partial matches** - "Goldman" finds "Goldman Sachs"

5. **Save your info** - After first time, your browser remembers your name/school

### Building Your Database

**Option 1: Add Manually**
- Go to "Add Contact" tab
- Enter one contact at a time
- Great for high-value targets

**Option 2: Import CSV**
- Use command line: `python discover.py` → option 3
- Bulk import from alumni database
- Then use web interface to search/generate

**Option 3: Start with Sample**
- Load sample data
- Replace with real contacts over time
- Keep sample data to test new templates

---

## Customization

### Change the Port

Default: http://localhost:8000

Use different port:
```bash
python web_server.py 9000
```

Now visit: http://localhost:9000

### Email Templates

The web interface uses all 5 templates:
- Cold Outreach (default)
- Alumni Connection
- Referral Introduction
- Coffee Follow-up
- Thank You

Select from dropdown when generating emails.

### Modify Templates

Templates are in `templates/` folder:
- Edit any `.txt` file
- Changes apply immediately
- No server restart needed

---

## Output

### Where Are My Emails?

All generated emails are saved to:
```
output/batch_discovery/
```

### File Format

Each contact gets one file:
```
John_Smith_Goldman_Sachs.txt
Michael_Chen_Goldman_Sachs.txt
Emily_Davis_Goldman_Sachs.txt
```

### File Contents

```
================================================================================
EMAIL VARIATION 1
================================================================================

Subject: Goldman Sachs M&A - Quick Question from University of Pennsylvania Student

Hi John,

My name is Jane Doe, and I'm a Junior studying Finance at University of Pennsylvania...

[Full email body]

--- Metrics ---
Words: 96 (Ideal)
Characters: 576
Readability: Excellent
```

---

## Tracking

All generated emails are **automatically added** to the tracking system.

View tracking:
```bash
python main.py
# Option 3: View Tracking Stats
```

Or check the file:
```
data/tracking.csv
```

---

## Troubleshooting

### "Address already in use" Error

Another program is using port 8000.

**Solution**: Use different port
```bash
python web_server.py 8001
```

### Can't Connect to Server

**Solution 1**: Make sure server is running
- Look for "Server running at" message
- Don't close the terminal

**Solution 2**: Try different browser
- Chrome, Firefox, Safari all work

**Solution 3**: Check the URL
- Should be: http://localhost:8000
- NOT: https://localhost:8000

### Sample Data Not Loading

**Solution**: Check terminal for errors
- Server shows all errors in terminal
- Look for database permissions issues

### Generated Emails Are Empty

**Solution**: Fill in all required fields
- Your name *
- Your school *
- Your background *
- These are marked with asterisks (*)

---

## Advanced

### Use While Traveling

Want to use on your phone?

1. Find your computer's IP address:
   ```bash
   # Mac/Linux
   ifconfig | grep "inet "

   # Windows
   ipconfig
   ```

2. Start server on all interfaces:
   ```bash
   python web_server.py
   ```

3. On phone, go to: `http://YOUR_IP:8000`

Example: `http://192.168.1.100:8000`

### Run in Background

**Mac/Linux**:
```bash
python web_server.py &
```

**Windows**:
```bash
start python web_server.py
```

### Keep Running After Closing Terminal

**Mac/Linux**:
```bash
nohup python web_server.py &
```

**Stop it later**:
```bash
pkill -f web_server.py
```

---

## Comparison: Web vs CLI

| Feature | Web Interface | CLI (`discover.py`) |
|---------|---------------|---------------------|
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visual | ✅ Beautiful UI | ❌ Text only |
| Mouse/Click | ✅ Yes | ❌ Keyboard only |
| Multiple tabs | ✅ Yes | ❌ No |
| Real-time preview | ✅ Yes | ❌ No |
| Search instructions | ❌ No | ✅ Yes |
| CSV import | ❌ Use CLI | ✅ Yes |
| Speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Recommendation**: Use web interface for most tasks. Use CLI for CSV imports and search instructions.

---

## FAQ

**Q: Do I need to install anything?**
A: No! It's pure Python with no dependencies.

**Q: Can multiple people use it?**
A: Yes, but one at a time. Database doesn't support concurrent writes.

**Q: Is my data saved?**
A: Yes! Everything is saved to `data/contacts.db` automatically.

**Q: Can I use this for other industries?**
A: Yes! Just change the contact data. Works for consulting, PE, VC, etc.

**Q: Does it work offline?**
A: Yes! No internet needed. Everything runs locally.

**Q: Can I export my data?**
A: Yes! The database is SQLite format. Open with any SQLite browser.

---

## Next Steps

1. ✅ Start server: `python web_server.py`
2. ✅ Load sample data: Click green button
3. ✅ Try a search: "Goldman Sachs"
4. ✅ Generate emails: Click generate button
5. ✅ Check output: `output/batch_discovery/`

Then:
- Add real contacts (Add Contact tab)
- Customize email templates (`templates/` folder)
- Start your recruiting campaign!

---

**Have fun networking!** 🚀

For the old command-line interface, see: [DISCOVERY_GUIDE.md](DISCOVERY_GUIDE.md)

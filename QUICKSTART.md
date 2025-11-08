# Quick Start Guide

## Get Started in 2 Minutes

### Installation
```bash
cd ibprep
python main.py
```

That's it! No dependencies to install.

## First Email (Interactive)

1. Run `python main.py`
2. Select option `1` (Generate Single Email)
3. Choose template type (start with `1` for Cold Outreach)
4. Fill in recipient info:
   - Name: John Smith
   - Bank: Goldman Sachs
   - Group: TMT
   - Seniority: Associate
   - Relationship: Cold
5. Fill in your info
6. Add optional deal mention for personalization
7. Review generated emails with metrics
8. Save and track!

## Batch Generation

1. Look at `example_batch_input.csv` for format
2. Create your own CSV with targets
3. Run `python main.py`
4. Select option `2` (Batch Generate)
5. Enter your CSV filename
6. All emails generated in `output/` folder!

## Tips for Success

### Before You Generate
- ✅ Research the person (LinkedIn, bank website)
- ✅ Find a specific recent deal to mention
- ✅ Check alumni database if applicable
- ✅ Have your elevator pitch ready

### After Generation
- ✅ Read each email before sending
- ✅ Customize further if needed
- ✅ Check metrics (aim for <150 words)
- ✅ Use tracking system
- ✅ Follow up appropriately

### Template Selection Guide

**Cold Outreach** → First-time contact
- Use when: No prior relationship
- Best for: Broad networking
- Follow up: 5 days

**Alumni Connection** → School connection
- Use when: Same university
- Best for: Leveraging school network
- Follow up: 5 days

**Referral** → Someone introduced you
- Use when: Mutual connection
- Best for: Warm intros (highest response rate)
- Follow up: 4 days

**Coffee Follow-up** → After initial chat
- Use when: Following up previous conversation
- Best for: Building relationships
- Follow up: 7 days

**Thank You** → Post-interview
- Use when: After any formal/informal interview
- Best for: Showing appreciation
- Follow up: 14 days (or when they suggest)

## Example Workflow

### Week 1: Initial Outreach
1. Research 10 targets (mix of cold, alumni, referrals)
2. Create CSV with all targets
3. Batch generate all emails
4. Customize each with specific details
5. Send 2-3 per day (Tuesday-Thursday)
6. Track all in system

### Week 2: Follow-ups
1. Check pending follow-ups daily
2. Send follow-ups to non-responders
3. Use "Coffee Follow-up" template for responses
4. Continue new outreach (2-3 per day)

### Week 3+: Relationship Building
1. Use "Thank You" after all calls
2. Track response rates by bank/approach
3. Adjust strategy based on what works
4. Build pipeline of ongoing conversations

## Common Questions

**Q: How many variations should I generate?**
A: 2-3 is ideal. Pick the one that feels most natural.

**Q: Should I always customize?**
A: YES. At minimum, add a specific deal mention.

**Q: What's the best time to send?**
A: Tuesday-Thursday, 9-11 AM or 2-4 PM EST.

**Q: How often should I follow up?**
A: Once is enough. System suggests timing automatically.

**Q: What if I don't hear back?**
A: Normal! 20-30% response rate is good. Focus on quality.

## Next Steps

1. ✅ Run test: `python test_generator.py`
2. ✅ Generate your first email: `python main.py`
3. ✅ Read full README.md for advanced features
4. ✅ Customize templates in `templates/` folder
5. ✅ Track your progress and iterate

---

**You're ready!** Start with 5-10 high-quality, researched emails rather than 50 generic ones. Quality > Quantity.

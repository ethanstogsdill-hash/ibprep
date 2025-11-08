# Usage Examples

## Example 1: First Cold Outreach

### Scenario
You're a Penn junior targeting Goldman Sachs TMT. You found John Smith (Associate) on LinkedIn.

### Input
```
Template: Cold Outreach
Name: John Smith
Bank: Goldman Sachs
Group: TMT
Seniority: Associate
Relationship: Cold
Your Name: Jane Doe
Your School: University of Pennsylvania
Your Background: Junior studying Finance
Deal Mention: Microsoft-Activision acquisition
```

### Generated Email
```
Subject: Goldman Sachs TMT - Quick Question from University of Pennsylvania Student

Hi John,

My name is Jane Doe, and I'm a Junior studying Finance at University of Pennsylvania.
I'm reaching out because I'm deeply interested in TMT investment banking and have been
following Goldman Sachs's work in the space.

Goldman Sachs's execution on Microsoft-Activision acquisition really caught my attention,
and I'd love to learn more about your experience working in TMT. Would you have 15-20
minutes for a quick call sometime in the next couple of weeks?

I'm flexible with timing and happy to work around your schedule.

Thanks so much for considering!

Best,
Jane Doe
```

### Metrics
- Words: 96 (Ideal)
- Readability: Excellent
- Characters: 576

---

## Example 2: Alumni Connection

### Scenario
Reaching out to a Northwestern alum (Sarah Chen, VP at Morgan Stanley Healthcare).

### Input
```
Template: Alumni Connection
Name: Sarah Chen
Bank: Morgan Stanley
Group: Healthcare M&A
Seniority: VP
Relationship: Alumni
Your Name: Michael Johnson
Your School: Northwestern University
Your Background: Senior studying Economics
Deal Mention: Pfizer-Seagen acquisition
Mascot: Wildcats
```

### Generated Email
```
Subject: Fellow Northwestern Alum - Quick Question

Hi Sarah,

Go Wildcats! I'm Michael Johnson, a Senior studying Economics at Northwestern University,
and I came across your profile while researching Healthcare M&A banking.

I'm really interested in Healthcare M&A and have been following Morgan Stanley's work in
the space, especially Pfizer-Seagen acquisition. I'd love to hear about your experience
going from Northwestern to Healthcare M&A at Morgan Stanley.

Would you have 15-20 minutes for a quick call? Would be great to connect with a fellow alum!

Thanks so much,
Michael Johnson
```

---

## Example 3: Post-Coffee Chat Thank You

### Scenario
Following up after a great informational interview with an associate.

### Input
```
Template: Thank You
Name: David Lee
Bank: JP Morgan
Group: Leveraged Finance
Seniority: Associate
Your Name: Emma Wilson
Discussion Topic: the evolution of private credit markets
Specific Insight: how sponsors are increasingly working with multiple financing sources
Timeframe: yesterday
```

### Generated Email
```
Subject: Thank You - JP Morgan Conversation

Hi David,

I wanted to send a quick note to thank you for our conversation yesterday. I really
appreciated you taking the time to share your experiences in Leveraged Finance at
JP Morgan.

Your insights on the evolution of private credit markets were incredibly helpful, and
I left our conversation even more excited about Leveraged Finance. Your point about
how sponsors are increasingly working with multiple financing sources really resonated
with me.

Thanks again for your time and advice. I'll definitely stay in touch as things progress!

Best,
Emma Wilson
```

---

## Example 4: Referral-Based Introduction

### Scenario
Your mentor (Professor Mark Stevens) suggested you reach out to his former student.

### Input
```
Template: Referral
Name: Jennifer Park
Bank: Evercore
Group: Technology M&A
Seniority: Associate
Relationship: Referral
Your Name: Alex Kumar
Referrer Name: Professor Mark Stevens
Referrer Context: mentioned you were one of his top students and suggested I reach out
Deal Mention: Broadcom-VMware transaction
```

### Generated Email
```
Subject: Professor Mark Stevens Suggested I Reach Out

Hi Jennifer,

Professor Mark Stevens mentioned you were one of his top students and suggested I reach
out regarding my interest in Technology M&A at Evercore.

I'm a Junior studying Finance at University of Pennsylvania, and I've been particularly
drawn to Technology M&A banking. Professor Stevens mentioned that you'd be an excellent
person to speak with given your experience in Technology M&A and your work on deals like
Broadcom-VMware transaction.

Would you be available for a brief 15-20 minute call to discuss your experience at Evercore?
I'm flexible with timing and happy to work around your schedule.

Thank you for considering my request.

Best regards,
Alex Kumar
```

---

## Example 5: Coffee Chat Follow-up

### Scenario
Following up with an analyst you met at a networking event last week.

### Input
```
Template: Coffee Follow-up
Name: Ryan Martinez
Bank: Lazard
Group: Restructuring
Seniority: Analyst
Relationship: Warm
Your Name: Sophie Chen
Timeframe: last week at the finance networking event
Discussion Topic: the current restructuring pipeline
Specific Followup: learning more about the summer analyst program
Update On Your End: I've since spoken with two other Lazard analysts and am even more
excited about the restructuring group
```

### Generated Email
```
Subject: Following Up - Coffee Chat

Hi Ryan,

Thanks again for the great conversation last week at the finance networking event!
I really appreciated your perspective on the current restructuring pipeline and
learning more about your path in Restructuring.

I wanted to follow up on learning more about the summer analyst program. Also, I thought
you'd be interested to know that I've since spoken with two other Lazard analysts and am
even more excited about the restructuring group.

Would love to stay in touch as recruiting progresses. Thanks again for your time and insights!

Best,
Sophie Chen
```

---

## Batch Processing Example

### CSV File: `my_targets.csv`
```csv
name,bank,group,seniority,relationship,deal_mention,tone
John Smith,Goldman Sachs,TMT,Associate,Cold,Microsoft-Activision deal,warm
Sarah Chen,Morgan Stanley,Healthcare M&A,VP,Alumni,Pfizer-Seagen acquisition,warm
David Lee,JP Morgan,Leveraged Finance,Analyst,Referral,Vista Equity LBO,casual
Jennifer Park,Evercore,Technology M&A,Associate,Cold,Broadcom-VMware transaction,warm
Ryan Martinez,Lazard,Restructuring,Analyst,Warm,Bed Bath & Beyond restructuring,casual
```

### Command
```bash
python main.py
# Select option 2
# Enter filename: my_targets.csv
```

### Result
- 5 emails generated in `output/` directory
- Each person gets 1 customized email
- All added to tracking system automatically
- Files named: `John_Smith_cold_outreach.txt`, etc.

---

## Tracking Example

### After Sending 10 Emails

```bash
python main.py
# Select option 3 (View Tracking Stats)
```

### Output
```
TRACKING STATISTICS
================================================================================

Total Emails Sent: 10
Responses Received: 3
Response Rate: 30.0%
Pending Follow-ups: 5

--- By Bank ---
  Goldman Sachs: 3
  Morgan Stanley: 2
  JP Morgan: 2
  Evercore: 2
  Lazard: 1

--- By Email Type ---
  cold_outreach: 6
  alumni: 2
  referral: 2
```

---

## Tips Based on These Examples

### What Makes These Effective

1. **Specific Deal Mentions**: Each email references actual deals
2. **Appropriate Length**: All under 150 words
3. **Clear Ask**: 15-20 minute call (specific and reasonable)
4. **Personalization**: References relationship, background, interests
5. **Professional Tone**: Matches recipient seniority
6. **Strong Subject Lines**: Clear and attention-grabbing

### Common Mistakes to Avoid

❌ Too long (>200 words)
❌ Generic ("I'm interested in investment banking")
❌ No specific ask
❌ Wrong tone for seniority (too casual with MDs)
❌ No deal/research mentioned
❌ Asking for a job directly

### Success Metrics

- **Cold Outreach**: 15-25% response rate
- **Alumni**: 30-40% response rate
- **Referral**: 50-70% response rate
- **Follow-up**: 60-80% response rate

### Follow-up Strategy

If no response after recommended timeframe:
1. Send ONE follow-up
2. Keep it brief (3-4 sentences)
3. Add value (mention new deal, update on your end)
4. Don't be pushy
5. If still no response, move on gracefully

---

## Customization Tips

### For Each Example Above, Consider Adding:

**Cold Outreach**
- Specific mutual connection
- Recent article they wrote
- Conference you saw them at

**Alumni**
- Specific professor/class connection
- School club/activity overlap
- Recent school news

**Thank You**
- Specific action item from conversation
- Resource they recommended
- Introduction to someone else

**Referral**
- More context about referrer
- Why referrer thought you'd connect
- Specific question referrer suggested

**Follow-up**
- Progress update
- New relevant news
- Helpful resource

---

## Advanced: A/B Testing Subject Lines

Generate 3 variations and test which subject lines get best response:

**Version A**: School-focused
- "Northwestern Alum - Quick Question"
- Response rate: Track it!

**Version B**: Bank-focused
- "Exploring Healthcare M&A at Morgan Stanley"
- Response rate: Track it!

**Version C**: Direct
- "15-Minute Call About Your Path to MS?"
- Response rate: Track it!

Use tracking system to see what works for YOUR target audience.

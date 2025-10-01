# Top P Parameter Examples

## What is Top P (Nucleus Sampling)?

Top P controls the cumulative probability threshold for token selection. Instead of selecting from a fixed number of tokens (like Top K), Top P selects from the smallest set of tokens whose cumulative probability exceeds the threshold.

- **Lower top_p (0.1-0.5)**: More focused, conservative word selection
- **Higher top_p (0.8-1.0)**: More diverse, creative vocabulary choices

## Example Comparisons

### User Input:
- **Name**: Sarah Johnson
- **Skills**: Python, SQL, Excel
- **Target Role**: Data Scientist
- **Tone**: Professional

### Top P = 0.3 (Conservative)
**Resume Bullets:**
```json
{
  "resumeBullets": [
    "Analyzed data using Python and SQL to support business decisions",
    "Created reports with Excel to present findings to management",
    "Developed data models to identify trends and patterns in datasets"
  ],
  "skillGaps": [
    "Machine Learning",
    "Statistical Analysis",
    "Data Visualization"
  ]
}
```

**Characteristics:**
- Uses common, predictable vocabulary
- Straightforward, conventional phrasing
- Safe, standard industry terms

### Top P = 0.7 (Balanced)
**Resume Bullets:**
```json
{
  "resumeBullets": [
    "Leveraged Python and SQL to extract insights from complex datasets",
    "Designed comprehensive Excel reports to communicate analytical findings",
    "Built predictive models to uncover actionable business intelligence"
  ],
  "skillGaps": [
    "Advanced Machine Learning",
    "Statistical Modeling",
    "Tableau/Power BI"
  ]
}
```

**Characteristics:**
- Good balance of professional and engaging language
- More descriptive action words
- Industry-appropriate but varied vocabulary

### Top P = 0.9 (Creative)
**Resume Bullets:**
```json
{
  "resumeBullets": [
    "Orchestrated sophisticated data analysis workflows using Python and SQL",
    "Architected dynamic Excel dashboards to illuminate key performance metrics",
    "Engineered robust analytical frameworks to decode complex data narratives"
  ],
  "skillGaps": [
    "Deep Learning Frameworks",
    "Advanced Statistical Techniques",
    "Cloud-based Analytics Platforms"
  ]
}
```

**Characteristics:**
- More creative, varied vocabulary choices
- Sophisticated action verbs (orchestrated, architected, engineered)
- More elaborate descriptions and technical terminology

## Technical Explanation

### How Top P Works:
1. **Token Probability Ranking**: AI ranks all possible next tokens by probability
2. **Cumulative Probability**: Calculates running total of probabilities
3. **Threshold Selection**: Selects from tokens until cumulative probability exceeds top_p
4. **Dynamic Vocabulary**: Vocabulary size varies based on probability distribution

### Example Token Selection:

For the phrase "Developed web applications using..."

**Top P = 0.3 (30% probability mass):**
- Considers: "React" (15%), "JavaScript" (10%), "Python" (5%)
- Result: "Developed web applications using React"

**Top P = 0.9 (90% probability mass):**
- Considers: "React" (15%), "JavaScript" (10%), "Python" (5%), "Vue" (8%), "Angular" (7%), "Node.js" (6%), "Django" (4%), "Flask" (3%), "TypeScript" (12%), "modern" (9%), "cutting-edge" (2%), "innovative" (3%), "sophisticated" (1%)
- Result: "Developed web applications using cutting-edge frameworks"

## Best Practices

### When to Use Low Top P (0.1-0.4):
- Professional, formal documents
- Technical documentation
- Conservative industries (finance, healthcare, legal)
- When consistency is more important than creativity

### When to Use Medium Top P (0.5-0.8):
- General business communications
- Balanced professional content
- Most resume and cover letter applications
- When you want some variety but not too creative

### When to Use High Top P (0.8-1.0):
- Creative industries (marketing, design, media)
- Innovative technology companies
- When you want to stand out with unique phrasing
- Brainstorming and ideation sessions

## Testing Top P in the Application

Run the application and experiment with different top_p values:

```bash
python main.py
```

1. Choose the same user information
2. Try different top_p settings (Conservative, Balanced, Creative)
3. Compare the vocabulary and phrasing differences
4. Notice how higher top_p values produce more varied and creative language

## Combining with Other Parameters

Top P works best when combined with other parameters:

- **Temperature + Top P**: Temperature controls randomness, Top P controls vocabulary diversity
- **Top K + Top P**: Top K limits vocabulary size, Top P uses probability thresholds
- **Professional Tone + Low Top P**: Very conservative, predictable output
- **Creative Tone + High Top P**: Maximum creativity and vocabulary diversity

## Real-World Impact

Different top_p values can significantly impact how your resume is perceived:

- **Conservative (0.3)**: Safe for traditional industries, may seem generic
- **Balanced (0.7)**: Professional yet engaging, good for most applications
- **Creative (0.9)**: Stands out but may be too unconventional for some roles

Choose based on your target industry, company culture, and personal brand!
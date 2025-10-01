# Top K Parameter Examples

This document demonstrates how different top_k values affect output diversity in the AI Career Mentor application.

## What is Top K?

The top_k parameter controls vocabulary selection by limiting the AI to consider only the top K most likely tokens at each generation step.

- **Lower top_k (10-20)**: More focused, predictable vocabulary
- **Medium top_k (30-50)**: Balanced vocabulary selection  
- **Higher top_k (60-100)**: More diverse, creative word choices

## Implementation

The top_k parameter has been added to:

1. **`get_generation_config()`** function in `gemini_client.py`
2. **`call_gemini_api()`** function in `gemini_client.py`
3. **User input collection** in `main.py`
4. **Demonstration script** `top_k_demo.py`

## Usage Examples

### In Code

```python
from gemini_client import call_gemini_api

# Focused vocabulary (predictable)
response = call_gemini_api(
    system_prompt="You are a career mentor...",
    user_prompt="Help create resume bullets...",
    tone="professional",
    top_k=20
)

# Diverse vocabulary (creative)
response = call_gemini_api(
    system_prompt="You are a career mentor...",
    user_prompt="Help create resume bullets...",
    tone="creative", 
    top_k=80
)
```

### In Main Application

When running `python main.py`, users can now choose:

1. **Focused vocabulary (top_k=20)** - More predictable, common words
2. **Balanced vocabulary (top_k=40)** - Default Gemini setting
3. **Diverse vocabulary (top_k=80)** - More creative, varied word choices
4. **Skip (use default)** - Let Gemini use its default setting

## Example Output Differences

### Sample Input
- **Name**: Alex Johnson
- **Skills**: Python, SQL, Excel
- **Target Role**: Data Scientist
- **Tone**: Professional

### Low Top K (20) - Focused Vocabulary
```json
{
  "resumeBullets": [
    "Analyzed data using Python and SQL to support business decisions",
    "Developed reports using Excel to present findings to stakeholders", 
    "Applied statistical methods to identify trends in large datasets"
  ],
  "skillGaps": [
    "Machine Learning",
    "Data Visualization", 
    "Cloud Platforms"
  ]
}
```

### High Top K (80) - Diverse Vocabulary  
```json
{
  "resumeBullets": [
    "Leveraged Python and SQL to extract actionable insights from complex datasets",
    "Orchestrated comprehensive analytical reports utilizing Excel for executive presentations",
    "Implemented sophisticated statistical methodologies to uncover patterns in extensive data repositories"
  ],
  "skillGaps": [
    "Advanced Machine Learning Frameworks",
    "Interactive Data Visualization Tools",
    "Distributed Computing Platforms"
  ]
}
```

## Key Observations

1. **Vocabulary Richness**: Higher top_k values tend to use more sophisticated and varied vocabulary
2. **Consistency**: Lower top_k values produce more consistent, predictable language
3. **Professional Context**: Even with high top_k, professional tone keeps language appropriate
4. **Subtle Effects**: The impact may be subtle but becomes more apparent in longer texts

## Best Practices

### Recommended Combinations

- **Technical Documentation**: `temperature=0.3, top_k=20` (maximum consistency)
- **Professional Content**: `temperature=0.3, top_k=40` (balanced approach)  
- **Creative Content**: `temperature=0.8, top_k=80` (maximum creativity)
- **General Use**: `temperature=0.5, top_k=40` (versatile default)

### When to Use Different Values

- **Low top_k (10-30)**: 
  - Formal business communications
  - Technical specifications
  - Consistent brand voice
  
- **Medium top_k (30-60)**:
  - General content creation
  - Educational materials
  - Balanced creativity and consistency
  
- **High top_k (60-100)**:
  - Creative writing
  - Marketing copy
  - Varied content generation

## Testing the Implementation

### Run the Demo Script
```bash
python top_k_demo.py
```

This script will:
1. Generate resume bullets with different top_k values
2. Show vocabulary diversity analysis
3. Provide interactive testing capabilities
4. Explain the educational concepts

### Manual Testing in Main App
```bash
python main.py
```

Choose option 1, 2, or 3 when prompted for vocabulary diversity to see the effects in action.

## Technical Details

### Validation
- top_k values must be integers between 1-100
- Invalid values trigger a warning and fall back to default
- None/null values use Gemini's default setting

### Error Handling
- Invalid top_k values are gracefully handled
- Warning messages guide users to correct values
- System continues with default settings on invalid input

### Integration
- Seamlessly integrated with existing temperature control
- Compatible with all existing functionality
- No breaking changes to existing API calls
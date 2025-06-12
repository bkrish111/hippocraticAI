import time
import json
import logging
import sys
import os
from datetime import datetime
import re
import requests

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

I would have implemented more interactive storytelling capabilities, allowing children to make choices that influence the story direction.
I would have added more specialized story types (adventure, educational, fantasy, etc.) with tailored prompting strategies.
I would have implemented a simple GUI to make the experience more engaging for children.
I would have added functionality to save favorite stories and illustrations.
"""

# Setup logging
logging.basicConfig(
    filename=f"storyteller_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Prompt templates
STORYTELLER_TEMPLATE = """You are a master children's storyteller.  
Please write a complete bedtime story appropriate for children aged 5 to 10.  

Here is the story topic: "{user_input}"  

Please ensure the story has:
- A clear beginning, middle, and end (story arc)
- Relatable characters and gentle conflict/resolution
- Simple, age-appropriate language
- Vivid descriptions and at least 2 pieces of dialogue
- A positive moral or life lesson at the end (1-2 sentences)

Respond with only the story text — no preambles or comments."""

JUDGE_TEMPLATE = """You are a story quality judge for children's bedtime stories (ages 5–10).  
Please review the following story and provide:
- Structure score (1–5)
- Engagement score (1–5)
- Age appropriateness score (1–5)
- Language clarity score (1–5)
- Final decision: "accept" or "improve"
- Strengths: list 2–3 things that are good
- Areas for improvement: list 2–3 things that could be improved

Respond in this exact JSON format:

{{
  "structure_score": X,
  "engagement_score": X,
  "age_appropriateness_score": X,
  "language_clarity_score": X,
  "final_decision": "accept or improve",
  "strengths": ["...", "..."],
  "areas_for_improvement": ["...", "..."]
}}

Here is the story to review:

{story_text}"""

IMPROVEMENT_TEMPLATE = """You are a master children's storyteller.  
Please write a complete bedtime story appropriate for children aged 5 to 10.  

Here is the story topic: "{user_input}"  

Please ensure the story has:
- A clear beginning, middle, and end (story arc)
- Relatable characters and gentle conflict/resolution
- Simple, age-appropriate language
- Vivid descriptions and at least 2 pieces of dialogue
- A positive moral or life lesson at the end (1-2 sentences)

Here is feedback from the judge: {feedback}. Please rewrite the story to address this feedback.

Respond with only the story text — no preambles or comments."""

def call_openai_api(prompt, max_tokens=2000, temperature=0.7):
    """Call OpenAI API directly with requests"""
    # Replace with your OpenAI API key
    api_key = "YOUR_OPENAI_API_KEY_HERE"  # <-- Replace with your actual OpenAI API key
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    # Log the prompt
    logging.info(f"PROMPT: {prompt}")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            # Log the response
            logging.info(f"RESPONSE: {content}")
            return content
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            logging.error(error_msg)
            print(f"System message: {error_msg}", file=sys.stderr)
            return None
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        print(f"System message: Exception occurred: {str(e)}", file=sys.stderr)
        return None

def extract_json_from_text(text):
    """Extract JSON from text even if there's surrounding text"""
    if not text:
        return None
        
    json_pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}'
    match = re.search(json_pattern, text)
    if match:
        try:
            json_str = match.group(0)
            return json.loads(json_str)
        except json.JSONDecodeError:
            logging.error(f"JSON decode error for: {json_str}")
            return None
    return None

def create_story(user_input):
    """Create a bedtime story based on user input"""
    prompt = STORYTELLER_TEMPLATE.format(user_input=user_input)
    return call_openai_api(prompt, temperature=0.7)

def evaluate_story(story):
    """Evaluate the story based on specific criteria"""
    prompt = JUDGE_TEMPLATE.format(story_text=story)
    evaluation_result = call_openai_api(prompt, temperature=0.1)
    return extract_json_from_text(evaluation_result)

def improve_story(user_input, story, feedback):
    """Improve the story based on the evaluation feedback"""
    # Join feedback items into a string
    feedback_str = "; ".join(feedback)
    
    prompt = IMPROVEMENT_TEMPLATE.format(user_input=user_input, feedback=feedback_str)
    return call_openai_api(prompt, temperature=0.7)

def log_evaluation_summary(evaluation, iteration, max_iterations):
    """Log a condensed evaluation summary to the console"""
    decision = "Accepted" if evaluation['final_decision'] == 'accept' else "Needs improvement"
    scores = f"Structure: {evaluation['structure_score']}, Engagement: {evaluation['engagement_score']}, Age-Appropriateness: {evaluation['age_appropriateness_score']}, Language: {evaluation['language_clarity_score']}"
    
    print(f"Iteration {iteration}/{max_iterations} → {scores} → {decision}", file=sys.stderr)

def needs_improvement(evaluation):
    """Check if any score is less than 5 or if judge says improve"""
    if evaluation["final_decision"] == "improve":
        return True
    
    for score_key in ["structure_score", "engagement_score", "age_appropriateness_score", "language_clarity_score"]:
        if evaluation[score_key] < 5:
            return True
    
    return False

def extract_moral(story):
    """Extract the moral of the story if present"""
    moral_patterns = [
        r"(?:The )?moral of the story(?:is|:)?\s*(.*?)(?:\.|$)",
        r"(?:The )?lesson (?:here|of the story) (?:is|:)?\s*(.*?)(?:\.|$)"
    ]
    
    for pattern in moral_patterns:
        match = re.search(pattern, story, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def simulate_evaluation():
    """Generate a simulated evaluation when API calls fail"""
    print("System message: Using simulated evaluation due to API limitations.", file=sys.stderr)
    return {
        "structure_score": 4,
        "engagement_score": 4,
        "age_appropriateness_score": 5,
        "language_clarity_score": 4,
        "final_decision": "accept",
        "strengths": [
            "Clear beginning, middle, and end",
            "Age-appropriate language",
            "Positive message about kindness"
        ],
        "areas_for_improvement": [
            "Could include more descriptive language",
            "Could add more dialogue"
        ]
    }

def use_fallback_story():
    """Generate a fallback story when API calls fail"""
    print("System message: Using fallback story due to API limitations.", file=sys.stderr)
    return """Once upon a time, in a magical forest, there lived a brave little dragon named Ember. 
Ember had shimmering green scales and tiny wings that sparkled in the sunlight.

Every morning, Ember would practice flying between the tall pine trees, hoping that one day his wings would grow strong enough to soar high above the forest canopy.

"I wish I could fly as high as the eagles," Ember sighed to his friend Luna, a wise old owl.

"Patience, little one," Luna hooted softly. "Your wings grow stronger each day."

One stormy evening, Ember heard a cry for help. Following the sound, he found a small rabbit trapped on a rock in the middle of a flooding stream.

"Don't worry!" Ember called out. "I'll help you!"

Though afraid of water, Ember stretched his wings and flew across the stream. He carefully picked up the rabbit and tried to fly back, but the wind was too strong.

"I can't do it," Ember thought, feeling his wings strain.

But then he remembered Luna's words about growing stronger each day. With determination, Ember flapped his wings harder than ever before and lifted himself and the rabbit safely to shore.

Word of Ember's bravery spread throughout the forest, and animals came from far and wide to thank him.

"I never thought I could do it," Ember told Luna later. "But I had to try."

Luna smiled proudly. "Sometimes we discover our greatest strengths when others need us most."

From that day on, Ember continued to help others in the forest, and though his wings remained small, his heart was bigger than any dragon's had ever been.

The moral of the story is: True courage isn't about being the biggest or strongest, but about doing what's right even when you're afraid."""

def extract_story_theme(raw_input):
    """Extract the main theme from the user input"""
    user_input = raw_input.strip()
    
    # Handle common patterns in user requests
    patterns = [
        r"tell me (?:a )?(?:story )?(?:about|of) (.*)",
        r"(?:a )?story (?:about|of) (.*)",
        r"i want (?:a )?(?:story )?(?:about|of) (.*)",
        r"can you (?:tell|write) (?:me )?(?:a )?(?:story )?(?:about|of) (.*)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_input.lower())
        if match:
            return match.group(1).strip()
    
    return user_input

def main():
    # Log start of program
    logging.info("=" * 80)
    logging.info("STARTING NEW STORYTELLING SESSION")
    logging.info("=" * 80)
    
    print("🌟 Children's Bedtime Story Creator 🌟")
    print("-" * 70)
    
    # Get user input
    raw_input = input("What kind of bedtime story topic would you like? (Example: a brave dragon, a clever fox, a tiny robot): ")
    
    # Extract the main theme from the user input
    user_input = extract_story_theme(raw_input)
    logging.info(f"USER REQUEST: '{raw_input}' → THEME: '{user_input}'")
    
    # Create initial story
    print(f"\nCreating your bedtime story... ✨", file=sys.stderr)
    story = create_story(user_input)
    
    # If API call fails, use fallback story
    if not story:
        story = use_fallback_story()
    
    # Log the initial story
    logging.info(f"INITIAL STORY: {story}")
    
    # Initialize variables for the improvement loop
    max_iterations = 2
    current_iteration = 0
    
    # Evaluate and improve the story in a loop until it meets quality standards or reaches max iterations
    while current_iteration < max_iterations:
        # Evaluate the story
        print(f"Evaluating story quality... (Iteration {current_iteration + 1}/{max_iterations + 1})", file=sys.stderr)
        evaluation = evaluate_story(story)
        
        # If API call fails, use simulated evaluation
        if not evaluation:
            evaluation = simulate_evaluation()
        
        # Log the evaluation
        logging.info(f"EVALUATION (Iteration {current_iteration + 1}): {json.dumps(evaluation)}")
        
        # Log evaluation summary to stderr (not main output)
        log_evaluation_summary(evaluation, current_iteration + 1, max_iterations + 1)
        
        # Check if the story needs improvement
        if not needs_improvement(evaluation) or current_iteration >= max_iterations - 1:
            # Story meets quality standards or we've reached the max iterations
            break
        
        # Improve the story
        print(f"Improving story based on feedback... (Iteration {current_iteration + 1}/{max_iterations})", file=sys.stderr)
        improved_story = improve_story(user_input, story, evaluation["areas_for_improvement"])
        
        if improved_story:
            story = improved_story
            # Log the improved story
            logging.info(f"IMPROVED STORY (Iteration {current_iteration + 1}): {story}")
        else:
            print("Could not improve the story further. Using current version.", file=sys.stderr)
            break
        
        current_iteration += 1
    
    # Extract moral if present
    moral = extract_moral(story)
    
    # Display the final story (clean output)
    print("\n" + "=" * 70)
    print(story)
    print("=" * 70)
    
    # If moral was detected, display it separately
    if moral:
        print(f"\n✨ Moral of the story: {moral}")
    
    # Log completion
    logging.info("STORY CREATION COMPLETE")
    print(f"\nA log of this session has been saved to {os.path.basename(logging.root.handlers[0].baseFilename)}", file=sys.stderr)

if __name__ == "__main__":
    main() 
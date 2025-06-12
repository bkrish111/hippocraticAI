# AI Bedtime Story Generator

## Project Summary

This project implements an AI agent system for generating high-quality children's bedtime stories for ages 5-10. The system uses a self-improving approach with multiple AI agents working together:

1. **Storyteller Agent**: Creates engaging, age-appropriate bedtime stories based on user-provided topics
2. **Judge Agent**: Evaluates stories on structure, engagement, age-appropriateness, and language clarity
3. **Improvement Agent**: Refines stories based on specific feedback until quality standards are met

The system ensures stories have clear structure, relatable characters, appropriate language, and a positive moral lesson. It implements an iterative improvement loop to enhance story quality, with all prompts and results carefully logged for transparency.

## System Architecture

```
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│               │       │               │       │               │
│   User Input  │──────>│  Storyteller  │──────>│  Story Output │
│               │       │      LLM      │       │               │
└───────────────┘       └───────────────┘       └───────┬───────┘
                                                        │
                                                        ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│               │       │               │       │               │
│  Final Story  │<──────│ Accept/Improve│<──────│  Judge LLM    │
│               │       │   Decision    │       │               │
└───────────────┘       └───────┬───────┘       └───────────────┘
                                │
                                │ If "Improve"
                                ▼
                        ┌───────────────┐
                        │               │
                        │ Improvement   │
                        │     LLM       │
                        │               │
                        └───────┬───────┘
                                │
                                │ Improved Story
                                │
                                └───────────> (Back to Storyteller)
```

## Features

- Generates age-appropriate stories based on user-provided topics
- Evaluates stories on multiple quality criteria
- Iteratively improves stories based on specific feedback
- Extracts and highlights the moral of the story
- Comprehensive logging of all prompts and responses
- Clean, user-friendly interface

## Example Scenario

### User Input
```
What kind of bedtime story topic would you like? (Example: a brave dragon, a clever fox, a tiny robot): a shy turtle who makes friends
```

### System Process (Behind the Scenes)
1. **Storyteller Agent** creates an initial story about a shy turtle
2. **Judge Agent** evaluates the story:
   - Structure: 4/5
   - Engagement: 3/5
   - Age-Appropriateness: 5/5
   - Language: 4/5
   - Decision: Needs improvement
   - Areas for improvement: "More engaging dialogue needed", "Story could use more descriptive language"
3. **Improvement Agent** enhances the story based on feedback
4. **Judge Agent** re-evaluates:
   - Structure: 5/5
   - Engagement: 4/5
   - Age-Appropriateness: 5/5
   - Language: 5/5
   - Decision: Accept

### Final Output
```
======================================================================
THE SHELL THAT SHINED

Once upon a time, in a crystal-clear pond surrounded by tall reeds and colorful water lilies, lived a small turtle named Timmy. Timmy had a beautiful green shell with unique yellow patterns, but whenever other pond creatures swam near, he would quickly tuck his head and legs inside his shell.

"I wish I could talk to others without feeling so scared," Timmy whispered to himself one sunny morning as he watched a group of frogs leaping from lily pad to lily pad, laughing together.

Each day, Timmy would swim to the shallow end of the pond and practice saying "hello," hoping that someday he would be brave enough to say it to someone else.

One cloudy afternoon, while Timmy was nibbling on some tender water plants, he heard a soft sniffling sound. Looking around, he spotted a tiny blue fish hiding behind a rock.

"Are you okay?" Timmy asked, surprising himself by speaking first.

The little fish looked up with wide, tearful eyes. "I'm lost! I can't find my family, and I'm scared of the big fish."

Timmy felt a flutter in his heart. Here was someone who felt scared too! "I know a safe place with lots of plants to hide in," he said, his voice growing steadier. "I could show you, if you'd like."

"You would do that for me?" asked the fish, her fins perking up slightly. "My name is Finn."

"I'm Timmy," the turtle replied with a small smile. "And yes, I would."

As they swam together, Timmy pointed out the safest routes and the best hiding spots. "I've spent a lot of time watching and learning about the pond," he explained, "since I was too shy to join in with others."

"Being observant is a wonderful quality," Finn said. "You notice things others might miss."

By the time they found Finn's family in a cozy corner of the pond, Timmy had forgotten about hiding in his shell. Finn's family was so grateful that they invited Timmy to join them for dinner.

"Thank you for helping my daughter," Finn's mother said warmly. "You're welcome to visit us anytime."

The next day, Timmy was surprised when Finn returned with a friendly-looking turtle.

"This is my friend, Tommy," Finn announced proudly. "I told him how you helped me, and he wanted to meet you!"

Tommy smiled. "I've seen you around the pond, but you always seemed to disappear before I could say hello."

Timmy felt his old shyness threatening to return, but he remembered how good it felt to help Finn. "I've been a bit shy," he admitted. "But I'm learning that making friends isn't as scary as I thought."

As the days passed, Timmy met more and more pond creatures. He still felt shy sometimes, but he discovered that everyone had their own worries and fears. Some of the loudest frogs admitted they were afraid of leaving the pond, and even the graceful dragonflies confessed they sometimes felt clumsy.

"Your shell isn't just for hiding," Tommy told him one day as they basked in the sun. "It's also what makes you special and unique."

Timmy looked at his reflection in the water, noticing how his shell caught the sunlight and created beautiful patterns on the pond's surface. "I guess we all have our own kind of shell," he said thoughtfully. "And that's okay."

From that day on, Timmy still tucked into his shell sometimes when he needed quiet moments alone, but he also learned to poke his head out and say "hello" – because he discovered that friendship was worth being brave for.

The moral of the story is: Being shy is nothing to be ashamed of, and taking small, brave steps can lead to wonderful friendships.
======================================================================

✨ Moral of the story: Being shy is nothing to be ashamed of, and taking small, brave steps can lead to wonderful friendships.
```

## Usage

1. Run `python main.py`
2. Enter a bedtime story topic when prompted
3. The system will generate, evaluate, and if necessary, improve the story
4. The final story and its moral will be displayed

## Implementation Details

The system implements three key LLM agents:

1. **Storyteller**: Creates stories with clear beginning/middle/end, relatable characters, appropriate language, vivid descriptions, dialogue, and a moral lesson
2. **Judge**: Evaluates on structure, engagement, age-appropriateness, and language clarity, providing specific strengths and areas for improvement
3. **Improver**: Refines stories based on judge feedback while maintaining the original theme

All processing occurs in the background, with only the final polished story presented to the user for a clean experience. 

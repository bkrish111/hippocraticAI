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
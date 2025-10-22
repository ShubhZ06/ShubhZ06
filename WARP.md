# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a GitHub profile README template repository. It contains a customizable profile template (`README.md`) with dynamic widgets, badges, and stats for creating a professional GitHub profile page.

## Repository Structure

- `README.md` - The main profile template with placeholders to be customized
- `SETUP.md` - Complete setup and customization instructions
- `.gitignore` - Standard ignore patterns for OS files, editor configs, and temporary files

## Key Customization Points

When editing `README.md`, these are the primary placeholders that need replacement:

### User-Specific Values
- `[Your Name]` - User's full name (line 1)
- `YOUR_USERNAME` - GitHub username (appears on lines 67, 69, 71, 81, 97, 98, 119-121, 129, 131)
- `[Your Current Project]` - Current work (line 15)
- `[Technologies you're learning]` - Learning goals (line 16)
- `[Your expertise areas]` - Areas of expertise (line 18)
- `[your.email@example.com]` - Email address (lines 19, 121)
- `[Something interesting about you]` - Fun fact (line 20)
- `YOUR_PROFILE` - LinkedIn username (line 118)
- `YOUR_HANDLE` - Twitter handle (line 119)
- `REPO_NAME` - Featured repository names (lines 97-98)

### Dynamic Components

The profile uses external services that auto-generate content:
- **GitHub Stats API** (`github-readme-stats.vercel.app`) - Stats, language charts, repo cards
- **Streak Stats** (`github-readme-streak-stats.herokuapp.com`) - Contribution streaks
- **Trophy** (`github-profile-trophy.vercel.app`) - Achievement trophies
- **Activity Graph** (`github-readme-activity-graph.vercel.app`) - Contribution graphs
- **Typing SVG** (`readme-typing-svg.herokuapp.com`) - Animated typing effect
- **Profile Views** (`komarev.com/ghpvc`) - View counter

### Theme Consistency

All widgets currently use the `tokyonight` theme. When customizing, maintain consistent theming across all components or coordinate theme changes.

## Commands

### Git Workflow
```powershell
# Push changes to GitHub
git add .
git commit -m "Update profile"
git push origin main
```

### View Profile
After pushing to a repository named after the GitHub username (ShubhZ06), the profile appears at:
- https://github.com/ShubhZ06

## Working with This Repository

### Adding New Badges
Find badge formats at https://shields.io/ and https://simpleicons.org/

### Modifying the Typing Animation
Edit line 5 URL parameters, separating phrases with semicolons and using `+` for spaces

### Content Sections
The README is organized into these sections:
1. Header with animated typing
2. About Me
3. Tech Stack (Languages, Frontend, Backend, Database, DevOps)
4. GitHub Statistics
5. GitHub Trophies
6. Contribution Graph
7. Featured Projects
8. Latest Blog Posts (requires workflow automation)
9. Social Links
10. Footer

### Adding Blog Post Automation
Requires GitHub Actions workflow setup (see SETUP.md lines 66-69)

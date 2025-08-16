# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This is a static website hosted on GitHub Pages. No build process is required.

- To develop locally, simply open `index.html` in a browser
- To deploy, push changes to the main branch

## Code Architecture

The website uses a client-side rendering approach with JavaScript to dynamically load content:

- Configuration is stored in YAML format in `contents/config.yml`
- Content is written in Markdown format in `contents/*.md` files
- The main page `index.html` loads Bootstrap, MathJax, and custom JavaScript
- `scripts.js` dynamically fetches the YAML configuration and Markdown content files, then renders them into the page using marked.js for Markdown parsing and MathJax for LaTeX rendering
- CSS styles are located in `static/css/` directory
- JavaScript libraries and custom scripts are in `static/js/` directory
- Images and other assets are stored in `static/assets/` directory
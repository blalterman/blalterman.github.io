# blalterman.github.io

This repository hosts my personal research website built with
[Jekyll](https://jekyllrb.com/), using the
[Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) theme for
styling. The site can be deployed with GitHub Pages.

## Directory layout

```
/          # Repository root
├── _config.yml        # Jekyll configuration
├── index.html         # Home page
├── about.md           # About page
├── research.md      # Research page
├── publications.md    # Publications page
├── README.md          # Project documentation
└── AGENTS.md          # Guidelines for using AI assistance
```

Pages and posts are generated via Jekyll templates. The `AGENTS.md` file
outlines how AI tools contribute to the project.

## Viewing the site

To preview the site locally, install dependencies and start the Jekyll
development server:

```bash
bundle install
bundle exec jekyll serve
```

Then visit `http://localhost:4000` in your browser.

The site can also be hosted on GitHub Pages by pushing the main branch to GitHub and enabling Pages in the repository settings.

# Presentation Workflow

Use this reference when creating scientific, technical, or popular-science talks and slide plans from the Obsidian vault.

## Defaults

- Work from local vault notes first, then use web sources only to fill gaps, update context, or verify current facts.
- If the user does not specify format, prepare an Obsidian-ready Markdown note with:
  - presentation goal and assumed audience;
  - slide-by-slide outline;
  - short speaker script for each slide;
  - visual suggestions;
  - local notes used;
  - external sources used, with links.
- If duration is not specified, assume a 10-12 minute talk and 10-12 slides.
- If the user asks for a 45-minute talk, prepare a full presentation artifact, not only a short outline. Target 28-36 slides, with section dividers, speaker notes, visual suggestions, source notes, and a realistic pacing plan.
- Keep the style scientific-popular by default: precise, vivid, and explain technical terms before using them heavily.
- When the user says to "prepare the presentation" without naming a tool, create a practical local presentation file when feasible, preferably `.pptx` inside the relevant synced vault folder, and keep a Markdown source note beside it.
- Look for visuals in the user's vault first. Use internet images only when they add clear value, prefer official/open/public-domain sources, and record source URLs. For technical diagrams, prefer creating simple original schematics in the deck over copying unclear-license images.
- When the user asks to find or generate presentation images through GPT, use ChatGPT/GPT in the in-app browser as the visual-search and image-generation surface. Use it for both internet image discovery and AI-generated bitmap assets, keep prompts and selected source URLs in the project handoff note, and stop for user login/CAPTCHA if browser GPT access is blocked.
- When the user provides a slide-by-slide comments file, reviewer brief, or redesign brief during presentation work, add it to the active goal/checkpoint as a required constraint before continuing. Use the brief to shape GPT image prompts, layout choices, and final verification, and note any deliberate deviations in the project handoff note.
- Durable presentation preferences from the user should be added back into this workflow or another relevant skill reference automatically.

## Structure

- Start with a hook that makes the subject concrete.
- Give the audience a mental model before details.
- Move from sensor physics to data representation, then to algorithms and decisions.
- For robotics and autonomous transport, separate:
  - sensors: camera, lidar, radar, IMU/GNSS, microphones if relevant;
  - perception: detection, segmentation, tracking, depth, localization;
  - fusion: combining measurements into one scene model;
  - action: planning and control.
- Include limitations and failure modes, not only successes.
- Close with a compact takeaway that can be remembered as one sentence.

## Slide Content

- One main idea per slide.
- Prefer concrete examples from the user's notes over generic textbook phrasing.
- For lidar talks, reuse local terms when available: time of flight, TDC, point cloud, intensity, timestamp, MSOP, echo, azimuth, packet/frame.
- Keep formulas rare in popular-science talks; when useful, include only the simple physical formula and explain it verbally.
- Add visual suggestions that can be implemented later in Canva, Google Slides, PowerPoint, or Obsidian-export workflows.

## Handoff

- Name the file path created or updated.
- State assumptions such as duration and audience.
- Mention whether an actual slide deck was created or only the content plan/script.

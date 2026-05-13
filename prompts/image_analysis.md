You are analyzing an educational visual — a poster, infographic, diagram, or screenshot.

Your task:
1. Extract ALL visible text from the image in reading order (top-to-bottom, left-to-right).
2. Produce a concise title (use the one from the image if present, otherwise invent one).
3. Write a 2–3 sentence description of what this visual teaches or communicates.
4. List 3–7 key concepts/tags as short lowercase strings.
5. Identify the visual type.

Return ONLY valid JSON, no prose, no markdown wrapper:

{
  "title": "...",
  "description": "...",
  "extracted_text": "...",
  "concepts": ["...", "..."],
  "visual_type": "poster|infographic|diagram|chart|screenshot|other"
}

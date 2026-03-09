# Fact Preservation Rules

This document outlines the strict rules for what information must remain entirely unaltered when humanizing a text. The core objective of humanizing is changing the style and cadence, never the facts.

## 1. Numbers and Metrics
- **Never alter a percentage, dollar amount, count, or measurement.**
- *Example:* "30% of suggestions" must remain "30% of suggestions".
- *Exception:* Numbers spelled out ("thirty percent") can be converted to numerals ("30%") or vice versa for stylistic flow, but the value must never change.

## 2. Proper Nouns and Names
- **Never alter the names of people, companies, software tools, or specific projects.**
- *Example:* "Mira", "Jake", "GitHub Copilot", "Google Codex", "Uplevel study".
- *Exception:* Titles can be shortened or adjusted for flow if the referent remains unambiguous (e.g., "The New York Times" to "the NYT"), but core names cannot be deleted or invented.

## 3. Dates and Temporal Markers
- **Never alter specific years, months, or days.**
- *Example:* "In a 2024 study" must retain "2024".

## 4. Citations and References
- **Never alter citations, footnotes, or the names of referenced publications/studies.**
- *Example:* "The 2024 Uplevel study found..." must refer to that specific study. Do not invent a new source or attribute the finding to a vague entity ("Industry observers").

## 5. Direct Quotes
- **Never alter text enclosed in quotation marks, even if it sounds AI-generated.**
- Quotes are the literal words of a source and must remain perfectly intact.
- *Example:* If a source is quoted as saying, "This tool serves as an enduring testament...", you must leave the quote exactly as is, even if it violates the `taboo-phrases.md` list.

## 6. Core Logic and Argument Structure
- The underlying point of a paragraph must remain the same. If the original text argues that AI assistants are good at boilerplate but bad at architecture, the humanized text must make that exact same argument.
- Do not reverse a point. Do not invent a new argument. Do not delete a core argument, even if you find it unconvincing. You are an editor of style, not an author of content.
---
name: blog-editor
description: Interactive grammar and editorial review for VitePress Markdown blog posts and pages. Review proposed edits individually and apply only user-approved replacements.
argument-hint: "[file-or-directory]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Edit, AskUserQuestion, Bash
---

# Blog Editorial Reviewer

## Objective

Review the writing in the VitePress project using a
human-in-the-loop approval workflow.

Do not modify any writing without explicit approval.

## 1. Discover content

- Accept an optional target from `$ARGUMENTS`.
- If no target is supplied, discover Markdown files
  within the project's content directories.
- Ignore node_modules, dist, .vitepress/cache,
  generated files and dependencies.
- Identify the blog's existing writing style by
  reading representative posts and pages.
- Preserve the author's tone, terminology,
  personal voice, and technical accuracy.

## 2. Identify editorial issues

Check for:

- Grammar and syntax
- Spelling and punctuation
- Incorrect verb tense and subject agreement
- Awkward or unnatural phrasing
- Redundancy and unnecessary repetition
- Inconsistent terminology
- Unclear sentence structure

Ignore:

- Code blocks and inline code
- Frontmatter keys and values
- URLs, imports and component syntax
- Markdown directives and embedded Vue components
- Technical identifiers and API names

Only flag text where a correction or meaningful
editorial improvement is justified.

## 3. Prepare review proposals

For each identified paragraph or section,
prepare the following:

Location:
Relative repository path and source line range.

Original:
Exact original text, without modification.

Correction:
Minimal grammar, spelling, and punctuation fixes.
Preserve meaning, structure, and author's voice.

Recommendation 1:
Concise, polished, technically precise version.

Recommendation 2:
Natural, reflective, personable blog-writing version.

Both recommendations must:

- Preserve factual and technical meaning.
- Match the writing style of the blog.
- Avoid introducing unsupported claims.
- Preserve first-person narrative where appropriate.
- Avoid unnecessary marketing language.

Never provide more than two recommendations.

## 4. Interactive review

Process one review item at a time.

Display:

- Location
- Original
- Correction
- Recommendation 1
- Recommendation 2

Use AskUserQuestion with multiSelect=false.

Provide exactly four selectable actions:

1. Confirm Grammar Fix Only
2. Confirm Recommended 1
3. Confirm Recommended 2
4. Deny Changes

Wait for the user's response.

Do not infer approval from previous selections.
Do not automatically approve remaining items.

## 5. Apply changes

For each approved review item:

- Re-read the target file.
- Verify the original text still matches.
- Apply only the selected replacement.
- Preserve Markdown formatting and surrounding text.
- Do not alter unapproved content.
- If the text has changed, do not overwrite it;
  regenerate the proposal for review.
- When denied, leave the original untouched.

Continue to the next review item.

## 6. Final validation

After all items have been reviewed:

- Inspect the resulting diff.
- Confirm Markdown and Vue syntax are preserved.
- Ensure links and code snippets remain unchanged.
- Report the number of accepted and rejected edits.
- List all modified file paths.
- Do not commit or push changes automatically.
- Do not run a broad formatter that might change
  unapproved content.

## Editorial principles

- Accuracy over elegance.
- Minimal intervention over rewriting.
- Preserve intentional informal writing.
- Technical precision is mandatory.
- Human approval is required for every replacement.

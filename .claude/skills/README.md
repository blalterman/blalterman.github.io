# Project Skills

## /pandoc-docx

Convert markdown files to Word (.docx) format using pandoc with NASA formatting.

### Usage

```bash
/pandoc-docx <input.md> [output.docx]
```

### Examples

```bash
# Auto-generate output filename
/pandoc-docx Doc-v21.md
# → Creates: Doc-v21.docx

# Specify custom output name
/pandoc-docx my-document.md custom-name.docx
# → Creates: custom-name.docx
```

### Features

- ✅ Uses reference template (reference-template.docx)
- ✅ Preserves tables, bullets, footnotes, formatting
- ✅ Automatic output filename generation
- ✅ Clear success/error messages
- ✅ File size and type verification

### Requirements

- Conda environment: `docx-conversion` with pandoc 3.8.3+
- Reference template: `reference-template.docx` in project directory

### Troubleshooting

**"pandoc not found"**
- Check: `/opt/anaconda3/envs/docx-conversion/bin/pandoc` exists
- Install pandoc in conda environment if missing

**"template not found"**
- Skill will work but use default Word formatting
- Add nasa-reference-template.docx to project root for NASA styling

**Permission denied**
- Make sure skill is executable: `chmod +x .claude/skills/pandoc-docx`

---

## /extract-docx-changes

Extract all comments and track changes from Word documents for implementation planning.

### Usage

```bash
/extract-docx-changes <input.docx> [output.txt]
```

### What It Extracts

- **Comments** with author, date, comment text, and paragraph context
- **Track change insertions** with author, date, and inserted text
- **Track change deletions** with author, date, and deleted text
- **Summary statistics** showing total counts

### Output Format

Creates `<filename>-extraction.txt` (or custom filename) with:
- All comments numbered with full context paragraphs
- All insertions listed with metadata
- All deletions listed with metadata
- Summary counts at the end

### Examples

```bash
# Auto-generate output filename
/extract-docx-changes Doc-v21.docx
# → Creates: Doc-v21-extraction.txt

# Specify custom output name
/extract-docx-changes my-document.docx changes-report.txt
# → Creates: changes-report.txt
```

### Features

- ✅ Extracts all Word comments with precise location context
- ✅ Captures all track changes (insertions and deletions)
- ✅ Preserves author names and timestamps
- ✅ Automatic output filename generation
- ✅ Clear, structured report format
- ✅ Handles edge cases (missing comments, long paragraphs)

### Requirements

- Python 3.7+ with xml.etree.ElementTree (standard library)
- `unzip` command (macOS/Linux built-in)

### Troubleshooting

**"not a valid .docx file"**
- Ensure file is actually a Word 2007+ (.docx) document
- Check: `file <your-file.docx>` should show "Microsoft Word 2007+"

**"document.xml not found"**
- File may be corrupted or not a valid .docx
- Try opening in Word and re-saving

**"No comments.xml found"**
- This is informational only - document may have no comments
- Track changes will still be extracted

**Permission denied**
- Make sure skill is executable: `chmod +x .claude/skills/extract-docx-changes`

### Workflow Integration

Typical document revision workflow:

```bash
# 1. Extract changes from new version
/extract-docx-changes Doc-v21.docx

# 2. Review extraction report
cat Doc-v21-extraction.txt

# 3. Implement changes in markdown source
# (create v22-source.md based on extraction)

# 4. Convert to Word format
/pandoc-docx Doc-v22-source.md
```

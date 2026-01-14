#!/usr/bin/env python3
"""
Extract all comments and track changes from Word documents with precise locations.
Based on proven extraction methodology from v19→v20 workflow.
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
import sys
import os
from pathlib import Path


# Define Word XML namespaces
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def extract_text(element, ns):
    """
    Extract all text from an XML element and its children.

    Args:
        element: XML element to extract text from
        ns: Namespace dictionary

    Returns:
        str: Concatenated text content
    """
    texts = []
    for text_elem in element.findall('.//w:t', ns):
        if text_elem.text:
            texts.append(text_elem.text)
    return ''.join(texts)


def extract_comments(comments_xml_path, document_xml_path):
    """
    Extract all comments with author, date, text, and paragraph context.

    Args:
        comments_xml_path: Path to comments.xml file
        document_xml_path: Path to document.xml file

    Returns:
        dict: Dictionary of comments keyed by comment ID
    """
    if not os.path.exists(comments_xml_path):
        return {}

    # Parse comments.xml
    comments_tree = ET.parse(comments_xml_path)
    comments_root = comments_tree.getroot()

    comments = {}
    for comment in comments_root.findall('.//w:comment', NAMESPACES):
        comment_id = comment.get(f'{{{NAMESPACES["w"]}}}id')
        author = comment.get(f'{{{NAMESPACES["w"]}}}author')
        date = comment.get(f'{{{NAMESPACES["w"]}}}date')

        # Extract comment text from paragraphs
        text_parts = []
        for para in comment.findall('.//w:p', NAMESPACES):
            for run in para.findall('.//w:r', NAMESPACES):
                for text_elem in run.findall('.//w:t', NAMESPACES):
                    if text_elem.text:
                        text_parts.append(text_elem.text)

        comment_text = ''.join(text_parts)
        comments[comment_id] = {
            'author': author,
            'date': date,
            'text': comment_text,
            'context': ''  # Will be filled by finding location in document
        }

    # Parse document.xml to find comment locations and context
    if os.path.exists(document_xml_path):
        doc_tree = ET.parse(document_xml_path)
        doc_root = doc_tree.getroot()

        # Find all comment range markers
        comment_ranges = defaultdict(dict)
        for elem in doc_root.findall('.//w:commentRangeStart', NAMESPACES):
            comment_id = elem.get(f'{{{NAMESPACES["w"]}}}id')
            comment_ranges[comment_id]['start'] = elem

        for elem in doc_root.findall('.//w:commentRangeEnd', NAMESPACES):
            comment_id = elem.get(f'{{{NAMESPACES["w"]}}}id')
            comment_ranges[comment_id]['end'] = elem

        # Find paragraph context for each comment
        for comment_id in comments:
            if comment_id in comment_ranges and 'start' in comment_ranges[comment_id]:
                # Find all paragraphs
                for para in doc_root.findall('.//w:p', NAMESPACES):
                    # Check if this paragraph contains the comment start marker
                    for elem in para.iter():
                        if elem == comment_ranges[comment_id]['start']:
                            para_text = extract_text(para, NAMESPACES)
                            # Limit context to 500 chars for readability
                            if len(para_text) > 500:
                                comments[comment_id]['context'] = f"{para_text[:500]}..."
                            else:
                                comments[comment_id]['context'] = para_text
                            break

    return comments


def extract_track_changes(document_xml_path):
    """
    Extract all track change insertions and deletions.

    Args:
        document_xml_path: Path to document.xml file

    Returns:
        tuple: (insertions list, deletions list)
    """
    if not os.path.exists(document_xml_path):
        return [], []

    doc_tree = ET.parse(document_xml_path)
    doc_root = doc_tree.getroot()

    # Extract insertions
    insertions = []
    for ins in doc_root.findall('.//w:ins', NAMESPACES):
        author = ins.get(f'{{{NAMESPACES["w"]}}}author', 'Unknown')
        date = ins.get(f'{{{NAMESPACES["w"]}}}date', 'Unknown')
        text = extract_text(ins, NAMESPACES)
        if text:
            insertions.append({
                'author': author,
                'date': date,
                'text': text
            })

    # Extract deletions
    deletions = []
    for delete in doc_root.findall('.//w:del', NAMESPACES):
        author = delete.get(f'{{{NAMESPACES["w"]}}}author', 'Unknown')
        date = delete.get(f'{{{NAMESPACES["w"]}}}date', 'Unknown')
        text = ''
        # Deletions use w:delText elements
        for run in delete.findall('.//w:r', NAMESPACES):
            for t in run.findall('.//w:delText', NAMESPACES):
                if t.text:
                    text += t.text
        if text:
            deletions.append({
                'author': author,
                'date': date,
                'text': text
            })

    return insertions, deletions


def format_output(filename, comments, insertions, deletions):
    """
    Format extraction results into readable report.

    Args:
        filename: Original .docx filename
        comments: Dictionary of comments
        insertions: List of insertions
        deletions: List of deletions

    Returns:
        str: Formatted report text
    """
    lines = []

    # Header
    lines.append("=" * 80)
    lines.append(f"EXTRACTING COMMENTS FROM {filename}")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Found {len(comments)} comments")
    lines.append("")

    # Comments section
    for comment_id, comment_data in sorted(comments.items(), key=lambda x: int(x[0])):
        lines.append("=" * 80)
        lines.append(f"COMMENT #{comment_id}")
        lines.append(f"Author: {comment_data['author']}")
        lines.append(f"Date: {comment_data['date']}")
        lines.append(f"Comment: {comment_data['text']}")
        lines.append("-" * 80)
        lines.append(f"Context: {comment_data['context']}")
        lines.append("")

    lines.append("=" * 80)
    lines.append("")

    # Track changes section
    lines.append("=" * 80)
    lines.append(f"EXTRACTING TRACK CHANGES FROM {filename}")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Found {len(insertions)} insertions")
    lines.append("")

    for i, ins in enumerate(insertions, 1):
        lines.append(f"{i}. INSERT by {ins['author']} on {ins['date']}:")
        lines.append(f"   TEXT: \"{ins['text']}\"")
        lines.append("")

    lines.append("-" * 80)
    lines.append("")
    lines.append(f"Found {len(deletions)} deletions")
    lines.append("")

    for i, delete in enumerate(deletions, 1):
        lines.append(f"{i}. DELETE by {delete['author']} on {delete['date']}:")
        lines.append(f"   TEXT: \"{delete['text']}\"")
        lines.append("")

    # Summary
    lines.append("=" * 80)
    lines.append("SUMMARY:")
    lines.append(f"  Comments: {len(comments)}")
    lines.append(f"  Insertions: {len(insertions)}")
    lines.append(f"  Deletions: {len(deletions)}")
    lines.append(f"  Total changes: {len(comments) + len(insertions) + len(deletions)}")
    lines.append("=" * 80)
    lines.append("")

    return '\n'.join(lines)


def main():
    """
    Main entry point for command-line usage.
    """
    if len(sys.argv) < 2:
        print("Usage: docx_extractor.py <extracted_docx_dir> [output_file] [original_filename]")
        print("")
        print("Arguments:")
        print("  extracted_docx_dir  Directory containing extracted .docx XML files")
        print("  output_file         Optional output file (prints to stdout if not specified)")
        print("  original_filename   Optional original .docx filename for display")
        sys.exit(1)

    extracted_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    original_filename = sys.argv[3] if len(sys.argv) > 3 else None

    # Validate directory exists
    if not os.path.isdir(extracted_dir):
        print(f"❌ Error: Directory not found: {extracted_dir}")
        sys.exit(1)

    # Build paths to XML files
    comments_xml = os.path.join(extracted_dir, 'word', 'comments.xml')
    document_xml = os.path.join(extracted_dir, 'word', 'document.xml')

    # Validate document.xml exists (required)
    if not os.path.exists(document_xml):
        print(f"❌ Error: document.xml not found in {extracted_dir}/word/")
        sys.exit(1)

    # Extract filename for display (use original if provided, otherwise temp dir name)
    filename = original_filename if original_filename else Path(extracted_dir).name

    try:
        # Extract comments
        comments = extract_comments(comments_xml, document_xml)

        # Extract track changes
        insertions, deletions = extract_track_changes(document_xml)

        # Format output
        report = format_output(filename, comments, insertions, deletions)

        # Write output
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Extraction complete: {output_file}")
            print(f"   Comments: {len(comments)}")
            print(f"   Insertions: {len(insertions)}")
            print(f"   Deletions: {len(deletions)}")
            print(f"   Total changes: {len(comments) + len(insertions) + len(deletions)}")
        else:
            print(report)

    except ET.ParseError as e:
        print(f"❌ Error: Failed to parse XML: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

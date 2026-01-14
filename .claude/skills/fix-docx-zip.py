#!/usr/bin/env python3
"""
Fix DOCX ZIP metadata to match Word/pandoc expectations.
Converts ZIP 3.0 archives with Unix attributes to ZIP 2.0 format.

Usage:
    fix-docx-zip.py <input.docx> <output.docx>

Background:
    The macOS 'zip' command creates ZIP 3.0 archives with Unix-specific
    metadata (create_version=30, external_attr with Unix permissions).
    Microsoft Word and pandoc expect ZIP 2.0 archives with minimal metadata
    (create_version=0, external_attr=0).

    This script extracts a .docx file and repacks it with proper ZIP 2.0
    metadata, fixing "Word found unreadable content" errors caused by
    ZIP format mismatches.
"""

import zipfile
import os
import sys
import tempfile
import shutil
import struct


def _fix_external_attr(docx_path):
    """
    Patch the ZIP central directory to zero out external_attr fields.

    Python's zipfile.writestr() automatically sets external_attr to 0x01800000
    (Unix file permissions), but Word expects 0x00000000.

    Args:
        docx_path: Path to DOCX file to patch
    """
    with open(docx_path, 'r+b') as f:
        # Read entire file
        data = bytearray(f.read())

        # Find End of Central Directory (EOCD) signature
        eocd_sig = b'PK\x05\x06'
        eocd_offset = data.rfind(eocd_sig)
        if eocd_offset == -1:
            raise ValueError("Could not find End of Central Directory signature")

        # Parse EOCD to get central directory offset
        cd_offset = struct.unpack('<I', data[eocd_offset+16:eocd_offset+20])[0]

        # Iterate through central directory entries
        offset = cd_offset
        while offset < eocd_offset:
            # Check for central directory file header signature
            sig = data[offset:offset+4]
            if sig != b'PK\x01\x02':
                break

            # External file attributes are at offset +38 (4 bytes)
            # Zero them out
            data[offset+38:offset+42] = b'\x00\x00\x00\x00'

            # Get sizes to find next entry
            filename_len = struct.unpack('<H', data[offset+28:offset+30])[0]
            extra_len = struct.unpack('<H', data[offset+30:offset+32])[0]
            comment_len = struct.unpack('<H', data[offset+32:offset+34])[0]

            # Move to next entry (header is 46 bytes + variable lengths)
            offset += 46 + filename_len + extra_len + comment_len

        # Write patched data back
        f.seek(0)
        f.write(data)
        f.truncate()


def fix_docx_zip(input_docx, output_docx):
    """
    Repack DOCX with proper ZIP 2.0 metadata.

    Args:
        input_docx: Path to corrupted .docx file
        output_docx: Path to save fixed .docx file
    """
    # Validate input file exists
    if not os.path.exists(input_docx):
        print(f"❌ Error: Input file not found: {input_docx}")
        sys.exit(1)

    # Validate input is a valid ZIP file
    if not zipfile.is_zipfile(input_docx):
        print(f"❌ Error: Input file is not a valid ZIP/DOCX file: {input_docx}")
        sys.exit(1)

    # Create temporary extraction directory
    temp_dir = tempfile.mkdtemp()

    try:
        print(f"📂 Extracting {input_docx}...")

        # Extract the corrupted DOCX
        with zipfile.ZipFile(input_docx, 'r') as zf_in:
            zf_in.extractall(temp_dir)

        print(f"🔧 Repacking with proper ZIP 2.0 metadata...")

        # Repack with ZIP 2.0 metadata (matching pandoc output)
        with zipfile.ZipFile(output_docx, 'w', zipfile.ZIP_DEFLATED) as zf_out:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)

                    # Create ZipInfo with controlled metadata
                    zinfo = zipfile.ZipInfo(arcname)
                    zinfo.create_version = 0  # ZIP 2.0 (matches pandoc)
                    zinfo.external_attr = 0   # Clear Unix-specific attributes
                    zinfo.compress_type = zipfile.ZIP_DEFLATED

                    # Write file to archive
                    with open(file_path, 'rb') as f:
                        zf_out.writestr(zinfo, f.read())

        # Fix external_attr by patching the ZIP central directory
        # Python's writestr() automatically sets external_attr to 0x01800000
        # We need to zero it out to match pandoc's output
        print(f"🔧 Clearing external_attr in ZIP central directory...")
        _fix_external_attr(output_docx)

        # Get file sizes for reporting
        input_size = os.path.getsize(input_docx)
        output_size = os.path.getsize(output_docx)

        print(f"✅ Fixed DOCX saved to {output_docx}")
        print(f"   Input size:  {input_size:,} bytes")
        print(f"   Output size: {output_size:,} bytes")
        print(f"   ZIP version: 0 (ZIP 2.0)")
        print(f"   Attributes:  00000000 (cleared)")

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        sys.exit(1)

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)


def main():
    if len(sys.argv) != 3:
        print("Usage: fix-docx-zip.py <input.docx> <output.docx>")
        print()
        print("Fixes ZIP metadata mismatch causing Word corruption errors.")
        print("Converts ZIP 3.0 archives to ZIP 2.0 format expected by Word/pandoc.")
        print()
        print("Example:")
        print("  fix-docx-zip.py corrupted.docx fixed.docx")
        sys.exit(1)

    input_docx = sys.argv[1]
    output_docx = sys.argv[2]

    fix_docx_zip(input_docx, output_docx)


if __name__ == '__main__':
    main()

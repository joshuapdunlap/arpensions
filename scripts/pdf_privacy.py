"""Inspect every PDF in the publication tree before release."""
import hashlib
import re

import fitz


CONTACT = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?<!\d)(?:\(\d{3}\)\s*|\d{3}[-. ])\d{3}[-. ]\d{4}(?!\d)")
LOCAL_PATH = re.compile(r"(?i)(?:file:/+|[a-z]:[\\/](?:users|windows|documents)|/(?:Users|home)/[^/\s]+/)")
CAPTION = re.compile(r"Privacy extract \| Original page position \d+ of \d+(?: \| Administrative or contact material omitted)?")


def inspect_public_pdfs(public, reviewed_features, revisions):
    errors = []
    for path in sorted(public.rglob("*.pdf")):
        url = "/" + path.relative_to(public).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        features = set()
        with fitz.open(path) as pdf:
            if pdf.embfile_count() or pdf.is_form_pdf or pdf.get_ocgs():
                errors.append(f"{url}: attachment, form or optional layer requires removal or review")
            metadata = " ".join(str(value or "") for value in pdf.metadata.values()) + pdf.get_xml_metadata()
            if pdf.metadata.get("author") or pdf.metadata.get("creator") or pdf.metadata.get("producer") or pdf.get_xml_metadata():
                features.add("metadata")
            if LOCAL_PATH.search(metadata) or CONTACT.search(metadata):
                features.add("identifier in metadata")
            for page in pdf:
                if list(page.annots() or []) or list(page.widgets() or []):
                    errors.append(f"{url}: annotation or field on page {page.number + 1}")
                if page.get_links():
                    features.add("links")
                text = page.get_text()
                if CONTACT.search(text) or LOCAL_PATH.search(text):
                    features.add("contact or path")
                if any(span["type"] == 3 or span.get("opacity") == 0 for span in page.get_texttrace()):
                    features.add("invisible text")
                if revisions.get(url, {}).get("privacyExtract"):
                    if not CAPTION.fullmatch(text.strip()) or len(page.get_image_info()) != 1:
                        errors.append(f"{url}: unexpected image or text layer on page {page.number + 1}")
        if features or url in reviewed_features:
            reviewed = reviewed_features.get(url, {})
            if reviewed.get("sha256") != digest or reviewed.get("features") != sorted(features):
                errors.append(f"{url}: review required for {', '.join(sorted(features))}")
    return errors

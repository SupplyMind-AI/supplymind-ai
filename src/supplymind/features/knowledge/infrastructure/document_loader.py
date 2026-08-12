from pathlib import Path
from docx import Document as DocxDocument
from pypdf import PdfReader
SUPPORTED_SUFFIXES={'.pdf','.txt','.md','.docx'}
def load_document_text(path:str|Path)->str:
 p=Path(path); s=p.suffix.lower()
 if s not in SUPPORTED_SUFFIXES: raise ValueError(f'Unsupported document type: {s}')
 if s in {'.txt','.md'}: return p.read_text(encoding='utf-8')
 if s=='.pdf': return '\n\n'.join(page.extract_text() or '' for page in PdfReader(p).pages)
 return '\n'.join(x.text for x in DocxDocument(p).paragraphs)

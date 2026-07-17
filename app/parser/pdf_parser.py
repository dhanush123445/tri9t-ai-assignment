import fitz
import pdfplumber

from app.parser.models import ParsedNode
from app.parser.hash import create_hash
from app.parser.table_parser import TableParser
from app.parser.ocr import OCRParser
from app.parser.hierarchy import (
    is_heading,
    parse_heading
)


class PDFParser:

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path

        self.root_nodes = []

        self.stack = []

        self.current_node = None

        self.tables = []

    def parse(self):

        document = fitz.open(self.pdf_path)

        table_parser = TableParser(self.pdf_path)

        self.tables = table_parser.extract_tables()

        for page_number, page in enumerate(document):

            self.parse_page(
                page,
                page_number + 1
            )

        # Attach tables only after all pages are parsed
        self.attach_tables()

        self.generate_hashes()

        return self.root_nodes

    def parse_page(
        self,
        page,
        page_number
    ):

        blocks = page.get_text("blocks")

        # OCR fallback for scanned pages
        if not blocks:

            text = OCRParser.extract(page)

            if text:

                self.process_text(
                    text,
                    page_number
                )

            return

        for block in blocks:

            text = block[4].strip()

            if not text:
                continue

            self.process_text(
                text,
                page_number
            )
    def process_text(
            self,
            text,
            page_number
    ):

         if is_heading(text):

            result = parse_heading(text)

            if result is None:
                return

            number, title, level = result

            node = ParsedNode(
                logical_id=number,
                heading=title,
                level=level,
                page=page_number
            )

            self.add_node(node)

            self.current_node = node

         else:

            if self.current_node:

                self.current_node.body += text + "\n"

    def add_node(
        self,
        node
    ):

        while (
            self.stack
            and
            self.stack[-1].level >= node.level
        ):

            self.stack.pop()

        if not self.stack:

            self.root_nodes.append(node)

        else:

            parent = self.stack[-1]

            parent.children.append(node)

            node.parent = parent

        self.stack.append(node)

    
    def generate_hashes(self):

         for node in self.root_nodes:
            self.hash_node(
                node,
                ""
            )

    def hash_node(
        self,
        node,
        parent_path
    ):

        path = parent_path + "/" + node.heading

        node.hash = create_hash(
            node.heading,
            node.body,
            node.level,
            path
        )

        for child in node.children:
            self.hash_node(
                child,
                path
            )

    def attach_tables(self):

        for table in self.tables:

            page = table["page"]

            for node in self.root_nodes:

                self.attach_table_to_node(
                    node,
                    page,
                    table["table"]
                )

    def attach_table_to_node(
        self,
        node,
        page,
        table
    ):

        if node.page == page:
            node.tables.append(table)

        for child in node.children:
            self.attach_table_to_node(
                child,
                page,
                table
            )
import pdfplumber


class TableParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_tables(self):

        extracted_tables = []

        with pdfplumber.open(self.pdf_path) as pdf:

            for page_no, page in enumerate(pdf.pages):

                tables = page.extract_tables()

                for table in tables:

                    extracted_tables.append(
                        {
                            "page": page_no + 1,
                            "table": table
                        }
                    )

        return extracted_tables
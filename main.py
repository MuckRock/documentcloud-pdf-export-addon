"""
This add-on allows you to bulk export PDFs from DocumentCloud
"""

import zipfile

from addon import AddOn


class PdfExport(AddOn):
    """Export all of the selected documents in a zip file"""

    def main(self):
        with zipfile.ZipFile("export.zip", mode="w") as archive:
            for doc_id in self.documents:
                document = self.client.documents.get(doc_id)
                with archive.open(f"{document.slug} - {document.id}.pdf", "w") as pdf:
                    pdf.write(document.pdf)

        self.upload_file(open("export.zip"))


if __name__ == "__main__":
    PdfExport().main()

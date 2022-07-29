"""
This add-on allows you to bulk export PDFs from DocumentCloud
"""

import zipfile

from documentcloud.addon import AddOn


class PdfExport(AddOn):
    """Export all of the selected documents in a zip file"""

    def main(self):
        print(self.documents)
        if not self.documents:
            self.set_message("Please select at least one document")
            return

        with zipfile.ZipFile("export.zip", mode="w") as archive:
            for document in self.get_documents():
                print(f"{document.slug} - {document.id}.pdf")
                with archive.open(f"{document.slug} - {document.id}.pdf", "w") as pdf:
                    pdf.write(document.pdf)

        self.upload_file(open("export.zip"))


if __name__ == "__main__":
    PdfExport().main()

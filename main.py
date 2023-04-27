"""
This add-on allows you to bulk export PDFs from DocumentCloud
"""
import os
import zipfile
from documentcloud.addon import AddOn


class PdfExport(AddOn):
    """Export all of the selected documents in a zip file"""

    def main(self):
        with zipfile.ZipFile("export.zip", mode="w") as archive:
            for document in self.get_documents():
                # print(f"{document.slug} - {document.id}.pdf")
                with archive.open(f"{document.slug} - {document.id}.pdf", "w") as pdf:
                    pdf.write(document.pdf)
        if os.path.getsize("export.zip")>5300000000:
            self.set_message("The export you are trying to do is larger than 5GB" 
                             " which is the maximum allowed, please retry "
                             "on a smaller set of documents.")
        else: 
            self.upload_file(open("export.zip"))


if __name__ == "__main__":
    PdfExport().main()

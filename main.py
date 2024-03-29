"""
This add-on allows you to bulk export PDFs from DocumentCloud
"""
import os
import sys
import zipfile
from documentcloud.addon import AddOn


class PdfExport(AddOn):
    """Export all of the selected documents in a zip file"""

    def main(self):
        if self.get_document_count() is None:
            self.set_message("Please select at least one document.")
            return
        with zipfile.ZipFile("export.zip", mode="w") as archive:
            for document in self.get_documents():
                # print(f"{document.slug} - {document.id}.pdf")
                with archive.open(f"{document.slug} - {document.id}.pdf", "w") as pdf:
                    pdf.write(document.pdf)
        # If the zip file is >5GB, it won't be able to upload to S3, so need to send a warning. 
        if os.path.getsize("export.zip")>5300000000:
            self.set_message("The export you are trying to do is larger than 5GB " 
                             "which is the maximum size allowed. Please retry "
                             "on a smaller set of documents or split up "
                             "the documents you are trying to export into two runs.")
            
            sys.exit(1)
        else: 
            self.upload_file(open("export.zip"))

if __name__ == "__main__":
    PdfExport().main()

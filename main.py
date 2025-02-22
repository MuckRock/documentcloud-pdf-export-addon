""" Uses datetime, zipfile, os and sys """

import os
import sys
import zipfile
from datetime import datetime

from documentcloud.addon import AddOn


class PdfExport(AddOn):
    """
    Export all of the selected documents in a zip file.
    This class handles the export process, including generating a zip file with all selected PDFs.
    """

    def main(self):
        """
        Main function that processes the selected documents and creates a zip file.
        If the zip file exceeds 5GB, an error message is shown, and the process is aborted.
        """
        if self.get_document_count() is None:
            self.set_message("Please select at least one document.")
            return

        # Generate timestamp for the zip file (month, day, hour, minute)
        timestamp = datetime.now().strftime("%m-%d_%H-%M")
        zip_filename = f"export_{timestamp}.zip"

        with zipfile.ZipFile(zip_filename, mode="w") as archive:
            for document in self.get_documents():
                # Add each document's PDF to the zip file
                with archive.open(f"{document.slug} - {document.id}.pdf", "w") as pdf:
                    pdf.write(document.pdf)

        # If the zip file is >5GB, it won't be able to upload to S3, so need to send a warning.
        if os.path.getsize(zip_filename) > 5300000000:
            self.set_message(
                "The export you are trying to do is larger than 5GB "
                "which is the maximum size allowed. Please retry "
                "on a smaller set of documents or split up "
                "the documents you are trying to export into two runs."
            )
            sys.exit(1)
        else:
            # Ensure that the file is opened with binary mode
            with open(zip_filename, "rb") as file:
                self.upload_file(file)


if __name__ == "__main__":
    PdfExport().main()

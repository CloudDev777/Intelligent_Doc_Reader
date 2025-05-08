import os, json
import azure.functions as func
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# load Form Recognizer creds from app settings
endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key      = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
analyzer = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

def main(blob: func.InputStream):
    # blob.name  e.g. "invoices/invoice_1.pdf"
    blob_url = f"{os.getenv('AzureWebJobsStorage').split(';')[1].split('=')[1]}/invoices/{blob.name.split('/')[-1]}"
    poller   = analyzer.begin_analyze_document("prebuilt-invoice", blob_url)
    result   = poller.result()

    doc = result.documents[0]
    data = {
        "InvoiceId":   doc.fields["InvoiceId"].value,
        "VendorName":  doc.fields["VendorName"].value,
        "InvoiceDate": doc.fields["InvoiceDate"].value.isoformat(),
        "TotalAmount": doc.fields["InvoiceTotal"].value,
        "SourcePdf":   blob_url
    }

    # optional: write to output/ for local debugging
    os.makedirs("output", exist_ok=True)
    with open(f"output/{blob.name}.json", "w") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Processed {blob.name}")
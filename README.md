# Intelligent Doc Reader – Azure Invoice Processor

![Azure](https://img.shields.io/badge/Azure-Form%20Recognizer-blue) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Functions](https://img.shields.io/badge/Azure%20Functions-v4-green) ![Power BI](https://img.shields.io/badge/Power%20BI-Report-yellow) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]

A demo that shows how to:

* Automatically process invoice PDFs dropped into Azure Blob Storage
* Extract key fields via Azure Form Recognizer’s **prebuilt-invoice** model
* Emit JSON outputs locally or to storage
* Visualize both structured data and embedded PDFs in Power BI

---

## 📁 Repository structure

```
IntelligentDocReader/
├── .gitignore
├── host.json
├── local.settings.json              ← local secrets, excluded from Git
├── requirements.txt
├── README.md
├── samples/
│   └── invoice_1.pdf                ← sample invoice PDF
├── output/                          ← JSON outputs (optional)
└── ProcessInvoiceBlob/
    ├── __init__.py                  ← Blob-trigger Function code
    └── function.json                ← trigger binding config
```

---

## 🔧 Prerequisites

* An **Azure** subscription (student account works)
* **Azure CLI** (>= 2.0)
* **Python** 3.8+
* **Azure Functions Core Tools** v4
* **Power BI Desktop** (for report)

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone git clone https://github.com/<your-username>/IntelligentDocReader.git
cd IntelligentDocReader
```

### 2. Provision Azure resources

```bash
az group create --name rg-invoices-demo --location eastus

az storage account create --name stginvoicesdemo --resource-group rg-invoices-demo --sku Standard_LRS --location eastus
az storage container create --account-name stginvoicesdemo --name invoices

az cognitiveservices account create --name ai-invoicereader --resource-group rg-invoices-demo --kind FormRecognizer --sku F0 --location eastus

az functionapp create --resource-group rg-invoices-demo --consumption-plan-location eastus --runtime python --functions-version 4 --name fn-invoicereader-demo --storage-account stginvoicesdemo
```

### 3. Configure `local.settings.json`

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<YOUR_STORAGE_CONNECTION_STRING>",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_FORM_RECOGNIZER_ENDPOINT": "<YOUR_FORM_RECOGNIZER_ENDPOINT>",
    "AZURE_FORM_RECOGNIZER_KEY": "<YOUR_FORM_RECOGNIZER_KEY>"
  }
}
```

### 4. Configure `host.json`

```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "maxTelemetryItemsPerSecond": 5
      }
    },
    "logLevel": {
      "Function": "Information",
      "Host.Results": "Warning",
      "Host.Aggregator": "Information"
    }
  }
}
```

### 5. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🏃 Running locally

```bash
func start
```

* Upload PDFs to your `invoices` container
* JSON output appears in `output/`

---

## 🚀 Deploy to Azure

```bash
az login
az account set --subscription "<SUBSCRIPTION_ID>"
func azure functionapp publish fn-invoicereader-demo
```

---

## 📤 Upload a sample invoice

```bash
az storage blob upload --account-name stginvoicesdemo --container-name invoices --name invoice_1.pdf --file samples/invoice_1.pdf
```

---

## 📊 Visualize in Power BI

1. Install the **PDF Viewer** custom visual.
2. **Get Data** → **Folder**, select your `output/` → **Combine & Transform**.
3. In Power Query Editor:

   * Expand **Content** as JSON → Expand record → select
     `InvoiceId`, `VendorName`, `InvoiceDate`, `TotalAmount`, `SourcePdf`.
   * If you need a SAS token, add custom column:

```m
= [SourcePdf] & "?<your-SAS-token>"
```

4. **Close & Apply**.
5. Build report:

   * **Table**: `InvoiceId`, `VendorName`, `InvoiceDate`, `TotalAmount`
   * **PDF Viewer**: bind **Document URL** to `SourcePdf`.
6. **Publish** to Power BI Service.

---

## 💡 Next steps

* Secure blob access via **Azure AD**
* Persist results to **Cosmos DB** or **Azure SQL**
* Automate CI/CD with **GitHub Actions**
* Add unit tests for Functions

---



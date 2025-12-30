# task_manager/bots/emissao/caixa/__init__.py

## Propósito

Manage deposit documents and operations in the Caixa system for CrawJUD-Bots effectively.

Provide a set of methods to handle site navigation, form filling, document creation,
and PDF processing in compliance with Google/PEP 257 docstring standards.

## Dependências Principais

- `backend.common.exceptions`
- `backend.controllers.head`
- `contextlib`
- `pypdf`
- `re`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `shutil`
- `time`

## Classe: `Emissor`

Emissão de guias caixa.

**Herda de:** `CrawJUD`

### Métodos

#### `execution()`

Run the main operation loop and handle each DataFrame row comprehensively.

Iterate through the DataFrame while checking session validity, capturing
errors, and resuming operations as required.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Orchestrate the entire deposit emission procedure and record success or error.

Execute steps like site navigation, deposit data input, PDF creation,
and data extraction in a single call.

**Parâmetros:**

- `self` (Any)

#### `get_site()`

Access deposit site, solve CAPTCHA, and load required deposit interface.

Navigate to the deposit page, handle CAPTCHA resolution, and select
deposit type for further processing.

**Parâmetros:**

- `self` (Any)

#### `locale_proc()`

Define tribunal, comarca, vara, and agency based on user-provided data inputs.

Allow the script to select appropriate locale and proceed with deposit steps.

**Parâmetros:**

- `self` (Any)

#### `proc_nattribut()`

Set the process number and action type for the judicial deposit context.

Insert the required process details, ensuring the correct action type
and default deposit nature.

**Parâmetros:**

- `self` (Any)

#### `dados_partes()`

Fill in party information, including name and document details.

Determine the document type (CPF or CNPJ) automatically and populate
corresponding fields for both plaintiff (autor) and defendant (réu).

**Parâmetros:**

- `self` (Any)

#### `info_deposito()`

Insert depositor's indicator and deposit amount into the form.

Identify the depositor (usually 'Réu') and format the deposit value
to comply with input requirements.

**Parâmetros:**

- `self` (Any)

#### `make_doc()`

Generate the deposit document and initiate the PDF download sequence.

Trigger the system to create a deposit PDF that is saved for further
renaming and data extraction.

**Parâmetros:**

- `self` (Any)

#### `rename_pdf()`

Rename and relocate the downloaded PDF with a standardized file name.

Use bot_data for constructing the new name and move the file to its
final output directory, then return the new File Name .

Returns:
    str: New PDF File Name after relocation.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `get_val_doc_and_codebar()`

Extract deposit values and barcode from the specified PDF.

Open the PDF, locate barcodes and monetary values, then package the
results into a structured list for further processing.

Args:
    pdf_name (str): PDF file name to parse.

Returns:
    list: Contains process information, including barcodes and deposit data.

**Parâmetros:**

- `self` (Any)
- `pdf_name` (str)


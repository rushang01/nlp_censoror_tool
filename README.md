# Censoror Tool Using NLP
By Rushang Sunil Chiplunkar

## Introduction
The Censoror is a sophisticated data processing tool designed to automate the redaction of sensitive information from text documents. This Python-based application ensures the confidentiality of personal names, dates, phone numbers, and addresses in documents such as the Enron Email Dataset.

## Installation and Setup
Before running The Censoror, please ensure python and pipenv are installed on your system. Follow these steps to set up the project:

Clone the repository to your local machine.
Navigate to the project directory and run pipenv install to set up the virtual environment and install dependencies.

Usage
To censor sensitive information from text files within a directory, use the following command:


pipenv run python censoror.py --input '*.txt' --names --dates --phones --address --output 'files/' --stats stderr

## Parameters
--input: Specifies the glob pattern for input text files.

--output: Directory where the censored files will be stored.

--names: Censors any detected names.

--dates: Censors date formats.

--phones: Censors phone numbers in various formats.

--address: Censors physical addresses.

--stats: Specifies the output for censorship statistics. Options include 'stdout', 'stderr', or a specified file path.

# Function Descriptions

## `analyze_entities(text)`
- **Purpose**: Utilizes the Google Natural Language API to analyze and identify entities within the given text, returning a response with recognized entities and their types (e.g., person, location).
- **Parameters**: 
  - `text` (str): The text content to be analyzed for entities.
- **Returns**: Response from the Google Natural Language API containing detected entities.

## `censor_email_names(doc, content)`
- **Purpose**: Detects email addresses in the text and censors parts recognized as names, updating the global count of names found within emails.
- **Parameters**: 
  - `doc` (Doc): A spaCy Doc object representing the parsed content.
  - `content` (str): The original text content.
- **Returns**: Text content with censored email names.

## `spacy_censor_by_entity_type(content, flags)`
- **Purpose**: Censors entities in the text based on specified flags using spaCy's Named Entity Recognition (NER), handling names, addresses, and dates, and updates global counts for each entity type.
- **Parameters**: 
  - `content` (str): The text content to be censored.
  - `flags` (list): A list of flags indicating which entity types to censor.
- **Returns**: Text content with specified entities censored.

## `google_nlp_censor_by_entity_type(content, flags)`
- **Purpose**: Complements spaCy's NER by using Google Natural Language API to detect and censor additional entities not covered or missed by spaCy, focusing on names, addresses, dates, and phone numbers, and updating global counts for each.
- **Parameters**: 
  - `content` (str): The text content to be censored.
  - `flags` (list): A list of flags indicating which entity types to censor.
- **Returns**: Text content with additional entities censored based on Google's NLP analysis.

## `censor_text(content, flags)`
- **Purpose**: Orchestrates the overall text censoring process by combining spaCy NER, Google NLP, and PyAP for address parsing, ensuring all specified entity types are censored within the text.
- **Parameters**: 
  - `content` (str): The text content to be censored.
  - `flags` (list): A list of flags indicating which entity types to censor.
- **Returns**: Fully censored text content according to the specified flags.

## `stats(file)`
- **Purpose**: Generates a summary of censorship statistics for a given file, including counts of censored names, addresses, dates, phone numbers, and email names.
- **Parameters**: 
  - `file` (str): The name of the file being processed.
- **Returns**: A formatted string containing the statistics summary for the processed file.

## `process_files(input_pattern, output_dir, censor_flags, stats_output)`
- **Purpose**: Processes multiple files based on a glob pattern, applying censorship according to specified flags, outputs censored files and statistics as per the user's choice (`stdout`, `stderr`, or a file).
- **Parameters**: 
  - `input_pattern` (str): A glob pattern specifying the files to process.
  - `output_dir` (str): The directory where censored files will be stored.
  - `censor_flags` (dict): A dictionary of flags indicating which entity types to censor.
  - `stats_output` (str): Specifies where to output the statistics summary (`stdout`, `stderr`, or a file path).
- **Side Effects**: Writes censored files to the specified output directory and outputs censorship statistics as directed.

## `main()`
- **Purpose**: Entry point for the script, parsing command-line arguments, setting up the environment, and initiating file processing with specified parameters.
- **Side Effects**: Executes the censorship process on specified files and outputs results accordingly.


## Censorship Flags and Characters
The Censoror tool applies specific parameters to each censorship flag:

Names and Addresses are identified through spaCy's Named Entity Recognition and Google NLP for email names.
Dates are detected via regular expressions and natural language processing techniques.
Phone numbers are found using the Google NLP library for comprehensive format coverage.
The censored characters are replaced with the Unicode full block character █ (U+2588) to maintain the original text's layout while ensuring anonymity. Spaces between censored words, such as names, are also redacted to prevent partial information disclosure.

## Statistics Output
The --stats parameter enables users to output a summary of the censorship process to either a file, standard output, or standard error, detailing the counts and types of terms censored. This feature aids in understanding the extent of redactions made and in debugging. The stats output format has been designed to include the count of censored items grouped by flags for more detailed analysis.

stdout: Directs the summary to the standard output stream. Use --stats stdout for this  behavior.
stderr: Directs the summary to the standard error output stream. Use --stats stderr.
File Path: Directs the summary to a specified file. Do not include "stdout" or "stderr" in your command if you wish to get a stats.txt file under your output directory.

## Dataset
For testing, the Enron Email Dataset is recommended. Please utilize a manageable subset since it has an extensive size.

## Documentation and Assumptions
This README includes detailed setup and usage instructions, ensuring ease of use. During the development of The Censoror, several assumptions were made:

Sensitive information is primarily contained within the text and does not include images or non-text elements.
The spaCy model and Google NLP provide sufficient coverage for named entity recognition, albeit with potential limitations in detecting less conventional names or addresses.

## Known Bugs and External Resources
Bugs: Few entities are not censored correctly, while few others may be censored incorrectly. These are due to limitations of NLP and the NLP libraries used. spaCy and Google NLP are both used in this project to catch most entities that need to be censored. 
External resources such as spaCy documentation, Google Cloud Natural Language API documentation, and Python's official documentation were extensively used.

## Testing
Tests are structured to cover each feature individually, ensuring the correctness of the censoring process across various document types and contents. Tests can be executed with the command pipenv run python -m pytest.

test_address.py
Purpose: Tests the application's ability to censor physical addresses using PyAP, spaCy and Google NLP.
Method: test_censor_address_with_pyap verifies that a given address is censored entirely, replaced by a placeholder of equal length.

test_dates.py
Purpose: Ensures that dates in various formats are correctly identified and censored.
Method: test_censor_date checks if a specific date within a sentence is replaced with a placeholder, leaving the rest of the sentence intact.

test_names.py
Purpose: Validates the censoring of person names, whether mentioned individually or multiple names within the same context.
Methods:
test_censor_single_name confirms a single name is censored.
test_censor_multiple_names ensures multiple names in the same sentence are each replaced with placeholders.

test_phones.py
Purpose: Assesses the tool's capability to censor phone numbers in standard formats.
Method: test_censor_phone_number ensures that a phone number is fully censored, with a placeholder substituting the original number.

## Conclusion
The Censoror represents a significant step forward in automating the sensitive information redaction process, combining advanced NLP techniques with user-friendly operation. This tool is poised to streamline privacy protection efforts in a wide range of document processing contexts.

import sys
import spacy
import re
import argparse
from glob import glob
import os
import pyap
from spacy.matcher import Matcher
from google.cloud import language_v1
import en_core_web_md
import phonenumbers


name_count = 0
address_count = 0
date_count = 0
phone_count = 0

# Load spaCy model
nlp = en_core_web_md.load()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'quiet-radius-416123-dced0b64f239.json'

def analyze_entities(text):
    """
    Use Google Natural Language API to analyze entities in the text.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)

    return response
    


def censor_email_names(doc, content):
    # Define a pattern for matching email addresses
    email_pattern = [{"LIKE_EMAIL": True}]
    matcher = Matcher(nlp.vocab)
    matcher.add("EMAIL_DETECTION", [email_pattern])
    
    matches = matcher(doc)
    emails = [doc[start:end].text for _, start, end in matches]

    # Extract potential names from emails
    for email in emails:
        name_parts = re.split(r'[.\-_]', email.split('@')[0])
        name_parts_str = ' '.join(name_parts)
        
        # print(name_parts_str)
        doc = nlp(name_parts_str)
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
               
                # Replace "name1 name2" with name1.name2 to match with the email names in text
                content = content.replace(ent.text.replace(' ','.'), '█' * len(ent.text))

    return content    

def spacy_censor_by_entity_type(content,flags):
    entity_types = []
    global name_count
    global address_count
    global date_count
    global phone_count
    
    name_entities = ['PERSON']
    address_entities = ['GPE','LOC','FAC']
    date_entities = ['DATE']

    doc = nlp(content)

    sorted_ents = sorted(doc.ents, key=lambda ent: len(ent.text), reverse=True) 

    if 'address' in flags:
        entity_types.extend(address_entities)
    if 'names' in flags:
        #Email Layer
        content = censor_email_names(doc, content)
        entity_types.extend(name_entities)
    if 'dates' in flags:
        entity_types.extend(date_entities)
        
    for ent in sorted_ents:
        if ent.label_ in entity_types:
            content = content.replace(ent.text, '█' * len(ent.text))
            if ent.label_ in name_entities:
                name_count += 1
            if ent.label_ in address_entities:
                address_count += 1
            if ent.label_ in date_entities:
                date_count += 1
    return content
    
def google_nlp_censor_by_entity_type(content,flags):
    entity_types = []
    global name_count
    global address_count
    global date_count
    global phone_count
    
    name_entities = [language_v1.Entity.Type.PERSON]
    address_entities = [language_v1.Entity.Type.ADDRESS]
    date_entities = [language_v1.Entity.Type.DATE]

    if 'address' in flags:
        entity_types.extend(address_entities)
    if 'names' in flags:
        #Email Layer
        entity_types.extend(name_entities)
    if 'dates' in flags:
        entity_types.extend(date_entities)
    response = analyze_entities(content)
    # print(response)
    for entity in response.entities:
        if entity.type_ in entity_types:
            content = content.replace(entity.name, '█' * len(entity.name))
            if entity.type_ in name_entities:
                name_count += 1
            if entity.type_ in address_entities:
                address_count += 1
            if entity.type_ in date_entities:
                date_count += 1
    return content

def censor_text(content, flags):
    global name_count
    global address_count
    global date_count
    global phone_count

    #PyAp layer to catch and censor addresses.
    if 'address' in flags:
        addresses = pyap.parse(content, country='US')
        for address in addresses:
            content = content.replace(str(address),'█'*len(str(address)))

    #Regex to catch and censor phone numbers
    if 'phones' in flags:
        for match in phonenumbers.PhoneNumberMatcher(content, None):
            phone = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            # Calculate the length of the formatted phone number for replacement
            replacement = '█' * len(phone)
            # Replace the original text that matched the phone number
            content = content[:match.start] + replacement + content[match.end:]
            phone_count += 1

    # Censor names,addresses or dates using spaCy's named entity recognition
    content = spacy_censor_by_entity_type(content,flags)

    # Censor remaining names,addresses or dates using Google NLP
    content = google_nlp_censor_by_entity_type(content,flags)  

    return content

def stats(file):
    global name_count
    global address_count
    global date_count
    global phone_count

    stats_content = [
                     f"File: {file}\n",
                     f"Name Count: {name_count}\n", 
                     f"Address Count: {address_count}\n",
                     f"Date Count: {date_count}\n",
                     f"Phone Count: {phone_count}\n\n",
                    ]

    name_count = 0
    address_count = 0
    date_count = 0
    phone_count = 0

    return stats_content



def process_files(input_pattern, output_dir, censor_flags, stats_output):
    global name_count
    global address_count
    global date_count
    global phone_count

    stats_path = os.path.join(output_dir, "stats.txt")
    if os.path.exists(stats_path):
        os.remove(stats_path)

    for file_path in glob(input_pattern):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue  # Skip to the next file

        try:
            censored_content = censor_text(content, censor_flags)
            
        except Exception as e:
            print(f"Error censoring file {file_path}: {e}")
            continue  # Skip to the next file
        
        try:
            stats_content = stats(file_path)
            if stats_output == 'stdout':
                print(''.join(stats_content))
            elif stats_output == 'stderr':
                sys.stderr.write(''.join(stats_content))
            else:
                with open(stats_path, 'a') as f:
                    f.writelines(stats_content)


        except Exception as e:
            print(f"Error writing into stats file {stats_output}: {e}")
            continue  # Skip to the next file

        try:
            output_path = os.path.join(output_dir, f"{os.path.basename(file_path)}.censored")

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(censored_content)
                print(f"Processed and saved: {output_path}")
        except Exception as e:
            print(f"Error writing censored content to file {output_path}: {e}")
    

def main():
    parser = argparse.ArgumentParser(description='Censor sensitive information from text files.')
    parser.add_argument('--input', type=str, required=True, help='Glob pattern for input files')
    parser.add_argument('--output', type=str, required=True, help='Directory to store censored files')
    parser.add_argument('--names', action='store_true', help='Flag to censor names')
    parser.add_argument('--dates', action='store_true', help='Flag to censor dates')
    parser.add_argument('--phones', action='store_true', help='Flag to censor phone numbers')
    parser.add_argument('--address', action='store_true', help='Flag to censor addresses')
    parser.add_argument('--stats', nargs='?', const='default_output', default='stdout',
                        help="Output for stats. Use 'stdout', 'stderr', or a file path. Defaults to a file if not specified.")
    
    
    args = parser.parse_args()

    if args.stats == 'default_output':
        # User has specified '--stats' without a value, default to a file
        stats_output = 'stats_output.txt'  # Provide a default file name
    else:
        stats_output = args.stats  # Use the provided value
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    process_files(args.input, args.output, {
        'names': args.names,
        'dates': args.dates,
        'phones': args.phones,
        'address': args.address,
    }, stats_output)

if __name__ == "__main__":
    main()

import os
ASSITSTANT_TOKEN = os.getenv('TEST_ASSISTANT_TOKEN', '')
DIRECTOR_TOKEN   = os.getenv('TEST_DIRECTOR_TOKEN', '')
PRODUCER_TOKEN   = os.getenv('TEST_PRODUCER_TOKEN', '')
ASSISTANT_AUTH_HEADER = {'Authorization': 'Bearer ' + ASSITSTANT_TOKEN}
DIRECTOR_AUTH_HEADER  = {'Authorization': 'Bearer ' + DIRECTOR_TOKEN}
PRODCUER_AUTH_HEADER  = {'Authorization': 'Bearer ' + PRODUCER_TOKEN}
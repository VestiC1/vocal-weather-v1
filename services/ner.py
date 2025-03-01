from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class NERService:
    """ NER Service """

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
        self.model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
        self.nlp = pipeline('ner', model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")

    def extract_entities(self, text, labels=['LOC', 'DATE']):
        resultat = self.nlp(text)
        extracted = []

        for ent in resultat :
            #if ent['entity_group'] in labels :
            extracted.append((ent['entity_group'], ent['word']))
        return extracted

if __name__ == '__main__':
    ner = NERService()

    print(ner.extract_entities("Météo à Tours pour 3 jours"))
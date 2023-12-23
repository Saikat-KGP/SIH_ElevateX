import spacy
from fuzzywuzzy import fuzz
import csv
import pickle
#spacy.download("en_core_web_sm")
# nltk.download('popular')
# nltk.download('punkt')
class GeoSpatialQuerySystem:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tables = {}
        self.load_tables()

    def load_tables(self):
        table_files = ['INDIA.csv', 'USA1.csv', 'AUSTRALIA.csv']
        for file in table_files:
            with open(file, 'r') as f:
                reader = csv.reader(f)
                country_name = file.split('.')[0]
                self.tables[country_name] = {'city': [], 'state': []}
                for row in reader:
                    if row[0] not in self.tables[country_name]['city']:
                        self.tables[country_name]['city'].append(row[0])
                    if row[1] not in self.tables[country_name]['state']:
                        self.tables[country_name]['state'].append(row[1])

    def identify_place_names(self, sentence):
        doc = self.nlp(sentence)
        place_names = []
        for ent in doc.ents:
            if ent.label_ == "GPE":
                for table_name, table in self.tables.items():
                    for column_name, column in table.items():
                        for name in column:
                            score = fuzz.ratio( str(ent).lower() , name.lower() )
                            if score > 80:
                                if {"token": str(ent), "canonical_name": name, "table": table_name} not in place_names:
                                    place_names.append({"token": str(ent), "canonical_name": name, "table": table_name})

        doc = self.nlp(sentence)
        for token in doc:
            if token.pos_ == "PROPN" and not token.is_stop:
                for table_name, table in self.tables.items():
                    for column_name, column in table.items():
                        for name in column:
                            score = fuzz.ratio(token.text.lower(), name.lower())
                            if score > 80:
                                if {"token": token.text, "canonical_name": name, "table": table_name} not in place_names:
                                    place_names.append({"token": token.text, "canonical_name": name, "table": table_name})
        return place_names

# if __name__ == "__main__":
geo_system = GeoSpatialQuerySystem()
pickle.dump(geo_system, open('modelsih3.pkl', 'wb'))
model = pickle.load(open('modelsih3.pkl','rb'))
sentence = "Which of the following saw the highest average temperature in January, Maharashtra, Ahmedabad or Sydney and Los Angeles?"
sentence = sentence.title()
print(sentence)

place_names = geo_system.identify_place_names(sentence)
print(place_names)


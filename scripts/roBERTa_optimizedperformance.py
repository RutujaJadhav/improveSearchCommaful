from sentence_transformers import SentenceTransformer
model2= SentenceTransformer('roberta-base-nli-mean-tokens')

import scipy
# input from the user - listener
query = 'Harry Potter' #@param {type: 'string'}

#encode the data - sents_bert is the preprocessed data containing the preprocessed text content 
sentence_embeddings = model2.encode(sents_bert)

#encode the query 
queries = [query]
query_embeddings = model2.encode(queries)

# Find the closest 3 sentences of the corpus for each query sentence based on cosine similarity
number_top_matches = 10 #@param {type: "number"}

print("Semantic Search Results")

for query, query_embedding in zip(queries, query_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], sentence_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    for idx, distance in results[0:number_top_matches]:
        print(sents_bert[idx].strip(), "(Cosine Score: %.4f)" % (1-distance))
        print()
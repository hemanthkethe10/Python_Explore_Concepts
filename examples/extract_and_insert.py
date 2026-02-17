from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai.embeddings_utils import get_embedding
import pinecone
import os

# Initialize Pinecone
pinecone.init(api_key="a95d974d-5df3-4d7d-8b1e-f5e2927ee1cb", environment="us-east-1")

# Create or connect to a Pinecone index
index_name = "bradai"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536, metric="cosine")
index = pinecone.Index(index_name)

# Semantic chunking using RecursiveCharacterTextSplitter
def semantic_chunking(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

# Process documents and insert into Pinecone
def process_and_insert(document_content, metadata):
    chunks = semantic_chunking(document_content)
    for i, chunk in enumerate(chunks):
        # Generate embeddings for the chunk
        embedding = get_embedding(chunk, engine="text-embedding-ada-002")
        
        # Prepare metadata
        chunk_metadata = metadata.copy()
        chunk_metadata.update({"chunk_number": i})
        
        # Upsert into Pinecone
        index.upsert([{
            "id": f"{metadata['source']}_chunk_{i}",
            "values": embedding,
            "metadata": chunk_metadata
        }])

# Example usage
if __name__ == "__main__":
    documents = {
        "Constellations": {
            "content": """
            Constellations are groups of stars that form recognizable patterns in the night sky. They have been
            used for navigation,
            storytelling, and understanding the cosmos for thousands of years. Ancient civilizations assigned
            names and myths to
            these patterns, many of which are still recognized today.
            There are 88 officially recognized constellations, including famous ones like Orion, Ursa Major, and
            Leo. Orion,
            also known as 'The Hunter,' is one of the most prominent constellations, easily identified by its
            three-star belt.
            Ursa Major, or 'The Great Bear,' includes the Big Dipper, a well-known asterism. Leo represents a
            lion and is
            visible during spring in the northern hemisphere.
            Constellations are not only cultural artifacts but also serve scientific purposes. Astronomers use
            them to divide
            the celestial sphere into regions, helping locate stars and other celestial objects. While stars in a
            constellation
            may appear close from Earth's perspective, they are often vast distances apart in space.
            """,
            "metadata": {"source": "Constellations_Q&A", "title": "Constellations", "tag_id": "tag_1"}
        },
        "Animals": {
            "content": """
                Animals are multicellular organisms that belong to the kingdom Animalia. They are characterized by
                their ability
                to move voluntarily, consume organic material, breathe oxygen, and reproduce sexually. Animals
                are highly diverse,
                ranging from tiny insects to large mammals like elephants and whales.
                There are various types of animals classified based on their characteristics and habitats. Mammals
                are warm-blooded
                animals that have hair or fur and feed their young with milk. Birds are feathered creatures that are
                known for their
                ability to fly, though some species are flightless. Reptiles are cold-blooded animals with scales,
                including snakes,
                lizards, and turtles. Amphibians like frogs and salamanders live both on land and in water.
                Marine animals such as fish, dolphins, and jellyfish inhabit the oceans, while terrestrial animals like
                lions, tigers,
                and bears roam the land. Animals play essential roles in ecosystems, from pollinating plants to
                maintaining food chains.
                """,
            "metadata": {"source": "Animals_Q&A", "title": "Animals", "tag_id": "tag_2"}
        }
    }

    for doc_name, doc_data in documents.items():
        process_and_insert(doc_data["content"], doc_data["metadata"])

    print("Documents inserted into Pinecone successfully.")

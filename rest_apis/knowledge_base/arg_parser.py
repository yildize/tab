import argparse


# Command line argument parsing
parser = argparse.ArgumentParser(description='Run the Knowledge Base API server.')

# Split arguments
parser.add_argument('--source_type', type=str, default='docs', choices=['pdfs', 'docs', 'qa_docs'], help='Type of source you want load')
parser.add_argument('--source_path', type=str, default="./storage/sources", help='Path to the source files to split')
parser.add_argument('--chunk_size', type=int, default=1000, help='Size of each chunk')
parser.add_argument('--chunk_overlap', type=int, default=0, help='Overlap between chunks')

# Serve arguments
parser.add_argument('--serve_style', type=str, default='flask', choices=['flask', 'waitress'], help='Server type to run with')
parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
parser.add_argument('--port', type=int, default=5000, help='Port number')
parser.add_argument('--num_threads', type=int, default=4, help='Number of threads (used only for waitress)')

# Embedder name
parser.add_argument('--embedder_name', type=str, default="all-mpnet-base-v2", help='Name of the embedder to use')
# Optional Cross-Encoder name
parser.add_argument('--cross_encoder_name', type=str, default=None, help='Optional cross encoder name') # cross-encoder/ms-marco-MiniLM-L-6-v2
# Optional Page Docs path Specifically used for Cross-Encoder search:
parser.add_argument('--page_docs_path', type=str, default=None, help='Optional page doc name specifically used with cross-encoder search') # "./storage/docs/page_doc.pkl"
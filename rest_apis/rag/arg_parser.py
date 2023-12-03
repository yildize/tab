import argparse


# Command line argument parsing
parser = argparse.ArgumentParser(description='Run the RAG API Server.')

# Serve arguments
parser.add_argument('--serve_style', type=str, default='flask', choices=['flask', 'waitress'], help='Server type to run with')
parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
parser.add_argument('--port', type=int, default=5001, help='Port number')
parser.add_argument('--num_threads', type=int, default=1, help='Number of threads (used only for waitress)')

# RAG Type:
parser.add_argument('--rag_type', type=str, default='search_pages', choices=['search_pages', 'search_chunks'],  help='Define rag type')

# URLs
parser.add_argument('--llm_endpoint_url', type=str, default=None, help='Full LLM endpoint URL')
parser.add_argument('--base_kb_endpoint_url', type=str, default=None, help='Base KB endpoint URL')
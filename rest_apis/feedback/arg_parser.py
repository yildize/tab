import argparse


# Command line argument parsing
parser = argparse.ArgumentParser(description='Run the FEEDBACK API')

# Serve arguments
parser.add_argument('--serve_style', type=str, default='flask', choices=['flask', 'waitress'], help='Server type to run with')
parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
parser.add_argument('--port', type=int, default=5010, help='Port number')
parser.add_argument('--num_threads', type=int, default=1, help='Number of threads (used only for waitress)')



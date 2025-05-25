import argparse
import glob

from index_builder.build_index import build_index
from search.search import search

def main():
    parser = argparse.ArgumentParser(description='Main entry point for building and searching the index')
    
    subparsers = parser.add_subparsers(dest='command')

    # Подкоманда для сборки индекса
    build_parser = subparsers.add_parser('build', help='Build the search index')
    build_parser.add_argument('inputs', nargs='+', help='Input JSON files')
    build_parser.add_argument('-o', '--output', required=True, help='Output index file')

    # Подкоманда для поиска
    search_parser = subparsers.add_parser('search', help='Search in the index')
    search_parser.add_argument('index', help='Path to index file')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('-e', '--encoding', choices=['delta', 'gamma', None], default=None, help='Encoding type')

    args = parser.parse_args()

    if args.command == 'build':
        all_inputs = []
        for input_pattern in args.inputs:
            matched_files = glob.glob(input_pattern)
            all_inputs.extend(matched_files)
        build_index(all_inputs, args.output)
    elif args.command == 'search':
        results = search(args.index, args.query, args.encoding)
        print(results)

if __name__ == "__main__":
    main()
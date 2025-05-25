import argparse
from .inverted_index import InvertedIndex


def build_index(inputs: list, output: str):
    index = InvertedIndex()
    index.merge_jsons(inputs)
    index.build_index()
    index.encode_indexes()
    index.save(output)
    print(f"Index built successfully. Saved to {output}")


def main():
    parser = argparse.ArgumentParser(description='Build search index from JSON files')
    parser.add_argument('inputs', nargs='+', help='Input JSON files')
    parser.add_argument('-o', '--output', required=True, help='Output index file')
    
    args = parser.parse_args()
    build_index(args.inputs, args.output)

if __name__ == "__main__":
    main()
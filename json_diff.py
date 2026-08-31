import argparse
import json
from pathlib import Path
from typing import Any, List, Optional


def format_path(path: List[Any]) -> str:
	result = '$'
	for item in path:
		if isinstance(item, int):
			result += f'[{item}]'
		else:
			result += f'[{item!r}]'
	return result


def compare(left: Any, right: Any, path: Optional[List[Any]] = None) -> List[str]:
	path = [] if path is None else path
	differences = []

	if type(left) is not type(right):
		differences.append(
			f'{format_path(path)}: type differs: {type(left).__name__} != {type(right).__name__}'
		)
		return differences

	if isinstance(left, dict):
		left_keys = set(left)
		right_keys = set(right)
		for key in sorted(left_keys - right_keys, key=str):
			differences.append(f'{format_path(path + [key])}: only in left: {left[key]!r}')
		for key in sorted(right_keys - left_keys, key=str):
			differences.append(f'{format_path(path + [key])}: only in right: {right[key]!r}')
		for key in sorted(left_keys & right_keys, key=str):
			differences.extend(compare(left[key], right[key], path + [key]))
	elif isinstance(left, list):
		shared_length = min(len(left), len(right))
		for index in range(shared_length):
			differences.extend(compare(left[index], right[index], path + [index]))
		for index in range(shared_length, len(left)):
			differences.append(f'{format_path(path + [index])}: only in left: {left[index]!r}')
		for index in range(shared_length, len(right)):
			differences.append(f'{format_path(path + [index])}: only in right: {right[index]!r}')
	elif left != right:
		differences.append(f'{format_path(path)}: {left!r} != {right!r}')

	return differences


def load_json(path: Path) -> Any:
	with path.open(encoding='utf-8') as file:
		return json.load(file)


def main() -> int:
	parser = argparse.ArgumentParser(description='Compare two JSON files.')
	parser.add_argument('left', type=Path, help='Path to the left JSON file')
	parser.add_argument('right', type=Path, help='Path to the right JSON file')
	args = parser.parse_args()

	try:
		differences = compare(load_json(args.left), load_json(args.right))
	except (OSError, json.JSONDecodeError) as error:
		parser.error(str(error))

	if differences:
		print('\n'.join(differences))
		return 1

	print('JSON files are identical.')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
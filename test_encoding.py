# -*- coding: utf-8 -*-
import sys
import io

# Set stdout encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

test_str = '1+1+1双学历合作办学'
print('Test string:', test_str)
print('Length:', len(test_str))

# Show each character's Unicode code point
print('\nCharacter analysis:')
for i, c in enumerate(test_str):
    print(f'  {i}: {repr(c)} = U+{ord(c):04X}')

# Test dict matching
product_outcome_map = {
    '1+1+1双学历合作办学': {'new_project': 1},
}

print('\nDict matching test:')
print('test_str in map:', test_str in product_outcome_map)
print('Keys in map:', list(product_outcome_map.keys()))

# Test startswith
print('\nstartswith test:')
print('test_str.startswith(1+1+1):', test_str.startswith('1+1+1'))
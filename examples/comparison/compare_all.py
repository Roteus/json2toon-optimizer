"""Script to compare JSON, TOON and TOON-COMPACT formats"""
import sys
import io
import json
from pathlib import Path
from json2toon import TOONEncoder, CompactTOONEncoder, TokenCounter

# Force UTF-8 output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

examples_dir = Path('examples/comparison')
results = []

for json_file in sorted(examples_dir.glob('*.json')):
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    
    json_min = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    toon = TOONEncoder().encode(data)
    compact = CompactTOONEncoder().encode(data)
    
    json_tokens = TokenCounter.count_tokens(json_min)
    toon_tokens = TokenCounter.count_tokens(toon)
    compact_tokens = TokenCounter.count_tokens(compact)
    
    formats = [
        ('JSON', json_tokens),
        ('TOON', toon_tokens),
        ('COMPACT', compact_tokens)
    ]
    formats.sort(key=lambda x: x[1])
    winner = formats[0][0]
    
    results.append({
        'file': json_file.name,
        'json': json_tokens,
        'toon': toon_tokens,
        'compact': compact_tokens,
        'winner': winner
    })

print('='*95)
print('COMPARATIVE ANALYSIS: JSON vs TOON vs TOON-COMPACT')
print('='*95)
print()
print(f"{'File':<45} {'JSON':>8} {'TOON':>8} {'COMPACT':>10} {'Winner':<12}")
print('-'*95)

for r in results:
    winner_mark = {
        'JSON': '  ✓ JSON',
        'TOON': '  ✓ TOON',
        'COMPACT': '  ✓ COMPACT'
    }
    print(f"{r['file']:<45} {r['json']:>8} {r['toon']:>8} {r['compact']:>10} {winner_mark[r['winner']]:<12}")

print('='*95)
print()

# Statistics
json_wins = sum(1 for r in results if r['winner'] == 'JSON')
toon_wins = sum(1 for r in results if r['winner'] == 'TOON')
compact_wins = sum(1 for r in results if r['winner'] == 'COMPACT')

print('STATISTICS:')
print(f"  JSON wins:         {json_wins} cases")
print(f"  TOON wins:         {toon_wins} cases")
print(f"  TOON-COMPACT wins: {compact_wins} cases")
print()
print('='*95)

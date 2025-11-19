# Token counting rules and JSON → TOON conversion

_Source: official TOON ecosystem on GitHub and associated tools_

## 1. Context and origin of rules

This technical summary was assembled from three main sources:

1. Repository **toon-format/toon** (TypeScript implementation, CLI, README and cheatsheet). citeturn5view0
2. Repository **toon-format/spec** (official specification – used when accessible as conceptual reference). citeturn7search0
3. Web tools linked to the TOON project:
   - **json2toon-optimizer / Token Calculator** citeturn4view0
   - **json2toon-optimizer – Token Counter & Cost Calculator** citeturn4view1

From this, I extracted all explicit rules about:

- How the **token-counter** estimates tokens and costs.
- How the **JSON → TOON** converter (`encode` and CLI) transforms structure and values.

> Note: when something is a reasonable inference (and not written literally), I mark it as “inference” so as not to mix fact with assumption.

---

## 2. Token counting rules (token‑counter)

### 2.1 Token‑counter objective

The tools linked to the TOON project exposed via web (json2toon-optimizer) use a token counter to:

- Compare **JSON tokens vs TOON tokens** for the same content. citeturn4view0turn4view1
- Display **savings percentage**. citeturn4view0turn4view1
- Estimate **dollar costs** based on prices per million tokens (e.g., `30/60 USD per 1M tokens` for GPT‑5 input/output in the example UI). citeturn4view1

These metrics are only for **planning and comparison**, not to exactly reproduce each model's proprietary tokenizer.

### 2.2 Base token estimation rule

The json2toon-optimizer FAQ explicitly documents how the counter works: citeturn4view0

- **Central rule**:
  > “Our token counter uses a standard estimate (approximately 1 token every 4 characters)”

That is, the token count **does not use** the model's actual tokenizer, but rather an _estimator_ based on character count.

Practical estimator rule (formulated from the description):

1. Count the total number of input **characters** (`chars`).
2. Estimate the number of **tokens** as something close to `chars / 4`.
3. This estimate is used for both JSON and TOON.
4. Token savings are calculated by **comparing the two estimates**.

> Inference: the exact formula is not published, but it is reasonable to assume something like `tokens_est = ceil(chars / 4)` or similar rounding, since the interface shows integer token values and not fractions.

### 2.3 Metrics displayed by the token‑counter

In the token‑counter interfaces linked to TOON, at least the following fields appear: citeturn4view1turn4view0

For the current text (JSON or TOON):

- **Characters** – number of characters (e.g., `Characters: 114`).
- **Words** – word count (e.g., `Words: 17`).
- **Lines** – number of lines (e.g., `Lines: 6`).
- **Total Tokens** – token estimate (e.g., `Total Tokens: 45`).

For JSON vs TOON comparison (in conversion context):

- `JSON: <N_JSON> tokens`
- `TOON: <N_TOON> tokens`
- `Saved: <N_JSON - N_TOON> tokens`
- `TOON Savings: <percentage>%` – savings in percentage. citeturn4view1turn4view0

Explicit percentage calculation rule (deduced from shown fields):

```text
TOON_Savings_% = 100 * (JSON_tokens - TOON_tokens) / JSON_tokens
```

> Inference: the formula does not appear literally, but it is the only one that simultaneously explains “JSON: 45 tokens / TOON: 23 tokens / Savings: 48.9%” in the example UI. citeturn4view1

### 2.4 Rules for cost calculation

The tools also display approximate cost, as on the Token Counter & Cost Calculator screen: citeturn4view1

- Fields presented:
  - **GPT‑5 Cost**
  - `Input: $…`
  - `Output: $…`
  - Text “Based on $30/$60 per 1M tokens”

Implicit calculation rules (from the interface):

1. The user chooses or the tool assumes **rates per 1M tokens** for input and output (e.g., `30 USD` for input, `60 USD` for output).
2. The counter estimates the number of **input tokens** and **output tokens** for the snippet under analysis (or just input, depending on the case).
3. The cost is calculated proportionally:
   - `cost_input ≈ (input_tokens / 1_000_000) * price_per_M_input`
   - `cost_output ≈ (output_tokens / 1_000_000) * price_per_M_output`
4. The displayed “GPT‑5 Cost” value is the sum or main focus of the estimate (depends on the specific screen). citeturn4view1

> Inference: the formula is standard for all token cost calculators, even if not appearing explicitly in the text.

### 2.5 Scope and limitations of counting

According to the json2toon-optimizer FAQ, the count is **approximate**: citeturn4view0

- The goal is to **compare JSON vs TOON**, not to match 100% with the official tokenizer.
- The character-based estimate tends to be consistent enough to measure **relative savings**.
- Different models have their own tokenization rules; the absolute difference in tokens may vary, but the percentage savings usually remain similar.

Other documented features:

- All processing is **100% client‑side** – the text does not leave the browser. citeturn4view0turn4view1
- The token‑counter works both in JSON→TOON converters and in an isolated “Token Counter & Cost Calculator” tool. citeturn4view1turn4view0

---

## 3. JSON → TOON conversion rules (json‑to‑toon)

Here enter both the TypeScript API (`encode`) and the `@toon-format/cli` CLI behavior documented in the main repository README. citeturn5view0turn11view3

### 3.1 `encode` API – overview

The main conversion function is:

```ts
encode(value: unknown, options?: EncodeOptions): string
```

Documented rules: citeturn2view2

1. **Input (`value`)**

   - Can be any **JSON‑serializable** value:
     - Objects
     - Arrays
     - Primitives (string, number, boolean, null)
     - Nested structures
   - Non-JSON‑serializable values are normalized (see section 3.6).

2. **Options (`EncodeOptions`)**

   - `indent?: number` – amount of spaces per indentation level (default `2`). citeturn2view2
   - `delimiter?: ',' | '\t' | '|'` – delimiter used in arrays and tabular rows (default `','`). citeturn2view2
   - `keyFolding?: 'off' | 'safe'` – enables “key folding” to collapse key chains into dot paths (default `'off'`). citeturn2view2turn2view2
   - `flattenDepth?: number` – maximum number of segments that can be collapsed when using `keyFolding` (default `Infinity`). citeturn2view2

3. **Output**
   - Returns a string in TOON format **without trailing newline or extra spaces**. citeturn2view2

### 3.2 JSON Objects → TOON blocks

#### 3.2.1 Simple objects

Example in README: citeturn2view2

JSON:

```ts
encode({
  id: 123,
  name: "Ada",
  active: true,
});
```

Resulting TOON:

```text
id: 123
name: Ada
active: true
```

Implicit rules:

- Each **key/value pair** becomes **one line** `key: value`.
- The **key order** is preserved relative to the original object.
- There are no repeated keys, as the data model is the same as JSON.

#### 3.2.2 Nested objects

Example: citeturn2view2turn11view3

JSON:

```ts
encode({
  user: {
    id: 123,
    name: "Ada",
  },
});
```

TOON:

```text
user:
  id: 123
  name: Ada
```

Rules:

1. When the value is an **object**, the key appears alone followed by `:` and **without value on the same line**.
2. Internal keys are printed **indented** by the number of spaces defined in `indent` (default: 2).
3. This pattern repeats recursively for deeper objects.

#### 3.2.3 Empty objects

Explicit rules for empty objects: citeturn11view4turn11view3

- `encode({})` – produces **empty output** (no lines).
- `encode({ config: {} })` – produces:

  ```text
  config:
  ```

  that is, the key is emitted, but without nested fields.

### 3.3 JSON Arrays → TOON arrays

TOON has three main ways to encode arrays: citeturn2view2turn11view3

1. **Arrays of primitives (inline)**
2. **Arrays of uniform objects (tabular)**
3. **Mixed or non-uniform arrays (list)**
4. **Arrays of arrays** (special case)
5. **Root arrays and empty arrays**

#### 3.3.1 Array header

Every array in TOON has a **header with length**:

- General: `name[LEN]: ...`
- For tabular arrays of objects: `name[LEN]{fields...}:` citeturn2view2turn2view2

Additionally:

- The length `LEN` is the **number of elements** in the array.
- This number must match the actual quantity of rows/values – otherwise, the decoder in **strict mode** throws an error (see 3.7). citeturn2view2

#### 3.3.2 Arrays of primitives (inline)

Example: citeturn2view2turn11view3

JSON:

```ts
encode({
  tags: ["admin", "ops", "dev"],
});
```

TOON:

```text
tags[3]: admin,ops,dev
```

Rules:

1. Arrays where **all elements are primitives** (string, number, boolean, null) are encoded **in a single line**.
2. The line contains:
   - `name[LEN]:`
   - List of values separated by the **active delimiter** (default: comma).
3. The delimiter is **implied** by the header when it is comma. When using tab or pipe, it is explicit (see 3.5). citeturn2view2

#### 3.3.3 Arrays of uniform objects (tabular format)

Example: citeturn2view2turn2view2

JSON:

```ts
encode({
  items: [
    { sku: "A1", qty: 2, price: 9.99 },
    { sku: "B2", qty: 1, price: 14.5 },
  ],
});
```

TOON:

```text
items[2]{sku,qty,price}:
  A1,2,9.99
  B2,1,14.5
```

Rules for the array to be considered **tabular**:

1. All array elements are **objects**. citeturn2view2
2. All these objects have **the same set of keys** (internal key order doesn't need to be the same, only the set). citeturn2view2
3. All values associated with keys are **primitives** (no nested objects or arrays). citeturn2view2

When these conditions are met:

- The header has the form: `name[LEN]{field1,field2,...}:`
- Each row below contains **only the values**, in the **order of fields declared in the header**, separated by the active delimiter.
- There are no repeated keys in each row – this is what generates token savings.

Tabular also works **recursively** in nested arrays, if the condition holds: citeturn2view2

```ts
encode({
  items: [
    {
      users: [
        { id: 1, name: "Ada" },
        { id: 2, name: "Bob" },
      ],
      status: "active",
    },
  ],
});
```

Generates, in essence:

```text
items[1]:
  - users[2]{id,name}:
    1,Ada
    2,Bob
    status: active
```

#### 3.3.4 Mixed or non-uniform arrays (list)

When the array **does not** meet tabular rules (mix of types, different objects, objects with non-primitive values etc.), encoding falls back to **list** format: citeturn2view2turn11view3

Example:

```ts
encode({
  items: [1, { a: 1 }, "text"],
});
```

TOON:

```text
items[3]:
  - 1
  - a: 1
  - text
```

List format rules:

1. The header is `name[LEN]:` (without `{fields}` because items are not uniform).
2. Each element is an entry starting with `- ` (hyphen and space).
3. If the element is:
   - **primitive** → goes directly after the hyphen (`- 1`).
   - **object** → the first key can go on the same line (`- id: 1`), others come indented on the line below. citeturn2view2
   - **array** → see “nested array indentation” rules below.

##### 3.3.4.1 “Nested array indentation”

When the first field of a list item is an **array**, the specification defines special rules: citeturn11view4

- The array content is **indented two spaces** below the item header.
- Other fields of the same object appear with the **same indentation**.
- Syntax remains unambiguous because:
  - list items start with `"- "`
  - tabular arrays declare size and fields in header
  - object fields always carry `":"`

#### 3.3.5 Arrays of arrays

Case with arrays of primitives **inside** an array: citeturn11view4turn11view3

JSON:

```ts
encode({
  pairs: [
    [1, 2],
    [3, 4],
  ],
});
```

TOON:

```text
pairs[2]:
  - [2]: 1,2
  - [2]: 3,4
```

Rules:

- The outer array is treated as **list** (`pairs[2]:` + items with `-`).
- Each list item is an array of primitives, encoded in the form `[LEN]: v1,v2,...`.
- The length `[2]` in the example indicates the number of elements in each inner pair.

#### 3.3.6 Root arrays

Cheatsheet: citeturn11view3

JSON:

```json
["x", "y"]
```

TOON:

```text
[2]: x,y
```

Rules:

- A root array, when of primitives, uses the header `[LEN]:` **without field name**, followed by the list of delimited values.
- For object/mixed arrays at the root, the same tabular/list logic described above applies, just without the field name.

#### 3.3.7 Empty arrays

Explicit rules: citeturn11view4turn11view3

- `encode({ items: [] })` → `items[0]:`
- `encode([])` → `[0]:`
- Empty arrays always display length `0` in the header, with no values after the colon.

### 3.4 “Key Folding” Rules (key collapse)

“Key folding” is an optional feature introduced in spec v1.5, and configured by the option `keyFolding: 'safe'`. citeturn2view2turn2view2

#### 3.4.1 Reason

- Decrease **indentation levels** and **key length** by joining object chains with **only one key** into a dot path (`data.metadata.items`). citeturn2view2

#### 3.4.2 Transformation example

Without key folding: citeturn2view2

```text
data:
  metadata:
    items[2]: a,b
```

With `keyFolding: 'safe'`:

```text
data.metadata.items[2]: a,b
```

#### 3.4.3 Safety rules

If `keyFolding` is set to `'safe'`: citeturn2view2turn11view2

- Only key segments that **match the valid identifier pattern** can be folded:
  - Start with letter or `_`
  - Followed by letters, digits, `_` or `.`
- Key chains are folded only if they don't generate ambiguity in re-expansion (formal details are in the spec; README references §13.4 of the specification). citeturn2view2
- `flattenDepth` limits how many segments can be collapsed (default: `Infinity`). Values `0` or `1` practically disable the effect. citeturn2view2

#### 3.4.4 Round‑trip with `expandPaths`

To reconstruct the original JSON, the `decode` API offers `expandPaths: 'safe'`: citeturn2view2

- `encode` with `keyFolding: 'safe'` generates keys like `data.metadata.items[2]: ...`.
- `decode` with `expandPaths: 'safe'` reassembles the nested structure `{ data: { metadata: { items: [...] } } }`.
- The README guarantees that this combination returns a structure equivalent to the original (lossless). citeturn2view2

### 3.5 Delimiter rules (`delimiter`)

`delimiter` option in `encode`: citeturn2view2

- Possible values: `','` (default), `'\t'` (tab) and `'|'` (pipe).
- Affects:
  - Arrays of primitives (inline)
  - Tabular arrays of objects (data rows and header)

#### 3.5.1 Comma delimiter (default)

- Header: `items[2]{sku,qty,price}:`
- Rows: `A1,2,9.99` etc. citeturn2view2

#### 3.5.2 Tab delimiter (`'\t'`)

Example: citeturn2view2

```ts
encode(data, { delimiter: "\t" });
```

Generates something like:

```text
items[2	]{sku	name	qty	price}:
  A1	Widget	2	9.99
  B2	Gadget	1	14.5
```

Rules:

- The header includes the delimiter explicitly after the length (`[2\t]`).
- Values in header and rows are separated by **tab**.
- Mentioned benefits:
  - Tabs usually tokenize better than commas.
  - Tabs rarely appear in normal text, reducing the need for quotes. citeturn2view2

#### 3.5.3 Pipe delimiter (`'|'`)

Example: citeturn2view2

```text
items[2|]{sku|name|qty|price}:
  A1|Widget|2|9.99
  B2|Gadget|1|14.5
```

Rules:

- The pipe appears in both header and rows as separator.
- Balances readability and token efficiency against comma and tab.

### 3.6 Type conversion rules (normalization)

The “Type Conversions” section of the README defines how values outside the pure JSON model are treated before serialization: citeturn2view2

Table:

| Input type                      | TOON Output / JSON‑equivalent                                           |
| ------------------------------- | ----------------------------------------------------------------------- |
| Finite number (`number`)        | Decimal form, no scientific notation (e.g., `1e6 → 1000000`, `-0 → 0`). |
| `NaN`, `+Infinity`, `-Infinity` | Converted to `null`.                                                    |
| `BigInt` within safe range      | Converted to normal number.                                             |
| `BigInt` outside safe range     | Emitted as decimal string **in quotes**.                                |
| `Date`                          | ISO String (`"2025-01-01T00:00:00.000Z"`), with quotes.                 |
| `undefined`                     | `null`.                                                                 |
| `function`                      | `null`.                                                                 |
| `symbol`                        | `null`.                                                                 |

These rules ensure the result is always **json‑compatible**, even if the original value comes from a broader JavaScript context.

### 3.7 Quoting rules for keys and values

TOON avoids quotes whenever possible to reduce tokens, but imposes clear rules to avoid ambiguity. citeturn11view2turn11view4

#### 3.7.1 General principles

- Strings are only quoted **when necessary**.
- Internal spaces are allowed without quotes; spaces **at start or end** require quotes.
- Unicode and emoji can stay **without quotes**.
- Quotes and control characters are escaped with backslash. citeturn11view2

#### 3.7.2 Object keys / field names

A key can be **unquoted** if it obeys the identifier pattern: citeturn11view2

- Starts with letter or `_`.
- Follows with letters, digits, `_` or `.`.

Valid unquoted examples:

- `id`
- `userName`
- `user_name`
- `user.name`
- `_private`

Any other key must be **quoted**:

- `"user name"`
- `"order-id"`
- `"123"`
- `"order:id"`
- `""` (empty string)

#### 3.7.3 String values

String values are quoted if **any** of the conditions below is true: citeturn11view2

1. The string is empty: `""`.
2. Has space at start or end: `" padded "`, `" "`.
3. Contains:
   - The **active delimiter** (comma, tab or pipe),
   - Colon `:`,
   - Quotes `"`,
   - Backslash `\`,
   - Control characters (like `\n`).
4. “Looks like” boolean, number or `null`:
   - `"true"`, `"false"`, `"null"`, `"42"`, `"-3.14"`, `"1e-6"`, `"05"`.
5. Starts with `"- "` (could be confused with list item).
6. Looks like structural token:
   - `"[5]"`, `"{key}"`, `"[3]: x,y"` etc.

Strings without these issues can be emitted **without quotes**, including with internal spaces:

- `hello world`
- `data analysis`
- Emojis and Unicode in general.

#### 3.7.4 Delimiter and quotes

Important parsing robustness rule: citeturn11view2

- Strings **without quotes never contain** `:` nor the active delimiter.
- This allows simple parsing:
  - Separate key/value with `split(":", 1)`.
  - Separate array values using the delimiter declared in the header.

When you change the delimiter (to tab or pipe):

- Quoting rules adapt: the string only needs quotes if it contains **the active delimiter**; commas become “safe” if they are not the current delimiter. citeturn11view2

### 3.8 `decode` decoder rules (TOON → JSON)

Although the focus is JSON → TOON, the README also documents the reverse path, which guarantees the **reversibility** of the above rules. citeturn2view2

Signature:

```ts
decode(input: string, options?: DecodeOptions): JsonValue
```

Relevant options:

- `indent?: number` – expected indentation width (default `2`).
- `strict?: boolean` – strict validation (default `true`).
- `expandPaths?: 'off' | 'safe'` – expands folded keys (see 3.4). citeturn2view2

Validation rules in strict mode: citeturn2view2

1. **Invalid escape sequences** (`"\x"`, unterminated strings) → error.
2. **Syntax errors** (missing colons, malformed headers etc.) → error.
3. **Inconsistent array length** – if `[LEN]` doesn't match the quantity of elements, the decoder fails.
4. **Inconsistent delimiter** – if rows don't follow the delimiter specified in the header, error.

This validation ensures that any TOON decoded in strict mode results in “well-formed” JSON within the specified rules.

### 3.9 `@toon-format/cli` CLI rules for JSON ↔ TOON

The CLI exposed in the README is a wrapper on top of the `encode/decode` API. citeturn2view2turn2view2

#### 3.9.1 Mode auto‑detection (encode vs decode)

Rules: citeturn2view2

- If the **input file** has `.json` extension → CLI assumes **encode** (JSON → TOON).
- If it has `.toon` extension → CLI assumes **decode** (TOON → JSON).
- When input comes from **stdin** (no file or with `-`), you can (and should) specify:
  - `--encode` – forces encode.
  - `--decode` – forces decode.
- In stdin, default mode is encode if no flag is passed.

#### 3.9.2 Options relevant to conversion / token counting

- `-o, --output <file>` – output file (if omitted, writes to stdout). citeturn2view2
- `-e, --encode` – forces encode mode. citeturn2view2
- `-d, --decode` – forces decode mode. citeturn2view2
- `--delimiter <char>` – array/tabular row delimiter (`,`, `\t` or `|`). citeturn2view2
- `--indent <number>` – indentation size. citeturn2view2
- `--stats` – shows **token statistics and savings** when encoding (JSON → TOON). citeturn2view2
- `--no-strict` – disables strict validation when decoding. citeturn2view2
- `--key-folding <mode>` – enables key folding (`off` or `safe`). citeturn2view2
- `--flatten-depth <number>` – key folding depth limit. citeturn2view2
- `--expand-paths <mode>` – enables path expansion (`off` or `safe`) when decoding. citeturn2view2

#### 3.9.3 Typical JSON → TOON flows with statistics

README examples: citeturn2view2

```bash
# Encode with stats (JSON → TOON) and save to file
npx @toon-format/cli data.json --stats -o output.toon

# Encode using tab as delimiter, redirecting to file
cat large-dataset.json | npx @toon-format/cli --delimiter "\t" > output.toon
```

In these flows, the CLI:

1. Reads JSON.
2. Internally calls `encode` with specified options.
3. Generates TOON.
4. If `--stats` is checked, calculates token statistics and savings based on the same estimate used by web tools (approx. 1 token every 4 characters). citeturn4view0turn4view1turn2view2

---

## 4. Consolidated Cheatsheet: JSON → TOON in simple rules

Based on official examples, the cheatsheet can be rewritten as direct rules: citeturn11view3turn2view2

1. **Simple object**

   - JSON `{ id: 1, name: 'Ada' }` →
     TOON:
     ```text
     id: 1
     name: Ada
     ```

2. **Nested object**

   - JSON `{ user: { id: 1 } }` →
     TOON:
     ```text
     user:
       id: 1
     ```

3. **Array of primitives (field)**

   - JSON `{ tags: ['foo', 'bar'] }` →
     TOON:
     ```text
     tags[2]: foo,bar
     ```

4. **Array of uniform objects**

   - JSON:
     ```json
     {
       "items": [
         { "id": 1, "qty": 5 },
         { "id": 2, "qty": 3 }
       ]
     }
     ```
   - TOON:
     ```text
     items[2]{id,qty}:
       1,5
       2,3
     ```

5. **Mixed / non-uniform array**

   - JSON `{ items: [1, { "a": 1 }, "x"] }` →
     TOON:
     ```text
     items[3]:
       - 1
       - a: 1
       - x
     ```

6. **Array of arrays**

   - JSON `{ pairs: [[1, 2], [3, 4]] }` →
     TOON:
     ```text
     pairs[2]:
       - [2]: 1,2
       - [2]: 3,4
     ```

7. **Root array**

   - JSON `["x", "y"]` →
     TOON:
     ```text
     [2]: x,y
     ```

8. **Empty containers**

   - JSON `{}` → empty output.
   - JSON `{ "items": [] }` → `items[0]:`
   - JSON `[]` → `[0]:`
   - JSON `{ "config": {} }` →
     ```text
     config:
     ```

9. **Special quotes**
   - JSON `{ note: 'hello, world' }` →
     TOON:
     ```text
     note: "hello, world"
     ```
     because the string contains a comma (default delimiter). citeturn11view3turn11view2
   - JSON `{ items: ['true', true] }` →
     TOON:
     ```text
     items[2]: "true",true
     ```
     because `"true"` without quotes could be confused with literal boolean.

---

## 5. What is _not_ explicitly documented

- The project **does not publish** the exact rounding algorithm for token estimation (e.g., whether it is `ceil(chars/4)` or another method). It only states “approximately 1 token per 4 characters”. citeturn4view0
- The full specification (SPEC.md) contains formal grammar (ABNF), but the environment here only allows partial access to content, so all fine details depending exclusively on SPEC were not reproduced word for word; I focused on what is clearly available in the README, cheatsheet and tools FAQ. citeturn7search0turn5view0turn4view0

Even with these limitations, all **explicit** rules appearing in accessible sources about:

- token counting, and
- JSON → TOON conversion

were included in this summary, without skipping any point that was clearly described.

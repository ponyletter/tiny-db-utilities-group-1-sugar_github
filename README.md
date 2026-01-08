# TinyDB Tool

A command-line utility suite for manipulating TinyDB JSON database files.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd tinydb-utility

# Install dependencies
pip install tinydb
```

## Quick Start

```bash
# List all documents
python -m tinydb_tool.main list --file db.json

# Insert a document
python -m tinydb_tool.main insert --file db.json --data '{"name": "john", "age": 30}'

# Query documents
python -m tinydb_tool.main query --file db.json --where 'name == "john"'

# Update documents
python -m tinydb_tool.main update --file db.json --where 'name == "john"' --data '{"age": 31}'

# Delete documents
python -m tinydb_tool.main delete --file db.json --where 'name == "john"'
```

## Commands

### `list` - List all documents

Display all documents in the database.

```bash
python -m tinydb_tool.main list --file db.json
python -m tinydb_tool.main list --file db.json --no-pretty
```

**Options:**
- `--file`: Path to database file (required)
- `--no-pretty`: Disable pretty formatting

### `insert` - Insert documents

Add one or more documents to the database.

```bash
# From command line
python -m tinydb_tool.main insert --file db.json --data '{"name": "john"}'

# From file
python -m tinydb_tool.main insert --file db.json --file-input data.json
```

**Options:**
- `--file`: Path to database file (required)
- `--data`: JSON string (single object or array of objects)
- `--file-input`: Path to JSON file (mutually exclusive with --data)

### `query` - Search documents

Find documents matching a query condition.

```bash
python -m tinydb_tool.main query --file db.json --where 'name == "john"'
python -m tinydb_tool.main query --file db.json --where 'age != 30'
```

**Query Format:**
- `field == value` - Equal comparison
- `field != value` - Not equal comparison
- `field > value` - Greater than (numeric only)
- `field < value` - Less than (numeric only)
- `field >= value` - Greater than or equal (numeric only)
- `field <= value` - Less than or equal (numeric only)
- String values: Use quotes: `'name == "john"'`
- Numeric values: No quotes: `'age > 30'`

**Options:**
- `--file`: Path to database file (required)
- `--where`: Query condition (required)
- `--no-pretty`: Disable pretty formatting

### `update` - Update documents

Modify fields in documents matching a query.

```bash
python -m tinydb_tool.main update --file db.json --where 'name == "john"' --data '{"age": 31}'
```

**Options:**
- `--file`: Path to database file (required)
- `--where`: Query condition (required)
- `--data`: JSON object with fields to update (required)

### `delete` - Delete documents

Remove documents matching a query.

```bash
python -m tinydb_tool.main delete --file db.json --where 'name == "john"'
```

**Options:**
- `--file`: Path to database file (required)
- `--where`: Query condition (required)

## Examples

### Complete Workflow

```bash
# 1. Create database and insert data
python -m tinydb_tool.main insert --file db.json --data '{"name": "john", "age": 30}'

# 2. List all documents
python -m tinydb_tool.main list --file db.json

# 3. Query specific documents
python -m tinydb_tool.main query --file db.json --where 'age == 30'

# 4. Update documents
python -m tinydb_tool.main update --file db.json --where 'name == "john"' --data '{"age": 31}'

# 5. Delete documents
python -m tinydb_tool.main delete --file db.json --where 'name == "john"'
```

### Insert Multiple Documents

```bash
python -m tinydb_tool.main insert --file db.json --data '[{"name": "john"}, {"name": "jane"}]'
```

### Query with Different Value Types

```bash
# String comparison
python -m tinydb_tool.main query --file db.json --where 'status == "active"'

# Numeric comparison
python -m tinydb_tool.main query --file db.json --where 'age != 25'
python -m tinydb_tool.main query --file db.json --where 'age > 30'
python -m tinydb_tool.main query --file db.json --where 'price <= 100'
```

## Error Handling

The tool provides clear error messages for common issues:

- **File not found**: Database file or directory doesn't exist
- **Permission denied**: Cannot access the file
- **Invalid JSON**: JSON parsing errors with details
- **Invalid query**: Query format errors with format explanation

## Help

Get help for any command:

```bash
python -m tinydb_tool.main --help
python -m tinydb_tool.main list --help
python -m tinydb_tool.main insert --help
```

## Developer Documentation

See [DEVELOPER.md](DEVELOPER.md) for information on extending the tool suite.

## License

MIT License

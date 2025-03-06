import pytest
from app.services import index_files, parse_query, search_files
from app.models import File, Context

def test_index_files(tmp_path):
    # Create a temporary file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")
    
    # Index files
    index = index_files(tmp_path)
    assert len(index) == 1
    assert index[0].name == "test_file.txt"

def test_parse_query():
    query = "mullen lowe invoice march opex"
    context = parse_query(query)
    assert "mullen lowe" in context.entities
    assert "march" in context.entities
    assert context.intent == "invoice"

def test_search_files():
    files = [
        File(path="/path/to/file1", name="mullen_lowe_invoice_march_opex.txt", created="2023-01-01", modified="2023-01-01"),
        File(path="/path/to/file2", name="clientx_report_april_budget.docx", created="2023-01-01", modified="2023-01-01"),
    ]
    context = Context(entities=["mullen lowe", "march"], intent="invoice")
    results = search_files(files, context)
    assert len(results) == 1
    assert results[0].name == "mullen_lowe_invoice_march_opex.txt"
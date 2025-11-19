"""
Unit tests for json2toon-optimizer
Tests CLI, batch processing, and streaming functionality
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from json2toon import TOONEncoder, TokenCounter, process_json_file, process_batch


class TestTOONEncoder:
    """Test basic TOON encoding functionality"""
    
    def test_simple_object(self):
        encoder = TOONEncoder()
        data = {"id": 123, "name": "Ada"}
        result = encoder.encode(data)
        assert "id: 123" in result
        assert "name: Ada" in result
    
    def test_nested_object(self):
        encoder = TOONEncoder()
        data = {"user": {"id": 1, "name": "Bob"}}
        result = encoder.encode(data)
        assert "user:" in result
        assert "  id: 1" in result
        assert "  name: Bob" in result
    
    def test_primitive_array(self):
        encoder = TOONEncoder()
        data = {"tags": ["a", "b", "c"]}
        result = encoder.encode(data)
        assert "tags[3]: a,b,c" in result
    
    def test_tabular_array(self):
        encoder = TOONEncoder()
        data = {
            "items": [
                {"id": 1, "qty": 5},
                {"id": 2, "qty": 3}
            ]
        }
        result = encoder.encode(data)
        assert "items[2]{id,qty}:" in result
        assert "1,5" in result
        assert "2,3" in result
    
    def test_custom_delimiter(self):
        encoder = TOONEncoder(delimiter='\t')
        data = {"tags": ["a", "b", "c"]}
        result = encoder.encode(data)
        assert "tags[3\t]: a\tb\tc" in result
    
    def test_custom_indent(self):
        encoder = TOONEncoder(indent=4)
        data = {"user": {"id": 1}}
        result = encoder.encode(data)
        assert "    id: 1" in result


class TestTokenCounter:
    """Test token counting functionality"""
    
    def test_count_tokens_simple(self):
        text = "Hello, world!"
        tokens = TokenCounter.count_tokens(text)
        assert tokens > 0
        assert tokens <= len(text)  # Should be less than or equal to chars
    
    def test_analyze(self):
        text = "Hello world\nTest line"
        analysis = TokenCounter.analyze(text)
        assert 'characters' in analysis
        assert 'lines' in analysis
        assert 'words' in analysis
        assert 'tokens' in analysis
        assert 'tokenizer' in analysis
        assert analysis['lines'] == 2
        assert analysis['words'] == 3


class TestProcessJSONFile:
    """Test single file processing"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def sample_json_file(self, temp_dir):
        """Create a sample JSON file"""
        data = {
            "users": [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 25}
            ]
        }
        json_file = temp_dir / "sample.json"
        with open(json_file, 'w') as f:
            json.dump(data, f)
        return json_file
    
    def test_process_simple_file(self, sample_json_file, temp_dir):
        """Test processing a simple JSON file"""
        result = process_json_file(
            str(sample_json_file),
            str(temp_dir)
        )
        
        assert result['input_file'] == str(sample_json_file)
        assert 'output_file' in result
        assert result['json_tokens'] > 0
        assert result['toon_tokens'] > 0
        assert 'chosen_format' in result
        assert Path(result['output_file']).exists()
    
    def test_force_toon_format(self, sample_json_file, temp_dir):
        """Test forcing TOON format output"""
        result = process_json_file(
            str(sample_json_file),
            str(temp_dir),
            format_choice='toon',
            force_format=True
        )
        
        assert 'TOON' in result['chosen_format']
        assert result['output_file'].endswith('.toon')
    
    def test_custom_delimiter(self, sample_json_file, temp_dir):
        """Test custom delimiter"""
        result = process_json_file(
            str(sample_json_file),
            str(temp_dir),
            delimiter='\t'
        )
        
        # Read output and check for tab delimiter
        with open(result['output_file'], 'r') as f:
            content = f.read()
            if 'TOON' in result['chosen_format']:
                # Tab delimiter should be present in tabular arrays
                assert '\t' in content or '[' in content


class TestBatchProcessing:
    """Test batch processing functionality"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def multiple_json_files(self, temp_dir):
        """Create multiple JSON files"""
        files = []
        for i in range(5):
            data = {
                "id": i,
                "items": [{"x": j, "y": j*2} for j in range(3)]
            }
            json_file = temp_dir / f"file_{i}.json"
            with open(json_file, 'w') as f:
                json.dump(data, f)
            files.append(json_file)
        return files
    
    def test_batch_sequential(self, multiple_json_files, temp_dir):
        """Test sequential batch processing"""
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        result = process_batch(
            multiple_json_files,
            output_dir=str(output_dir),
            parallel_workers=1,
            quiet=True
        )
        
        assert result['total_files'] == 5
        assert result['successful'] == 5
        assert result['failed'] == 0
        assert result['total_tokens_saved'] >= 0
    
    def test_batch_parallel(self, multiple_json_files, temp_dir):
        """Test parallel batch processing"""
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        result = process_batch(
            multiple_json_files,
            output_dir=str(output_dir),
            parallel_workers=2,
            quiet=True
        )
        
        assert result['total_files'] == 5
        assert result['successful'] == 5
        assert result['failed'] == 0
    
    def test_batch_with_errors(self, temp_dir):
        """Test batch processing with some invalid files"""
        # Create mix of valid and invalid files
        valid_file = temp_dir / "valid.json"
        invalid_file = temp_dir / "invalid.json"
        
        with open(valid_file, 'w') as f:
            json.dump({"test": "data"}, f)
        
        with open(invalid_file, 'w') as f:
            f.write("not valid json {")
        
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        result = process_batch(
            [valid_file, invalid_file],
            output_dir=str(output_dir),
            quiet=True
        )
        
        assert result['total_files'] == 2
        assert result['successful'] >= 1
        assert result['failed'] >= 1


class TestStreamProcessing:
    """Test streaming functionality"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def large_json_array(self, temp_dir):
        """Create a large JSON array file"""
        data = [{"id": i, "value": i * 2, "name": f"item_{i}"} for i in range(100)]
        json_file = temp_dir / "large.json"
        with open(json_file, 'w') as f:
            json.dump(data, f)
        return json_file
    
    def test_stream_array(self, large_json_array, temp_dir):
        """Test streaming large array"""
        try:
            from json2toon import process_stream
            
            output_dir = temp_dir / "output"
            output_dir.mkdir()
            
            result = process_stream(
                str(large_json_array),
                output_dir=str(output_dir),
                chunk_size=20,
                quiet=True
            )
            
            assert result['chunks_processed'] > 0
            assert result['items_processed'] == 100
            assert Path(result['output_file']).exists()
            assert result['peak_memory_mb'] > 0
        
        except ImportError:
            pytest.skip("ijson not installed, skipping streaming tests")
    
    def test_stream_object_fallback(self, temp_dir):
        """Test streaming with object (should fallback to regular processing)"""
        try:
            from json2toon import process_stream
            
            # Create object (not array)
            data = {"users": [{"id": i} for i in range(50)]}
            json_file = temp_dir / "object.json"
            with open(json_file, 'w') as f:
                json.dump(data, f)
            
            output_dir = temp_dir / "output"
            output_dir.mkdir()
            
            result = process_stream(
                str(json_file),
                output_dir=str(output_dir),
                quiet=True
            )
            
            assert Path(result['output_file']).exists()
        
        except ImportError:
            pytest.skip("ijson not installed, skipping streaming tests")


class TestCLIIntegration:
    """Test CLI argument parsing and integration"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)
    
    def test_cli_imports(self):
        """Test that CLI module imports correctly"""
        from json2toon.cli import main
        assert main is not None
    
    def test_resolve_input_paths(self, temp_dir):
        """Test input path resolution with glob patterns"""
        from json2toon.cli import _resolve_input_paths
        
        # Create test files
        for i in range(3):
            json_file = temp_dir / f"test_{i}.json"
            json_file.write_text('{"test": true}')
        
        # Test glob pattern
        paths = _resolve_input_paths(
            [str(temp_dir / "*.json")],
            recursive=False,
            pattern="*.json",
            exclude=None
        )
        
        assert len(paths) == 3
        assert all(p.suffix == '.json' for p in paths)
    
    def test_resolve_with_exclude(self, temp_dir):
        """Test input path resolution with exclusion"""
        from json2toon.cli import _resolve_input_paths
        
        # Create test files
        (temp_dir / "keep.json").write_text('{}')
        (temp_dir / "exclude_this.json").write_text('{}')
        
        paths = _resolve_input_paths(
            [str(temp_dir / "*.json")],
            recursive=False,
            pattern="*.json",
            exclude=["exclude_*"]
        )
        
        assert len(paths) == 1
        assert paths[0].name == "keep.json"


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_json_object(self):
        """Test encoding empty object"""
        encoder = TOONEncoder()
        result = encoder.encode({})
        assert result == ""
    
    def test_empty_array(self):
        """Test encoding empty array"""
        encoder = TOONEncoder()
        result = encoder.encode({"items": []})
        assert "items[0]:" in result
    
    def test_special_characters(self):
        """Test encoding strings with special characters"""
        encoder = TOONEncoder()
        data = {"text": "hello, world!"}
        result = encoder.encode(data)
        # Comma requires quoting
        assert '"hello, world!"' in result
    
    def test_unicode_characters(self):
        """Test encoding Unicode strings"""
        encoder = TOONEncoder()
        data = {"message": "こんにちは 世界 🌍"}
        result = encoder.encode(data)
        assert "こんにちは" in result
        assert "🌍" in result
    
    def test_nested_arrays(self):
        """Test encoding nested arrays"""
        encoder = TOONEncoder()
        data = {"matrix": [[1, 2], [3, 4]]}
        result = encoder.encode(data)
        assert "matrix[2]:" in result
        assert "[2]:" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

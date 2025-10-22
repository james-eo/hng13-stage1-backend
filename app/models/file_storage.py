import json
import os


class FileStorage:
    """File storage class for string data"""
    def __init__(self, file_path="data/strings.json"):
        """Initialize FileStorage with the given file path"""
        self.file_path = file_path
        self.ensure_data_dir()

    def ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def all(self):
        """Get all stored objects"""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_object(self, key, obj):
        """Save an object with the given key"""
        data = self.all()
        data[key] = obj
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_object(self, key):
        """Get object by key"""
        data = self.all()
        return data.get(key)

    def exists(self, key):
        """Check if key exists"""
        data = self.all()
        return key in data

    def delete_object(self, key):
        """Delete object by key"""
        data = self.all()
        if key in data:
            del data[key]
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)

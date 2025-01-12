import json

class ConfigLoader:
    """
    Utility to load configuration from a JSON file.
    """
    @staticmethod
    def load_config(file_path="config.json"):
        """
        Load configuration from a JSON file.
        :param file_path: Path to the JSON configuration file.
        :return: Configuration as a dictionary.
        """
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading config: {e}")
            return None

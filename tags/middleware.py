import json
from datetime import datetime , timezone
import os
from pathlib import Path  # Better path handling

# Use raw strings (r"") or forward slashes for Windows paths
PICKED_FILE_PATH = os.path.join("tagproject", "picked_files.json")
PICKED_FILE_PATH_MED = os.path.join("tagproject", "picked_files_med.json")
PICKED_FILE_PATH_FIN = os.path.join("tagproject", "picked_files_fin.json")
STALE_TIMEOUT_MINUTES = 10

class ReleaseStalePicksMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.release_stale_picks()
        return self.get_response(request)

    def _process_file(self, file_path):
        """Helper to process a single JSON file."""
        if not os.path.exists(file_path):
            return

        try:
            # Check if file is empty
            if os.path.getsize(file_path) == 0:
                # Create empty dictionary if file is empty
                with open(file_path, "w") as f:
                    json.dump({}, f)
                return

            with open(file_path, "r+") as f:
                data = json.load(f)
                now = datetime.now(timezone.utc)
                updated = {}

                for file, info in data.items():
                    if not isinstance(info, dict):
                        continue  # Skip non-dict entries

                    if info.get("permanent", True):
                        updated[file] = info
                        continue

                    picked_at_str = info.get("picked_at")
                    if not picked_at_str:
                        continue  # Skip if no timestamp

                    picked_at = datetime.fromisoformat(picked_at_str)
                    if (now - picked_at).total_seconds() / 60 <= STALE_TIMEOUT_MINUTES:
                        updated[file] = info
                        print("here",file)
                    print("middleware:",now,picked_at,file,(now - picked_at).total_seconds() / 60)

                f.seek(0)
                f.truncate()
                json.dump(updated, f, indent=2)
        except json.JSONDecodeError:
            # Handle the case where the file exists but contains invalid JSON
            with open(file_path, "w") as f:
                json.dump({}, f)
            print(f"Invalid JSON in file: {file_path} - Reset to empty dict")
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

    def release_stale_picks(self):
        try:
            # Process each file separately
            self._process_file(PICKED_FILE_PATH)
            self._process_file(PICKED_FILE_PATH_MED)
            self._process_file(PICKED_FILE_PATH_FIN)
        except PermissionError:
            print("Permission denied while accessing files.")
        except Exception as e:
            print(f"Unexpected error in release_stale_picks: {e}")
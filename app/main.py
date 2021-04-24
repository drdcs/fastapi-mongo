import uvicorn
import sys
import os

# The below code is to find the path for the driver program.
# This will remove module not found error.

cwd = os.getcwd()
sys.path.insert(0, cwd)

if __name__ == '__main__':
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
    
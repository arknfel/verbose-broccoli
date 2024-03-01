import os
import sys
# This fixes the import path so test files can import code
# the same way Lambda does when running on AWS
sys.path.append(os.path.join(sys.path[0], 'src'))

from flask import Flask, request
import subprocess
from spiders import scrapy_spider
import os

app = Flask(__name__)

@app.route('/trigger_scrapy', methods=['POST'])
def trigger_scrapy():
    spider_file = os.path.join(os.path.dirname(__file__), 'spiders', 'scrapy_spider.py')

    if not os.path.isfile(spider_file):
        return f"Error: Spider file not found at {spider_file}", 500
    print(f"Spider file path: {spider_file}")

    try:
        subprocess.Popen(['scrapy', 'runspider', 'scrapy_spider.py'])
    except Exception as e:
        print(f"Error running spider: {e}")
        return f"Error running spider: {e}", 500
    
    return 'Scrapy spider triggered', 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# from flask import Flask, request
# import subprocess
# import os
# import sys

# app = Flask(__name__)

# @app.route('/trigger_scrapy', methods=['POST'])
# def trigger_scrapy():
#     spider_file = os.path.join(os.path.dirname(__file__), 'scrapy_spider', 'spiders', 'scrapy_spider.py')
#     scrapy_executable = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'scrapy.exe')

#     print(f"Spider file: {spider_file}")
#     print(f"Scrapy executable: {scrapy_executable}")
#     print('********************************************************')

#     scrapy_project_dir = os.path.join(os.path.dirname(__file__), 'scrapy_spider')

#     try:
#         result = subprocess.run([scrapy_executable, 'runspider', spider_file], cwd=scrapy_project_dir, check=True, capture_output=True, text=True)
#         print(result.stdout)
#         print(result.stderr)
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#         return f"Error: {e}", 500
#     except subprocess.CalledProcessError as e:
#         print(f"Scrapy error: {e.stdout}\n{e.stderr}")
#         return f"Scrapy error: {e.stdout}\n{e.stderr}", 500

#     return 'Scrapy spider triggered', 200

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)


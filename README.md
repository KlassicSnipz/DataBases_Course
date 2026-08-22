## Quick Start

1. Clone the repo
2. Create a `.env` file in the project root:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password

3. Install dependencies:

pip install -r requirements.txt

4. Run the full pipeline:

python run_all.py

Push it all to GitHub
git add requirements.txt run_all.py README.md
git commit -m "Add requirements.txt and single-command pipeline runner for easier setup"
git push
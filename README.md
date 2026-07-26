1. Clone the repository
git clone https://github.com/yourusername/portfolio.git
cd portfolio
2. Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables
cp .env.example .env
# Edit .env with your settings
5. Seed the database
python seed_db.py
6. Run the development server
python run.py
Visit: http://localhost:5000

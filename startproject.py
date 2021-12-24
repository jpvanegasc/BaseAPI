"""
Usage: python3 startproject.py your_project_name
"""
import os
import sys
from dotenv import load_dotenv


def main():
    try:
        project_name = sys.argv[1]
    except IndexError:
        raise RuntimeError("project name not given")

    load_dotenv(".env.local")

    if os.getenv("DATABASE_URL"):
        db_url = os.getenv("DATABASE_URL")

        env = f"""PROJECT_NAME="{project_name}"\n"""
    else:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASS", "postgres")
        server = os.getenv("POSTGRES_SERVER", f"{project_name}_db")
        port = os.getenv("POSTGRES_PORT", "5000")
        db = os.getenv("POSTGRES_DB", project_name)

        db_url = f"postgresql://{user}:{password}@{server}:{port}/{db}"

        env = f"""PROJECT_NAME="{project_name}"\nDATABASE_URL="{db_url}"\n"""

    with open(".env", "w+") as f:
        f.write(env)

    os.system("cat .env.local >> .env")

    os.system(f'docker build -f local/Dockerfile -t {project_name}_backend .')
    os.system('docker-compose -f local/docker-compose.yml up -d')


if __name__ == "__main__":
    main()

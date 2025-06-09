FROM python:3.12

WORKDIR /home/ubuntu/flockerback

# Copy requirements and install dependencies first (for better caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Now copy the rest of your code BEFORE running scripts
COPY . .

# (Optional) Make scripts executable if you want to run them directly
# RUN chmod +x scripts/*.py

# Run your scripts using python (not as executables)
RUN python db_backup.py
RUN FORCE_DB_INIT=1 python scripts/db_init.py
RUN python scripts/db_restore.py

WORKDIR /

ENV GUNICORN_CMD_ARGS="--workers=3 --bind=0.0.0.0:8696"

EXPOSE 8696

# Define environment variable
ENV FLASK_ENV=deployed

CMD [ "gunicorn", "main:app" ]

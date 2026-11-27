FROM python:3.12-slim

WORKDIR /app

# Install test dependencies before copying source code
COPY pyproject.toml .
RUN pip install --no-cache-dir pytest pytest-bdd

# Copy project files
COPY . .

# Run the test suite
CMD ["pytest", "tests/", "-v", "--tb=short"]

docker-compose up --build -d

echo "Running tests in Docker container..."
docker-compose exec -T simple-scraper-test pytest -q

if [ $? -eq 0 ]; then
  echo "All tests passed successfully!"
  exit 0
else
  echo "Tests failed."
  exit 1
fi
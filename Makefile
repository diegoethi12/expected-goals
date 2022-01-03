docker-build:
	docker build -t expected-goals .

docker-run:
	docker run -p 8080:8080 expected-goals

cloud-run-deploy:
	gcloud run deploy expected-goals --image us-east1-docker.pkg.dev/dl-expected-goals/webapp/expected-goals:latest

artifact-registry-tag:
	docker tag expected-goals us-east1-docker.pkg.dev/dl-expected-goals/webapp/expected-goals

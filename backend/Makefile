.PHONY = generate-openapi

dev:
	python3 -m uvicorn server:app --reload-dir .

generate-openapi:
	curl http://localhost:8000/openapi.json | jq . > openapi.json

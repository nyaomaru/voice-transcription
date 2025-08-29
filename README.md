# voice-transcription

Voice transcription API

## Env

Setup env file using `.env.sample`

```sh
cp -p .env.sample .env
```

## Run

Use uvicorn to run this app.

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Curl example

With the server running, you can transcribe an audio file using `curl`:

```sh
curl -X 'POST' \
  'http://localhost:8000/transcribe' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@voice-test.mp3;type=audio/mpeg'
```

### API Docs

Interactive API documentation is available at http://localhost:8000/docs.
You can also access the raw OpenAPI spec at http://localhost:8000/openapi.json.

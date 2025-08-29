# voice-transcription

Voice transcription API

## Env

Setup env file using `.env.sample`

```sh
cp -p .env.sample .env
```

### Allowed Origins

By default, no origins are allowed for Cross-Origin Resource Sharing (CORS).
In production, specify the domains that should be permitted by setting the
`ALLOW_ORIGINS` environment variable. For example:

```sh
echo 'ALLOW_ORIGINS=["https://your.vercel.app"]' >> .env
```

Restart the application after updating the setting.

## Run

Use uvicorn to run this app.

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

Uploaded audio files are limited to **10&nbsp;MB**. Larger files will be
rejected with an HTTP `413 Payload Too Large` response.

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

# SR Info API

## Generating the server
1. Using the OpenAPI Generator docker image:
```bash
docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
                                                                      -i /local/service-request-info-spec.json \
                                                                      -g python-fastapi \
                                                                      -o /local/src/server/ \
                                                                      --additional-properties='packageName=coct_sr_info_server' \
                                                                      --additional-properties='packageVersion=0.1.0' \
                                                                      --additional-properties='sourceFolder=.'
```

2. Installing requirements:
```bash
source venv/bin/active && pip3 install -r src/server/requirements.txt
```
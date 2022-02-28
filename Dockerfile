FROM public.ecr.aws/lambda/python:3.8

RUN pip install "poetry==1.1.12"
COPY pyproject.toml poetry.lock ${LAMBDA_TASK_ROOT}/
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install --force-reinstall -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY . ${LAMBDA_TASK_ROOT}
RUN pip install .

ENTRYPOINT ["python3", "src/webapp/lambda.py"]
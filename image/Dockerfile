FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Required to make SQLlite3 work for Chroma.
RUN pip install pysqlite3-binary

# Install the specified packages
RUN pip install -r requirements.txt --upgrade

# For local testing.
EXPOSE 8000

# Set environment variables
ENV IS_USING_IMAGE_RUNTIME=True
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

# Create directory structure for data
RUN mkdir -p ${LAMBDA_TASK_ROOT}/data/chroma

# Copy application files
COPY src ${LAMBDA_TASK_ROOT}/src

# Set the CMD to your handler
CMD ["src/app_api_handler.lambda_handler"]


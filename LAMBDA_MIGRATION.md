# Migration from EC2 to AWS Lambda

## Overview
This project has been migrated from deploying to EC2 instances to using AWS Lambda with Docker container images.

## Changes Made

### 1. **Dockerfile** (`hello-world/Dockerfile`)
- **Previous**: Used generic `python:3.11-slim` base image designed for standalone applications
- **Now**: Uses AWS Lambda-compatible base image: `public.ecr.aws/lambda/python:3.11`
- **Why**: Lambda requires specific image specifications. The official AWS Lambda base images:
  - Include the Lambda runtime interface emulator
  - Set up the proper working directory (`${LAMBDA_TASK_ROOT}`)
  - Handle the execution model expected by Lambda

### 2. **Application Code** (`hello-world/app.py`)
- **Previous**: Flask web server listening on port 8080
- **Now**: Simple Lambda handler function
- **Why**: Lambda uses an event-driven model, not HTTP port listening. The handler function:
  - Receives `event` (request data) and `context` (execution context)
  - Returns a response dictionary with `statusCode` and `body`
  - No need for Flask or explicit port binding

### 3. **Dependencies** (`hello-world/requirements.txt`)
- **Previous**: `flask`
- **Now**: No external dependencies (basic Lambda handler)
- **Why**: The simple Lambda handler doesn't require Flask

### 4. **GitHub Actions Workflow** (`.github/workflows/aufgabe3.yml`)
- **Previous**: Complex multi-job workflow with EC2 instance provisioning and SSH deployment
- **Now**: Simplified single-job workflow with direct Lambda deployment
- **Key improvements**:
  - Removed EC2 instance creation and security group management
  - Removed SSH key generation and SSH-based deployment
  - Simplified to: Build → Push to ECR → Deploy to Lambda → Test
  - Uses `aws lambda create-function` and `aws lambda update-function-code`

## Setup Requirements

The workflow uses the **LabRole** IAM role that is already configured in your AWS account. No additional secrets need to be configured in your GitHub repository.

The role ARN is automatically determined from your AWS account ID using:
```bash
aws sts get-caller-identity --query Account --output text
```

This resolves to: `arn:aws:iam::ACCOUNT_ID:role/LabRole`

## Testing the Lambda Function

After deployment, the workflow will automatically test the function. You can also manually test it:

```bash
aws lambda invoke \
  --function-name hello-world \
  --payload '{}' \
  --cli-binary-format raw-in-base64-out \
  response.json
cat response.json
```

## Benefits of Lambda Over EC2

1. **Cost**: Pay only for actual execution time
2. **Scalability**: Automatic scaling without managing instances
3. **Maintenance**: No OS patching or instance management
4. **Simplicity**: Faster deployment and less infrastructure code
5. **Cold starts**: For a simple handler like this, cold start times are minimal

## Error Resolution

The previous error:
```
The image manifest, config or layer media type for the source image is not supported.
```

Was caused by using a generic Python base image instead of the AWS Lambda-specific base image. The Lambda runtime expects:
- Proper file structure with handler at `${LAMBDA_TASK_ROOT}`
- Specific metadata and configuration
- Compatible instruction set and runtime environment

The new Dockerfile resolves this by using the official `public.ecr.aws/lambda/python:3.11` base image.

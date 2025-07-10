# Instructions for Creating the ECR Repository

If you encounter the error:

    The repository with name 'hello-world-repo' does not exist in the registry with id '200186773643'

follow these steps to create the repository in AWS ECR:

## Using the AWS Management Console
1. Sign in to the AWS Management Console.
2. Navigate to the ECR (Elastic Container Registry) service.
3. Click on "Create repository."
4. Enter `hello-world-repo` as the repository name.
5. Click "Create repository."

## Using the AWS CLI
Run the following command:

```bash
aws ecr create-repository --repository-name hello-world-repo --region us-east-1
```

After creating the repository, rerun your GitHub Actions workflow. The error should be resolved.

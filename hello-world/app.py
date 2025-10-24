def lambda_handler(event, context):
    """
    Lambda handler function for the hello-world application.
    """
    return {
        'statusCode': 200,
        'body': 'Hello, World!'
    }

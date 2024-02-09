from diagrams import Diagram, Edge, Cluster
from diagrams.aws.compute import EC2Ami, Lambda
from diagrams.aws.network import Endpoint
from diagrams.aws.management import Cloudwatch
from diagrams.aws.storage import S3


with Diagram("EC2-Lambda", show=False, direction="LR"):
    cloudWatch = Cloudwatch("CloudWatch")
    with Cluster("Amazon S3"):
        codeBucket = S3("Code bucket")
        inputBucket = S3("Input bucket")
        outputBucket = S3("Output bucket")
        buckets = [codeBucket, inputBucket, outputBucket]

    

    with Cluster("ec2-lambda-vpc"):
        with Cluster("private-subnet"):
            with Cluster("AWS Lambda"):
                triggerLambda = Lambda("Trigger Function")
                shutdownLambda = Lambda("Cleanup Function")
                lambdas = [triggerLambda, shutdownLambda]
            s3Endpoint = Endpoint("S3 gateway endpoint")
            lambdaEndpoint = Endpoint("Lambda service endpoint")
            ec2Endpoint = Endpoint("EC2 service endpoint")
            cloudwatchEndpoint = Endpoint("Cloudwatch service endpoint")
            ssmEndpoint = Endpoint("System Manager service endpoint")

            ami = EC2Ami("Preloaded AMI")
            
            buckets - s3Endpoint - Edge(label="Refresh code") - ami
            s3Endpoint >> Edge(label="Get and Process files") << ami
            s3Endpoint << Edge(label="Save Output") << ami            
            ami << ec2Endpoint<< triggerLambda
            ami >> lambdaEndpoint >> shutdownLambda
            ami >> ssmEndpoint
            lambdas >> cloudwatchEndpoint >> cloudWatch
            ami >> cloudwatchEndpoint >> cloudWatch

    inputBucket >> Edge(label="Trigger") >> triggerLambda  

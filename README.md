## AWS ParallelCluster serverless API

This repository includes the code to combine AWS ParallelCluster (https://github.com/aws/aws-parallelcluster), AWS API Gateway (https://aws.amazon.com/api-gateway/) and AWS Lambda (https://aws.amazon.com/lambda/) to make a serverless API of the ParallelCluster command line interface.

**AWS ParallelCluster** simplifies the creation and the deployment of HPC clusters. 
**AWS API Gateway** is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. 
**AWS Lambda** automatically runs your code without requiring you to provision or manage servers.

In HPC environments, the role of security is paramount because customers are performing scientific analyses that are central to the businesses in which they work. By using a serverless API, this solution makes it so that customers do not need to run the ParallelCluster CLI in a user’s environment. This offers customers an additional method to keep their environments secure and more easily control the IAM roles and security groups to which individual scientists or researchers need to have access to.

The serverless integration of AWS ParallelCluster can also enable a cleaner and more reproducible infrastructure-as-code paradigm to legacy HPC environments. 

Taking this serverless, infrastructure-as-code approach enables several new interesting pieces of functionality for HPC environments. One such use case would be the ability to build on-demand clusters from an API when on-premises resources are unable to handle the required workload. In this way ParallelCluster can, in serverless and scriptable fashion, extend on-premises resources for running elastic and large-scale HPC on AWS’ virtually unlimited infrastructure. Another possible use case could be the creation of an event-driven workflow in which new clusters are created as soon as new data is uploaded to an S3 bucket. With these kinds of event-driven workflows, you can be creative in finding new ways to build HPC infrastructure easily and in a way that makes the most of the scarcest resource in most HPC departments: researchers’ time.


## License

This library is licensed under the MIT-0 License. See the LICENSE file.


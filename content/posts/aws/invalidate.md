Title: Invalidating CloudFront's Cache
Date: 2021-06-24
Modified: 2021-06-24
Tags: aws, python
Slug: invalidate
Authors: Brian Roepke
Summary: How to invalidate CloudFront's caches and ensure all items are up to date.
Header_Cover: images/sheep.jpg
Og_Image: images/sheep.jpg
Twitter_Image: images/sheep.jpg

## Invalidating with Python and the Boto3 SDK

Cloudfront's default TTL for edge caches is 24 hours.  In most cases this is totally sufficient, however, I've found in some that it's handy when deploying new changes to be able to force the update.  

Utilizing the python boto3 sdk, it's possible to invalidate items.  The below script will invalidate all objects in your cache.  You can modify this to invalidate a single item if you wish.

**Note**: The preferred method is to use the TTL feature or versioned URLs. This will automatically invalidate items and you will not have to wait the approximate 10-15 minutes for an invalidation to finish.

**Note**: There are no charges for the first 1000 [invalidations](https://aws.amazon.com/blogs/aws/new-cloudfront-feature-invalidation/) per month. After that, each one will cost you $0.005 (one half of one cent).

## Checking Status

After you run the srcipt, you can go to your AWS CloudFront console and check the status.

![AWS CloudFront Invalidate Status]({static}../../images/invalidate.png)

## Python Boto3 Script

```python
import boto3
import time
 
# Create CloudFront client
cf = boto3.client('cloudfront')
 
# Enter Original name
 
# A string of characters that can be found in your CF console
DISTRIBUTION_ID = "<distribution id>" 
 
# Create CloudFront invalidation
def create_invalidation():
    res = cf.create_invalidation(
        DistributionId=DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [
                    '/*'
                ]
            },
            'CallerReference': str(time.time()).replace(".", "")
        }
    )
    invalidation_id = res['Invalidation']['Id']
    return invalidation_id
 
# Create CloudFront Invalidation
id = create_invalidation()
print("Invalidation created successfully with Id: " + id)
```

## References**:

[^INV]: [Python Script to Create CloudFront Invalidations
](https://tecadmin.net/python-script-create-cloudfront-invalidations/)
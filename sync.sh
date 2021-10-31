# run the HTML command from the Makefile to publish any pages
make html

# Sync to S3 - Delete any files that are no longer present
aws s3 sync ./output s3://roepkeb.com --delete --exclude "*.DS_Store"

# Run this python script to invalidate CloudFront and ensure changes are visible
python3 invalidate_cf.py
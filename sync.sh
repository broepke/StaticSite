make html

aws s3 sync ./output s3://roepkeb.com --delete --exclude "*.DS_Store"

python3 invalidate_cf.py
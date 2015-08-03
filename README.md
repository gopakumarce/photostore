PhotoStore's database and backend services, first version. Just a simple
program to learn how to use AWS dynamodb/s3 and nginx/flask, it uploads
a bunch of photos to AWS S3 and gives them "tags". And then uploads the
tag information to dynamodb and gives the user a search option to search
on the tag. The search will lookup dynamodb for a match, and if there is
a match then dynamodb will give the S3 link to the actual photo which we
will then display (the UI js code is not present here). 

There is also a script in misc/ directory which basically downloads a ton
of high quality pictures from internet and gives them some random tags
and uploads them to S3 as a seed database to start with and then also
fills up dynamodb etc..

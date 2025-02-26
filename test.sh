psql -h inaturalist-dev.cu9mqs2m0f9r.us-east-1.rds.amazonaws.com -U postgres -d postgres -c "\copy raw_stg.food_access FROM 'food_access.csv' WITH CSV HEADER;"

psql -h inaturalist-dev.cu9mqs2m0f9r.us-east-1.rds.amazonaws.com -U postgres -d postgres -c "\copy raw_stg.food_access FROM '/home/ubuntu/iNaturalist-edibl e-plants/temp/food-access-research.csv' WITH CSV HEADER;"


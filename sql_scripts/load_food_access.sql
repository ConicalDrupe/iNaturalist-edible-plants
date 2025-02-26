SELECT aws_commons.create_s3_uri(
   'inat-hackathon25-bucket',
   'Food Access Research Atlas.csv',
   'us-east-1'
) AS s3_uri \gset


SELECT aws_s3.table_import_from_s3(
   'raw_stg.food_access',
   'CensusTract,State,County,POP2010,OHU2010,PovertyRate,MedianFamilyIncome,LA1and10,LATracts10,lapophalf,lalowihalf,lahunvhalf,lasnaphalf,lahunv1,lasnap1,lasnap10,TractLOWI,TractSNAP',
   '(format csv)',
   :'s3_uri'
);

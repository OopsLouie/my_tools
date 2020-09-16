import os
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
import pandas as pd

conf = SparkConf().setAppName('test_parquet')
sc = SparkContext('local', 'test', conf=conf)
spark = SparkSession(sc)

parquetRoot = r"C:\\Users\\luyi\\Desktop\\test_data\\test_data"
csv_fileRoot = r"C:\\Users\\luyi\\Desktop\\test_data"
csv_filename = "total_count.csv"

file_list = os.listdir(parquetRoot)
csv_data_list = []


for filename in file_list:
    print("processing file %s" % filename)
    df = spark.read.parquet(parquetRoot+'/'+filename)
    df_1 = df.select("Filename","ST_AMB_ITLI_ST_MNU_AMB_PR_ITLI","ST_AMB_ITLI_ST_MOD_AMB_PR_ITLI")

    df_2 = df_1.dropDuplicates(subset=["ST_AMB_ITLI_ST_MNU_AMB_PR_ITLI","ST_AMB_ITLI_ST_MOD_AMB_PR_ITLI"])
    df_2.show()

    rows = df_2.take(df_2.count())
    for row in rows:
        csv_data_list.append([row.Filename,row.ST_AMB_ITLI_ST_MNU_AMB_PR_ITLI,row.ST_AMB_ITLI_ST_MOD_AMB_PR_ITLI,df_1.where(df.ST_AMB_ITLI_ST_MNU_AMB_PR_ITLI == row.ST_AMB_ITLI_ST_MNU_AMB_PR_ITLI).where(df.ST_AMB_ITLI_ST_MOD_AMB_PR_ITLI == row.ST_AMB_ITLI_ST_MOD_AMB_PR_ITLI).count()])

name = ["Filename","ST_AMB_ITLI_ST_MNU_AMB_PR_ITLI","ST_AMB_ITLI_ST_MOD_AMB_PR_ITLI","counts"]
final_df = pd.DataFrame(columns=name, data = csv_data_list)
final_df.to_csv(csv_fileRoot + '\\' + csv_filename,index=False)


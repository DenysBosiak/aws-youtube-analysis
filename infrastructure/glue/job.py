import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node S3 raw bucket
S3rawbucket_node1780062729650 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://aws-developing-youtube-analysis/raw/"], "recurse": True}, transformation_ctx="S3rawbucket_node1780062729650")

# Script generated for node Change Schema
ChangeSchema_node1780063307444 = ApplyMapping.apply(frame=S3rawbucket_node1780062729650, mappings=[("video_id", "string", "video_id", "string"), ("trending_date", "string", "trending_date", "string"), ("title", "string", "title", "string"), ("channel_title", "string", "channel_title", "string"), ("category_id", "string", "category_id", "int"), ("publish_time", "string", "publish_time", "timestamp"), ("tags", "string", "tags", "string"), ("views", "string", "views", "int"), ("likes", "string", "likes", "int"), ("dislikes", "string", "dislikes", "int"), ("comment_count", "string", "comment_count", "int"), ("thumbnail_link", "string", "thumbnail_link", "string"), ("comments_disabled", "string", "comments_disabled", "string"), ("ratings_disabled", "string", "ratings_disabled", "string"), ("video_error_or_removed", "string", "video_error_or_removed", "string"), ("description", "string", "description", "string")], transformation_ctx="ChangeSchema_node1780063307444")

# Script generated for node S3 bronze bucket
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1780063307444, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1780063059297", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
if (ChangeSchema_node1780063307444.count() >= 1):
   ChangeSchema_node1780063307444 = ChangeSchema_node1780063307444.coalesce(1)
S3bronzebucket_node1780063663313 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchema_node1780063307444, connection_type="s3", format="glueparquet", connection_options={"path": "s3://aws-developing-youtube-analysis/bronze/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="S3bronzebucket_node1780063663313")

job.commit()
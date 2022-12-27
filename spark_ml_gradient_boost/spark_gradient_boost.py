from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import IndexToString, StringIndexer, VectorAssembler, VectorIndexer
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, year, col


def train_and_predict():
    spark = SparkSession.builder.master("local[*]").appName("MOT Test result prediction").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    source_files_path = "/home/user/download/dft_test_result_2020"
    mot_data = spark.read.option("header", "true").csv(source_files_path)
    (mot_data
     .withColumn("year", year(col("first_use_date")))
     .repartition(col("year"), col("make"), col("model"))
     .write
     .format("parquet")
     .saveAsTable("/home/user/motdata"))

    df = (spark.read
          .parquet("/home/user/motdata")
          .filter("""test_type = 'NT'
                       and test_result in ('F', 'P') """))

    df = (df
          .drop("colour", "vehicle_id", "test_id", "test_date", "test_class_id", "test_type", "postcode_area",
                "first_use_date")
          .withColumn("indexed_test_mileage", expr("int(test_mileage)"))
          .withColumn("indexed_year", expr("int(year)"))
          .withColumn("indexed_cylinder_capacity", expr("int(cylinder_capacity)"))
          .filter("make = 'FORD'")
          .filter("model = 'FIESTA'"))

    string_cols = ["make", "model", "fuel_type"]
    feature_cols = ["test_mileage", "fuel_type", "year", "cylinder_capacity"]

    def get_string_indexer(c) -> StringIndexer:
        return (StringIndexer()
                .setInputCol(c)
                .setOutputCol(f"indexed_{c}"))

    for _col in feature_cols:
        df = df.filter(f"{_col} is not null")

    df = df.localCheckpoint(True)

    for _col in string_cols:
        indexer = get_string_indexer(_col)
        df = indexer.fit(df).transform(df)

    idx_feature_cols = [f"indexed_{c}" for c in feature_cols]
    features_assembler = (VectorAssembler()
                          .setInputCols(idx_feature_cols)
                          .setOutputCol("features"))

    with_features_vector_df = (features_assembler
                               .transform(df)
                               .drop(*idx_feature_cols)
                               .localCheckpoint(True))

    # Automatically identify categorical features, and index them.
    # Set maxCategories so features with > 4 distinct values are treated as continuous.
    feature_indexer = (VectorIndexer()
                       .setInputCol("features")
                       .setOutputCol("indexedFeatures")
                       .setMaxCategories(4)
                       .fit(with_features_vector_df))

    # Split the data into training and test sets (30% held out for testing).
    (training_data, test_data) = with_features_vector_df.randomSplit([0.7, 0.3])

    # Train a Gradient boost model.
    gb = (GBTClassifier()
          .setLabelCol("indexedTestResult")
          .setFeaturesCol("indexedFeatures")
          .setMaxIter(10)
          .setFeatureSubsetStrategy("auto"))

    label_indexer = (StringIndexer()
                     .setInputCol("test_result")
                     .setOutputCol("indexedTestResult")
                     .fit(df))

    # Convert indexed labels back to original labels.
    label_converter = (IndexToString()
                       .setInputCol("prediction")
                       .setOutputCol("predictedTestResult")
                       .setLabels(list(label_indexer.labelsArray[0])))

    # Chain indexers and forest in a Pipeline.
    pipeline = Pipeline().setStages([label_indexer, feature_indexer, gb, label_converter])

    use_saved_model = False
    path = "/home/user/models/spark-rf/model"
    # Train model. This also runs the indexers.
    model: PipelineModel
    if use_saved_model:
        model = PipelineModel.load(path)
    else:
        model = pipeline.fit(training_data)
        model.write().overwrite().save(path)

    # Make predictions.
    predictions = model.transform(test_data)

    # Select example rows to display.
    cols = [*["predictedTestResult", "test_result"], *feature_cols]
    # predictions.selectExpr(cols: _*).show(1500)
    (predictions
     .repartition(1)
     .selectExpr(*cols)
     .write
     .mode("overwrite")
     .csv("/tmp/output.csv"))

    # Select (prediction, true label) and compute test error.
    evaluator = (MulticlassClassificationEvaluator()
                 .setLabelCol("indexedTestResult")
                 .setPredictionCol("prediction")
                 .setMetricName("accuracy"))
    accuracy = evaluator.evaluate(predictions)
    print(f"Test Accuracy = {accuracy}")
    print(f"Test Error = {(1.0 - accuracy)}")


if __name__ == "__main__":
    train_and_predict()

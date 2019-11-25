import org.apache.spark.sql.types.{StructField, StructType, DoubleType}
import org.apache.spark.ml.param.{ParamMap, Param, Params}

trait MyParams extends Params {
    final val inputCol1 = new Param[String](this, "inputCol1", "The first input column")
    final val inputCol2 = new Param[String](this, "inputCol2", "The second input column")
    final val outputCol = new Param[String](this, "outputCol", "The output column")
    
  protected def validateAndTransformSchema(schema: StructType): StructType = {
    val idx1 = schema.fieldIndex($(inputCol1))
    val field1 = schema.fields(idx1)
    if (field1.dataType != DoubleType) {
      throw new Exception(s"Input type ${field1.dataType} did not match input type DoubleType")
    }  
    val idx2 = schema.fieldIndex($(inputCol2))
    val field2 = schema.fields(idx2)
    if (field2.dataType != DoubleType) {
      throw new Exception(s"Input type ${field2.dataType} did not match input type DoubleType")
    }
    schema.add(StructField($(outputCol), DoubleType, false))

  }
}


import org.apache.spark.ml.util.Identifiable
import org.apache.spark.ml.Transformer
import org.apache.spark.ml.param.{ParamMap, Param, Params}
import org.apache.spark.sql.{DataFrame, Dataset}
import org.apache.spark.sql.types.{StructField, StructType, DoubleType, StringType, IntegerType}
import org.apache.spark.sql.functions.{col, udf}


class MyTransformer(override val uid: String) extends Transformer with MyParams {
    def this() = this(Identifiable.randomUID("configurablewordcount"))
    
    def setInputCol1(value: String): this.type = set(inputCol1, value)
    
    def setInputCol2(value: String): this.type = set(inputCol2, value)
    
    def setOutputCol(value: String): this.type = set(outputCol, value)
    
    override def copy(extra: ParamMap): MyTransformer = {
    defaultCopy(extra)
    }

    override def transformSchema(schema: StructType) = {
    val idx1 = schema.fieldIndex($(inputCol1))
    val field1 = schema.fields(idx1)
    if (field1.dataType != DoubleType) {
      throw new Exception(s"Input type ${field1.dataType} did not match input type DoubleType")
    }  
    val idx2 = schema.fieldIndex($(inputCol2))
    val field2 = schema.fields(idx2)
    if (field2.dataType != DoubleType) {
      throw new Exception(s"Input type ${field2.dataType} did not match input type DoubleType")
    }
    schema.add(StructField($(outputCol), DoubleType, false))

    }
    
    override def transform(dataset: Dataset[_]): DataFrame = {
        housing.withColumn($(outputCol), housing.col($(inputCol1)) / housing.col($(inputCol2)))    
    }
}



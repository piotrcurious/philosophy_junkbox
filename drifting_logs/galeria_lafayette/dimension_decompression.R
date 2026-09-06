# dimension_decompression.R - Multidimensional Decompression & Formal Proof Integration
library(jsonlite)

cat("Reading high_dim_trajectories.csv and ontology_output.json...\n")
df <- read.csv("high_dim_trajectories.csv", stringsAsFactors = FALSE)
prolog_data <- fromJSON("ontology_output.json")

# Extract 10D numerical matrix for dimensionality reduction
dim_cols <- c("posX", "posY", "posZ", "temperature", "humidity",
              "commercialVal", "accessibility", "symbolicVal",
              "thermalStress", "flowDensity")
dim_matrix <- as.matrix(df[, dim_cols])

# Scale matrix to zero mean, unit variance
scaled_matrix <- scale(dim_matrix)

# 1. Classical Multidimensional Scaling (MDS) to 3D
dist_matrix <- dist(scaled_matrix)
mds_fit <- cmdscale(dist_matrix, k = 3)

# 2. Principal Component Analysis (PCA) to 3D
pca_fit <- prcomp(scaled_matrix, center = TRUE, scale. = TRUE)
pca_3d <- pca_fit$x[, 1:3]

# Construct JSON payload structure
data_list <- list()

for (i in 1:nrow(df)) {
  data_list[[i]] <- list(
    archetype      = df$archetype[i],
    id             = df$id[i],
    name           = df$name[i],
    spatial_3d     = list(x = df$posX[i], y = df$posY[i], z = df$posZ[i]),
    mds_3d         = list(x = mds_fit[i, 1] * 10, y = mds_fit[i, 2] * 10, z = mds_fit[i, 3] * 10),
    pca_3d         = list(x = pca_3d[i, 1] * 10, y = pca_3d[i, 2] * 10, z = pca_3d[i, 3] * 10),
    raw_10d        = list(
      posX          = df$posX[i],
      posY          = df$posY[i],
      posZ          = df$posZ[i],
      temperature   = df$temperature[i],
      humidity      = df$humidity[i],
      commercialVal = df$commercialVal[i],
      accessibility = df$accessibility[i],
      symbolicVal   = df$symbolicVal[i],
      thermalStress = df$thermalStress[i],
      flowDensity   = df$flowDensity[i]
    )
  )
}

final_output <- list(
  trajectories = data_list,
  prolog_verification = prolog_data$verification,
  prolog_axioms = prolog_data$axioms,
  prolog_formal_trajectories = prolog_data$formal_trajectories
)

json_output <- toJSON(final_output, auto_unbox = TRUE, pretty = TRUE)
write(json_output, "decompressed_data.json")
cat("Successfully generated decompressed_data.json with 10D vectors and Prolog proof results.\n")

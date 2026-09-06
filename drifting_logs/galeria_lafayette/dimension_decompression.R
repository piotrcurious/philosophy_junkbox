# dimension_decompression.R - Multidimensional Decompression & Formal Proof Integration
library(jsonlite)

cat("Reading high_dim_trajectories.csv and ontology_output.json...\n")
df <- read.csv("high_dim_trajectories.csv", stringsAsFactors = FALSE)

prolog_data <- list()
if (file.exists("ontology_output.json")) {
  prolog_data <- fromJSON("ontology_output.json")
}

# Identify numeric columns excluding metadata
meta_cols <- c("archetype", "id", "name")
dim_cols <- setdiff(colnames(df), meta_cols)

cat("Dynamic dimensions detected:", paste(dim_cols, collapse = ", "), "\n")

dim_matrix <- as.matrix(df[, dim_cols])

# Scale matrix (handling zero variance columns)
scaled_matrix <- scale(dim_matrix)
scaled_matrix[is.na(scaled_matrix)] <- 0

# 1. Classical Multidimensional Scaling (MDS) to 3D
dist_matrix <- dist(scaled_matrix)
k_dims <- min(3, nrow(df) - 1)
mds_fit <- matrix(0, nrow = nrow(df), ncol = 3)
if (k_dims > 0) {
  res_mds <- cmdscale(dist_matrix, k = k_dims)
  mds_fit[, 1:ncol(res_mds)] <- res_mds
}

# 2. Principal Component Analysis (PCA) to 3D
pca_fit <- prcomp(scaled_matrix, center = TRUE, scale. = FALSE)
pca_3d <- matrix(0, nrow = nrow(df), ncol = 3)
num_pcs <- min(3, ncol(pca_fit$x))
if (num_pcs > 0) {
  pca_3d[, 1:num_pcs] <- pca_fit$x[, 1:num_pcs]
}

# Construct JSON payload structure
data_list <- list()

for (i in 1:nrow(df)) {
  raw_vector <- as.list(df[i, dim_cols])

  posX_val <- ifelse("posX" %in% names(raw_vector), raw_vector$posX, 0)
  posY_val <- ifelse("posY" %in% names(raw_vector), raw_vector$posY, 0)
  posZ_val <- ifelse("posZ" %in% names(raw_vector), raw_vector$posZ, 0)

  data_list[[i]] <- list(
    archetype      = df$archetype[i],
    id             = df$id[i],
    name           = df$name[i],
    spatial_3d     = list(x = posX_val, y = posY_val, z = posZ_val),
    mds_3d         = list(x = mds_fit[i, 1] * 10, y = mds_fit[i, 2] * 10, z = mds_fit[i, 3] * 10),
    pca_3d         = list(x = pca_3d[i, 1] * 10, y = pca_3d[i, 2] * 10, z = pca_3d[i, 3] * 10),
    raw_10d        = raw_vector
  )
}

final_output <- list(
  trajectories = data_list,
  prolog_dimensions = prolog_data$dimensions,
  prolog_verification = prolog_data$verification,
  prolog_axioms = prolog_data$axioms,
  prolog_formal_trajectories = prolog_data$formal_trajectories
)

json_output <- toJSON(final_output, auto_unbox = TRUE, pretty = TRUE)
write(json_output, "decompressed_data.json")
cat("Successfully generated decompressed_data.json with dynamic multi-dimensional vectors and Prolog proof results.\n")

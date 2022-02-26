devtools::install_github("robjhyndman/anomalous-acm")
library(anomalousACM)

data_root <- "/home/fanqiliang/data/yidong"
kpi_root <- file.path(data_root, "YiDong_train_detect_txtData")

for ( f in list.files(kpi_root)) {
    kpi_file <- file.path(kpi_root, f)
    print(kpi_file)
    kpi_value <- as.matrix(read.csv(kpi_file), byrow = TRUE)
    print(paste(nrow(kpi_value), ncol(kpi_value), sep = " "))
    kpi_seq <- ts(kpi_value, start=c(2020, 1), frequency = 24 * 60 / 15)  # 15min的时间间隔
    kpi_feature <- tsmeasures(kpi_seq)
    # biplot.features(y)
    res <- anomaly(kpi_feature)
    write.csv(res[2], file.path("output", f), row.names = FALSE)
}


# z <- ts(matrix(rnorm(3000),ncol=100),freq=4)
# y <- tsmeasures(z)
# biplot.features(y)
# anomaly(y)
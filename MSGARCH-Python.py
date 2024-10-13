import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
pandas2ri.activate()

# Carrega pacotes do R
tidyquant = importr('tidyquant')
quantmod = importr('quantmod')
msgarch = importr('MSGARCH')
dplyr = importr('dplyr')

# Código R para carregar tickers e ajustar o modelo MSGARCH
r_code = """
tickers <- readLines("C:/Users/loren/Downloads/tickers.txt")
start_date <- as.Date("2019-01-02")
end_date <- as.Date("2023-12-30")

get_stock_data <- function(ticker) {
  tryCatch({
    stock_data <- getSymbols(ticker, src = 'yahoo', from = start_date, to = end_date, auto.assign = FALSE)
    adjusted_prices <- Cl(stock_data)
    return(data.frame(Date = index(adjusted_prices), Price = as.numeric(adjusted_prices), Ticker = ticker))
  }, error = function(e) {
    message(paste("Erro ao baixar dados para:", ticker))
    return(NULL)
  })
}

all_stock_data <- do.call(rbind, lapply(tickers, get_stock_data))

all_stock_data <- all_stock_data %>%
  group_by(Ticker) %>%
  mutate(Return = log(Price / lag(Price))) %>%
  na.omit()

fit_msgarch <- function(returns) {
  spec <- CreateSpec()  
  fit <- FitML(spec = spec, data = returns)
  return(fit)
}

results <- all_stock_data %>%
  group_by(Ticker) %>%
  summarise(Model = list(fit_msgarch(Return)))

filtered_results <- results %>%
  mutate(MeanVolatility = sapply(Model, function(m) {
    pred <- Volatility(object = m)
    return(mean(pred))
  })) %>%
  arrange(MeanVolatility) %>%
  slice(1:50)

formatted_results <- filtered_results %>%
  transmute(Result = paste(Ticker, MeanVolatility, sep = ", "))

formatted_results$Result
"""

# Executa o código R em Python
ro.r(r_code)

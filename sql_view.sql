CREATE VIEW vStock AS
SELECT
    stockId,
    o,
    h,
    l,
    c,
    dt,
    ROUND(AVG(o) OVER (PARTITION BY stockId ORDER BY dt ROWS BETWEEN 13 PRECEDING AND CURRENT ROW),2) AS ma13,
    ROUND(AVG(o) OVER (PARTITION BY stockId ORDER BY dt ROWS BETWEEN 34 PRECEDING AND CURRENT ROW),2) AS ma34,
    ROUND(AVG(o) OVER (PARTITION BY stockId ORDER BY dt ROWS BETWEEN 89 PRECEDING AND CURRENT ROW),2) AS ma89,
    ROUND(AVG(o) OVER (PARTITION BY stockId ORDER BY dt ROWS BETWEEN 144 PRECEDING AND CURRENT ROW),2) AS ma144
FROM
    stockdata;
    

CREATE VIEW vStockCrossed AS
SELECT
    stockId,
    case when c >= ma13 and ma13 >=o then 1 else 0 end as isMa13,
    case when c >= ma34 and ma34 >=o then 1 else 0 end as isMa34,
    case when c >= ma89 and ma89 >=o then 1 else 0 end as isMa89,
    case when c >= ma144 and ma144 >=o then 1 else 0 end as isMa144
FROM
    vStock;

select count(*) from stockdata; --129904


select * from StockData;
select * from StockData where stockId='1514' order by dt desc;
select * from vStockCrossed;
select max(dt) from vStockCrossed;

    
select * from vStockCrossed where stockId='1514';

select stockId from vStockCrossed where isMa13+isMa34+isMa89+isMa144 =4 group by stockId;
select * from vStockCrossed2 where isMa13+isMa34+isMa89+isMa144 =3
            and o>20 and o<300
            group by stockId;
            
select * from vStock where stockId='3665' order by dt desc;

Delete from stockData where dt>='20240116 14:30';
SELECT
    a.stockId,
    a.o as o,
    b.o as om,
    case when a.o >= a.ma13 and a.ma13 >=b.o then 1 else 0 end as isMa13,
    case when a.o >= a.ma34 and a.ma34 >=b.o then 1 else 0 end as isMa34,
    case when a.o >= a.ma89 and a.ma89 >=b.o then 1 else 0 end as isMa89,
    case when a.o >= a.ma144 and a.ma144 >=b.o then 1 else 0 end as isMa144
FROM
    vStock as a 
    inner join (select stockId,o from StockData where dt='20240116 10:40') as b on b.stockId=a.stockId
where a.dt = (select max(dt) from stockdata)
    and a.ma34 >= a.ma13
    and a.ma89 >= a.ma34
    and a.ma144 >= a.ma89
    
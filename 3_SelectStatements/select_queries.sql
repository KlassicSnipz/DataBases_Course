-- Assignment 1 
with customer_total_sales as (
	select cd.customer_name,coalesce(sum(stf.total_amount),0) as total_sales from target.customer_dim cd 
	left join target.sales_transactions_fact stf
	on stf.customer_key = cd.customer_key
	group by cd.customer_name
)
select customer_name , total_sales  from customer_total_sales
where total_sales > (select avg(total_sales) from customer_total_sales) 

-- Assignment 2
select pd.product_name, coalesce(sum(stf.total_amount),0) as total_sales from target.product_dim pd 
left join target.sales_transactions_fact stf on stf.product_key = pd.product_key
group by pd.product_name
order by total_sales desc
limit 1

-- Assignment 3
with country_sales as (
    select cd.country_name, coalesce(sum(stf.total_amount),0) as total_sales
    from target.country_dim cd
    left join target.sales_transactions_fact stf on cd.country_key = stf.country_key
    group by cd.country_name
)
select country_name, total_sales
from country_sales
order by total_sales desc

-- Assignment 4
select cd.customer_name, count(stf.sales_trans_key) as number_of_purchases from target.customer_dim cd
left join target.sales_transactions_fact stf on cd.customer_key = stf.customer_key
group by cd.customer_name
having count(stf.sales_trans_key) > 5
order by number_of_purchases desc

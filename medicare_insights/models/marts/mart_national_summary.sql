with base as (
    select * from {{ ref('stg_inpatient') }}
)

select
    provider_state,
    count(*)                                           as total_records,
    sum(total_discharges)                              as total_discharges,
    round(avg(average_total_payments), 2)              as avg_total_payments,
    round(avg(average_medicare_payments), 2)           as avg_medicare_payments,
    round(avg(out_of_pocket), 2)                       as avg_out_of_pocket,
    round(avg(average_medicare_payments)
          / avg(average_total_payments) * 100, 1)      as medicare_pct,
    round(avg(out_of_pocket)
          / avg(average_total_payments) * 100, 1)      as oop_pct
from base
group by provider_state
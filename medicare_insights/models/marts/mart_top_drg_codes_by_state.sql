with base as (
    select * from {{ ref('stg_inpatient') }}
)

select
    provider_state,
    drg_definition,
    sum(total_discharges)                          as total_discharges,
    round(avg(average_covered_charges), 2)         as avg_covered_charges,
    round(avg(average_total_payments), 2)          as avg_total_payments,
    round(avg(average_medicare_payments), 2)       as avg_medicare_payments,
    round(avg(out_of_pocket), 2)                   as avg_out_of_pocket
from base
group by provider_state, drg_definition
order by total_discharges desc
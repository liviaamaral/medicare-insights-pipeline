with base as (
    select * from {{ ref('stg_inpatient') }}
),

national_avg as (
    select
        round(avg(average_total_payments), 2)   as national_avg_payment,
        round(avg(average_medicare_payments), 2) as national_avg_medicare,
        round(avg(out_of_pocket), 2)             as national_avg_out_of_pocket
    from base
),

state_avg as (
    select
        provider_state,
        round(avg(average_total_payments), 2)    as state_avg_payment,
        round(avg(average_medicare_payments), 2) as state_avg_medicare,
        round(avg(out_of_pocket), 2)             as state_avg_out_of_pocket,
        sum(total_discharges)                    as total_discharges,
        count(distinct provider_id)              as total_providers
    from base
    group by provider_state
)

select
    s.provider_state,
    s.state_avg_payment,
    s.state_avg_medicare,
    s.state_avg_out_of_pocket,
    s.total_discharges,
    s.total_providers,
    n.national_avg_payment,
    n.national_avg_medicare,
    n.national_avg_out_of_pocket,
    round(n.national_avg_medicare / n.national_avg_payment * 100, 1)         as national_medicare_pct,
    round(n.national_avg_out_of_pocket / n.national_avg_payment * 100, 1)    as national_oop_pct,
    round(s.state_avg_payment - n.national_avg_payment, 2)         as variance_from_national,
    round((s.state_avg_payment - n.national_avg_payment)
          / n.national_avg_payment * 100, 2)                       as pct_variance,
    round(s.state_avg_out_of_pocket - n.national_avg_out_of_pocket, 2)          as oop_variance,
    round((s.state_avg_out_of_pocket - n.national_avg_out_of_pocket) 
      / n.national_avg_out_of_pocket * 100, 2)                               as oop_pct_variance
from state_avg s
cross join national_avg n
order by pct_variance desc
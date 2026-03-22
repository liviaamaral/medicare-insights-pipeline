with source as (
    select * from {{ source('medicare_insights', 'inpatient_2015') }}
),

renamed as (
    select
        drg_definition,
        provider_id,
        provider_name,
        provider_city,
        provider_state,
        total_discharges,
        average_covered_charges,
        average_total_payments,
        average_medicare_payments,
        out_of_pocket
    from source
)

select * from renamed
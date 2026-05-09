select *
from {{ ref('stg_inpatient') }}
where average_total_payments < 0
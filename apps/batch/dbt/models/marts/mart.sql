select
    id,
    upper(name) as name_upper
from {{ ref('staging') }}

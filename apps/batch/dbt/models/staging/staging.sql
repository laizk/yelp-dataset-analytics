select
    id,
    name,
    created_at
from {{ ref('seed') }}

# CarRent

## Find matching cars

Use `GET /api/matching/cars/` to list available cars. Filters can be combined:

| Query parameter | Behavior |
| --- | --- |
| `model` | Case-insensitive partial model match |
| `year` | Exact model year |
| `min_price` | Minimum daily price, inclusive |
| `max_price` | Maximum daily price, inclusive |
| `is_available` | Filter by availability (`true` or `false`); defaults to available cars |

For example, `/api/matching/cars/?model=civic&year=2022&max_price=50.00` returns available 2022 Civic models priced at no more than 50 per day. Invalid filters, including a minimum price above the maximum, return `400 Bad Request`.
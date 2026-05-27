# Medication Scheduler

Schedules a user's daily medication intake across 6 time brackets (morning, etc.) based on their medication list, dosages, drug interactions, and lag times optimizing for waking hours where possible.

Built using OR-Tools to handle constraint satisfaction, ensuring medications with interactions are spaced appropriately. If interactions are too complex to resolve automatically, the schedule is flagged for doctor review.

Triggered manually via an optimize button, with the resulting schedule written directly to the database.

---

## Stack

| Layer | Technology |
|-------|------------|
| Language | Python |
| Backend | FastAPI |
| Database | Supabase (PostgreSQL) |
| Optimization | Google OR-Tools |

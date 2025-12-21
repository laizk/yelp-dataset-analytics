-- Minimal analytics seed data for local dev
CREATE TABLE IF NOT EXISTS analytics_seed (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  created_at DATE NOT NULL
);

INSERT INTO analytics_seed (id, name, created_at) VALUES
  (1, 'Alice', '2024-01-01'),
  (2, 'Bob', '2024-01-02'),
  (3, 'Charlie', '2024-01-03')
ON CONFLICT (id) DO NOTHING;

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    role TEXT,
    conversation_id TEXT NOT NULL,
    content TEXT,
    model TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
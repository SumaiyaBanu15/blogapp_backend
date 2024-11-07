-- Drop the existing posts table if it exists
DROP TABLE IF EXISTS posts;

-- Create the new posts table with the additional image field
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image TEXT,  -- New field for storing the image URL
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

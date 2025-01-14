CREATE TABLE shifts (
    shift_id VARCHAR(50) PRIMARY KEY,       -- Unique ID for the shift (from "id")
    employee_id BIGINT REFERENCES employees(employee_id),            -- Employee ID (from "user.id")
    start_time TIMESTAMP NOT NULL,          -- Scheduled shift start time (from "dtstart")
    end_time TIMESTAMP NOT NULL,            -- Scheduled shift end time (from "dtend")
    clock_in_time TIMESTAMP,                -- Actual clock-in time (from "clockIn")
    clock_out_time TIMESTAMP,               -- Actual clock-out time (from "clockOut")
    break_minutes INT DEFAULT 0,            -- Break minutes (from "breakMinutes")
    status VARCHAR(50),                     -- Shift status (e.g., "published", "pending")
    location_id BIGINT,                     -- Location ID (from "location.id")
    position_id BIGINT,                     -- Position ID (from "position.id")
    date DATE,     -- Record creation timestamp
);

CREATE TABLE employees (
    employee_id BIGINT PRIMARY KEY,      -- Matches the "id" from the API
    legal_name VARCHAR(255),            -- "legalName"
    lastname VARCHAR(255),              -- "lastname"
    email VARCHAR(255),                 -- "email"
    active BOOLEAN,                     -- "active" (true if the employee is active)
    created_at TIMESTAMP DEFAULT NOW() -- Timestamp for when the employee was added
);

CREATE TABLE payroll (
    payroll_id SERIAL PRIMARY KEY,         -- Unique ID for payroll entry
    employee_id BIGINT REFERENCES employees(employee_id), -- Foreign Key to employees
    month_year DATE,                       -- Month and year of the payroll (e.g., "2025-01-01")
    total_hours DECIMAL(5, 2),             -- Total hours worked in the month
    dagvinna DECIMAL(5,2),
    eftirvinna DECIMAL(5,2),
    næturvinna DECIMAL(5,2),
    yfirvinna DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW(),    -- Timestamp for when the payroll was generated
    updated_at TIMESTAMP DEFAULT NOW()     -- Timestamp for last update
);

CREATE TABLE locations (
    location_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    external_id INT,
    phone BIGINT
);
-- Insert default fields for 'personal_info' document type
INSERT INTO DefaultField (document_type, field_name, field_type, required, "order")
VALUES
('personal_info', 'first_name', 'string', TRUE, 1),
('personal_info', 'last_name', 'string', TRUE, 2),
('personal_info', 'date_of_birth', 'date', TRUE, 3),
('personal_info', 'gender', 'string', TRUE, 4),
('personal_info', 'address', 'string', TRUE, 5),
('personal_info', 'phone_number', 'string', TRUE, 6),
('personal_info', 'email', 'string', TRUE, 7),
('personal_info', 'emergency_contact_name', 'string', TRUE, 8),
('personal_info', 'emergency_contact_phone', 'string', TRUE, 9),
('personal_info', 'insurance_provider', 'string', FALSE, 10),
('personal_info', 'insurance_policy_number', 'string', FALSE, 11);

-- Insert default fields for 'medical_info' document type
INSERT INTO DefaultField (document_type, field_name, field_type, required, "order")
VALUES
('medical_info', 'allergies', 'string', FALSE, 1),
('medical_info', 'current_medications', 'string', FALSE, 2),
('medical_info', 'past_surgeries', 'string', FALSE, 3),
('medical_info', 'chronic_conditions', 'string', FALSE, 4),
('medical_info', 'family_medical_history', 'string', FALSE, 5),
('medical_info', 'immunizations', 'string', FALSE, 6),
('medical_info', 'smoking_status', 'string', FALSE, 7),
('medical_info', 'alcohol_use', 'string', FALSE, 8),
('medical_info', 'exercise_frequency', 'string', FALSE, 9),
('medical_info', 'height_cm', 'float', FALSE, 10),
('medical_info', 'weight_kg', 'float', FALSE, 11),
('medical_info', 'blood_type', 'string', FALSE, 12);

-- Insert default fields for 'dental' document type
INSERT INTO DefaultField (document_type, field_name, field_type, required, "order")
VALUES
('dental', 'last_dental_visit', 'date', FALSE, 1),
('dental', 'reason_for_last_visit', 'string', FALSE, 2),
('dental', 'brushing_frequency', 'string', FALSE, 3),
('dental', 'flossing_frequency', 'string', FALSE, 4),
('dental', 'any_dental_pain', 'boolean', FALSE, 5),
('dental', 'sensitivity_to_hot_or_cold', 'boolean', FALSE, 6),
('dental', 'previous_dental_procedures', 'string', FALSE, 7),
('dental', 'bleeding_gums', 'boolean', FALSE, 8),
('dental', 'teeth_grinding', 'boolean', FALSE, 9),
('dental', 'jaw_pain', 'boolean', FALSE, 10);

-- Insert default fields for 'psychological_info' document type
INSERT INTO DefaultField (document_type, field_name, field_type, required, "order")
VALUES
('psychological_info', 'current_mood', 'string', FALSE, 1),
('psychological_info', 'stress_level', 'integer', FALSE, 2),
('psychological_info', 'sleep_quality', 'integer', FALSE, 3),
('psychological_info', 'past_mental_health_issues', 'string', FALSE, 4),
('psychological_info', 'current_therapy', 'boolean', FALSE, 5),
('psychological_info', 'medications', 'string', FALSE, 6),
('psychological_info', 'any_suicidal_thoughts', 'boolean', FALSE, 7),
('psychological_info', 'anxiety_level', 'integer', FALSE, 8),
('psychological_info', 'history_of_substance_abuse', 'string', FALSE, 9),
('psychological_info', 'support_system', 'string', FALSE, 10);

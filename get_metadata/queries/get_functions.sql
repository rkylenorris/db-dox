

SELECT 
    f.object_id,
    s.name AS schema_name,
    f.name AS function_name,
    m.definition,
    f.create_date,
    f.modify_date
FROM 
    sys.objects f
JOIN 
    sys.schemas s ON f.schema_id = s.schema_id
JOIN 
    sys.sql_modules m ON f.object_id = m.object_id
WHERE 
    f.type IN ('FN', 'IF', 'TF');  -- Scalar, inline, or table-valued functions

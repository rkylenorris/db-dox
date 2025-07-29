

SELECT 
    p.object_id,
    s.name AS schema_name,
    p.name AS procedure_name,
    m.definition,
    p.create_date,
    p.modify_date
FROM 
    sys.procedures p
JOIN 
    sys.schemas s ON p.schema_id = s.schema_id
JOIN 
    sys.sql_modules m ON p.object_id = m.object_id;

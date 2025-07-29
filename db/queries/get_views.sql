

SELECT 
    v.object_id,
    s.name AS schema_name,
    v.name AS view_name,
    m.definition,
    v.create_date,
    v.modify_date
FROM 
    sys.views v
JOIN 
    sys.schemas s ON v.schema_id = s.schema_id
JOIN 
    sys.sql_modules m ON v.object_id = m.object_id;

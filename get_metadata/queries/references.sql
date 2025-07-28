

SELECT 
    referencing_schema.name AS referencing_schema,
    referencing.name AS referencing_entity,
    referencing.type_desc AS referencing_type,
    referenced_schema.name AS referenced_schema,
    referenced.name AS referenced_entity,
    referenced.type_desc AS referenced_type
FROM 
    sys.sql_expression_dependencies d
JOIN 
    sys.objects referencing ON d.referencing_id = referencing.object_id
JOIN 
    sys.objects referenced ON d.referenced_id = referenced.object_id
JOIN 
    sys.schemas referencing_schema ON referencing.schema_id = referencing_schema.schema_id
JOIN 
    sys.schemas referenced_schema ON referenced.schema_id = referenced_schema.schema_id
WHERE 
    referencing.type IN ('P', 'V')  -- Procedures or Views
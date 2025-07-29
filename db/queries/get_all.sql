    SELECT SCHEMA_NAME(o.schema_id) AS SchemaName,
        o.name AS [Name],
        'view' as [Type],
        m.definition AS [Definition],
        NULL as [Parameter],
        Null as [ParamType],
        null as [ParamLength],
        d.referenced_schema_name AS TableSchema,
        -- schemas of tables used
        d.referenced_entity_name AS TableName
    FROM sys.views o
        JOIN sys.sql_modules m ON o.object_id = m.object_id
        LEFT jOIN sys.sql_expression_dependencies d on o.object_id = d.referencing_id
union
    SELECT
        SCHEMA_NAME(o.schema_id) AS SchemaName,
        o.name AS [Name],
        'stored procedure' as [Type],
        m.definition AS [Definition],
        P.name AS [Parameter],
        type_name(p.user_type_id) as [ParamType],
        p.max_length as [ParamLength],
        d.referenced_schema_name AS TableSchema,
        -- schema of table used
        d.referenced_entity_name AS TableName
    FROM sys.objects o
        JOIN sys.sql_modules m ON o.object_id = m.object_id
        LEFT Join sys.parameters p ON o.object_id = p.object_id
        LEFT jOIN sys.sql_expression_dependencies d on o.object_id = d.referencing_id
    WHERE o.type = 'P'
-- P = SQL Stored Procedure
ORDER BY [Type],
    SchemaName,
    [Name];
 
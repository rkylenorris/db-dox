CREATE TABLE [databases] (
  [id] string PRIMARY KEY,
  [name] string,
  [definition] string,
  [created_at] datetime,
  [modified_at] datetime
)
GO

CREATE TABLE [schemas] (
  [id] string PRIMARY KEY,
  [name] string,
  [database_id] string,
  [created_at] datetime,
  [modified_at] datetime
)
GO

CREATE TABLE [tables] (
  [id] string PRIMARY KEY,
  [name] string,
  [schema_id] string,
  [created_at] datetime,
  [modified_at] datetime
)
GO

CREATE TABLE [columns] (
  [id] string PRIMARY KEY,
  [name] string,
  [data_type] string,
  [table_id] string,
  [is_nullable] string,
  [default_value] string,
  [created_at] datetime,
  [modified_at] datetime
)
GO

CREATE TABLE [stored_procedures] (
  [id] string PRIMARY KEY,
  [name] string,
  [schema_id] string,
  [definition] string,
  [created_at] datetime,
  [modified_at] datetime
)
GO

CREATE TABLE [stored_procedure_parameters] (
  [id] string PRIMARY KEY,
  [name] string,
  [data_type] string,
  [stored_procedure_id] string,
  [ordinal_position] string,
  [is_output] string
)
GO

CREATE TABLE [references] (
  [id] string PRIMARY KEY,
  [ref_type] string,
  [ref_id] string,
  [table_id] string,
  [created_at] datetime
)
GO

ALTER TABLE [schemas] ADD FOREIGN KEY ([database_id]) REFERENCES [databases] ([id])
GO

ALTER TABLE [tables] ADD FOREIGN KEY ([schema_id]) REFERENCES [schemas] ([id])
GO

ALTER TABLE [columns] ADD FOREIGN KEY ([table_id]) REFERENCES [tables] ([id])
GO

ALTER TABLE [stored_procedures] ADD FOREIGN KEY ([schema_id]) REFERENCES [schemas] ([id])
GO

ALTER TABLE [stored_procedure_parameters] ADD FOREIGN KEY ([stored_procedure_id]) REFERENCES [stored_procedures] ([id])
GO

ALTER TABLE [references] ADD FOREIGN KEY ([table_id]) REFERENCES [tables] ([id])
GO

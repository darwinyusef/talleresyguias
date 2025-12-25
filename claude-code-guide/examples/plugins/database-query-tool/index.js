/**
 * Database Query Tool Plugin
 * Permite a Claude Code ejecutar queries SQL de forma segura
 */

const Database = require('better-sqlite3');
const path = require('path');

class DatabaseQueryTool {
  constructor(options = {}) {
    this.dbPath = options.dbPath || path.join(process.cwd(), 'database.sqlite');
    this.db = null;
    this.readOnly = options.readOnly !== false; // Por defecto read-only
  }

  init() {
    this.db = new Database(this.dbPath, {
      readonly: this.readOnly,
      fileMustExist: true
    });
  }

  validateQuery(query) {
    const upperQuery = query.trim().toUpperCase();

    // En modo read-only, solo permite SELECT
    if (this.readOnly && !upperQuery.startsWith('SELECT')) {
      throw new Error('Only SELECT queries are allowed in read-only mode');
    }

    // Blacklist de operaciones peligrosas
    const dangerous = ['DROP', 'TRUNCATE', 'DELETE FROM', 'ALTER'];
    for (const keyword of dangerous) {
      if (upperQuery.includes(keyword)) {
        throw new Error(`Dangerous operation detected: ${keyword}`);
      }
    }

    return true;
  }

  async execute({ query, params = [] }) {
    try {
      if (!this.db) this.init();

      this.validateQuery(query);

      const upperQuery = query.trim().toUpperCase();

      if (upperQuery.startsWith('SELECT')) {
        // Query de lectura
        const stmt = this.db.prepare(query);
        const rows = params.length > 0 ? stmt.all(...params) : stmt.all();

        return {
          success: true,
          type: 'select',
          rowCount: rows.length,
          rows: rows,
          columns: rows.length > 0 ? Object.keys(rows[0]) : []
        };
      } else {
        // Query de escritura (INSERT, UPDATE)
        const stmt = this.db.prepare(query);
        const info = params.length > 0 ? stmt.run(...params) : stmt.run();

        return {
          success: true,
          type: 'write',
          changes: info.changes,
          lastInsertRowid: info.lastInsertRowid
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
        query: query
      };
    }
  }

  async getTables() {
    const query = `
      SELECT name, type
      FROM sqlite_master
      WHERE type IN ('table', 'view')
      AND name NOT LIKE 'sqlite_%'
      ORDER BY name
    `;

    const result = await this.execute({ query });
    return result.rows || [];
  }

  async getSchema({ tableName }) {
    const query = `PRAGMA table_info(${tableName})`;

    const result = await this.execute({ query });
    return {
      success: true,
      table: tableName,
      columns: result.rows || []
    };
  }

  close() {
    if (this.db) {
      this.db.close();
      this.db = null;
    }
  }
}

// Plugin configuration
module.exports = {
  name: 'database-query',
  version: '1.0.0',
  description: 'Execute SQL queries against SQLite database',

  tools: [
    {
      name: 'query_database',
      description: 'Execute SQL SELECT query',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'SQL SELECT query to execute'
          },
          params: {
            type: 'array',
            description: 'Query parameters for prepared statement',
            items: {
              type: ['string', 'number', 'null']
            }
          }
        },
        required: ['query']
      },
      async handler(args) {
        const tool = new DatabaseQueryTool({ readOnly: true });
        const result = await tool.execute(args);
        tool.close();
        return result;
      }
    },

    {
      name: 'list_tables',
      description: 'List all tables and views in database',
      parameters: {
        type: 'object',
        properties: {}
      },
      async handler() {
        const tool = new DatabaseQueryTool({ readOnly: true });
        const tables = await tool.getTables();
        tool.close();
        return {
          success: true,
          tables: tables
        };
      }
    },

    {
      name: 'describe_table',
      description: 'Get schema information for a table',
      parameters: {
        type: 'object',
        properties: {
          tableName: {
            type: 'string',
            description: 'Name of the table to describe'
          }
        },
        required: ['tableName']
      },
      async handler(args) {
        const tool = new DatabaseQueryTool({ readOnly: true });
        const schema = await tool.getSchema(args);
        tool.close();
        return schema;
      }
    }
  ]
};

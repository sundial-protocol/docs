import { NodeConfig } from "@/config.js";
import { UtilsDB } from "@/database/index.js";
import { BatchDBOp, DB } from "@ethereumjs/util";
import { fromHex } from "@lucid-evolution/lucid";
import { Effect, pipe } from "effect";
import { Sql, TransactionSql } from "postgres";

export class PostgresDB<TKey extends string, TValue extends Uint8Array>
  implements DB<TKey, TValue>
{
  _sql: Sql | undefined;
  _database: Effect.Effect<Sql, Error, NodeConfig>;
  _tableName: string;
  _referenceTableName: string | undefined;

  constructor(tableName: string, referenceTableName?: string, sql?: Sql) {
    this._tableName = tableName;
    this._referenceTableName = referenceTableName;
    this._sql = sql;
    this._database = Effect.gen(function* () {
      const nodeConfig = yield* NodeConfig;
      return nodeConfig.DB_CONN;
    });
  }

  open = async (copyFromReference?: true) => {
    if (!this._sql) {
      const pool = await Effect.runPromise(
        pipe(this._database, Effect.provide(NodeConfig.layer)),
      );
      this._sql = pool;
    }
    await this._sql`SET client_min_messages = 'error'`;
    await UtilsDB.mkKeyValueCreateQuery(this._sql, this._tableName);
    if (this._referenceTableName && copyFromReference) {
      try {
        const tableName = this._sql(this._tableName);
        const refTableName = this._sql(this._referenceTableName);
        await this._sql.begin(async (sql) => {
          await UtilsDB.clearTable(sql, this._tableName);
          await sql`
INSERT INTO ${tableName}
SELECT * FROM ${refTableName}`;
        });
      } catch (e) {
        throw e;
      }
    } else {
      try {
        await this.clear();
      } catch (e) {
        throw e;
      }
    }
  };

  conclude = async () => {
    if (this._sql) {
      await this.transferToReference();
      await this._sql.end();
    }
  };

  get = async (key: TKey): Promise<TValue | undefined> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else {
      try {
        const result = await this
          ._sql`SELECT value FROM ${this._sql(this._tableName)} WHERE key = ${Buffer.from(fromHex(key))}`;
        if (result.length > 0) {
          return result[0].value;
        } else {
          return undefined;
        }
      } catch (err) {
        throw err;
      }
    }
  };

  put = async (key: TKey, val: TValue): Promise<void> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else {
      await this
        ._sql`INSERT INTO ${this._sql(this._tableName)} (key, value) VALUES (${Buffer.from(fromHex(key))}, ${Buffer.from(val)}) ON CONFLICT (key) DO UPDATE SET value = ${Buffer.from(val)}`;
    }
  };

  _put = async (sql: TransactionSql, key: TKey, val: TValue): Promise<void> => {
    await sql`INSERT INTO ${sql(this._tableName)} (key, value) VALUES (${Buffer.from(fromHex(key))}, ${Buffer.from(val)}) ON CONFLICT (key) DO UPDATE SET value = ${Buffer.from(val)}`;
  };

  del = async (key: TKey): Promise<void> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else {
      await this
        ._sql`DELETE FROM ${this._tableName} WHERE key = ${Buffer.from(fromHex(key))}`;
    }
  };

  _del = async (sql: TransactionSql, key: TKey): Promise<void> => {
    await sql`DELETE FROM ${this._tableName} WHERE key = ${Buffer.from(fromHex(key))}`;
  };

  batch = async (opStack: BatchDBOp<TKey, TValue>[]): Promise<void> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else {
      try {
        await this._sql.begin(async (sql) => {
          for (const op of opStack) {
            if (op.type === "del") {
              await this._del(sql, op.key);
            }

            if (op.type === "put") {
              await this._put(sql, op.key, op.value);
            }
          }
        });
      } catch (err) {
        throw err;
      }
    }
  };

  getAll = async (): Promise<{ key: Uint8Array; value: Uint8Array }[]> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else {
      const result = await this
        ._sql`SELECT * FROM ${this._sql(this._tableName)}`;
      return result.map((row) => ({
        key: row.key,
        value: row.value,
      }));
    }
  };

  getAllFromReference = async (): Promise<
    { key: Uint8Array; value: Uint8Array }[]
  > => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else if (this._referenceTableName) {
      const result = await this
        ._sql`SELECT * FROM ${this._sql(this._referenceTableName)}`;
      return result.map((row) => ({
        key: row.key,
        value: row.value,
      }));
    } else {
      throw new Error("No reference tables set");
    }
  };

  clear = async (): Promise<void> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else {
      await UtilsDB.clearTable(this._sql, this._tableName);
    }
  };

  clearReference = async (): Promise<void> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else if (this._referenceTableName) {
      await UtilsDB.clearTable(this._sql, this._referenceTableName);
    } else {
      throw new Error("No reference tables set");
    }
  };

  _clearReference = async (sql: TransactionSql): Promise<void> => {
    if (this._referenceTableName) {
      await UtilsDB.clearTable(sql, this._referenceTableName);
    } else {
      throw new Error("No reference tables set");
    }
  };

  transferToReference = async (): Promise<void> => {
    if (!this._sql) {
      throw new Error("Database not open");
    } else if (this._referenceTableName) {
      try {
        const tableName = this._sql(this._tableName);
        const refTableName = this._sql(this._referenceTableName);
        await this._sql.begin(async (sql) => {
          await this._clearReference(sql);
          await sql`
INSERT INTO ${refTableName}
SELECT * FROM ${tableName}`;
        });
      } catch (e) {
        throw e;
      }
    } else {
      throw new Error("No reference tables set");
    }
  };

  shallowCopy = (): DB<TKey, TValue> => {
    return new PostgresDB(this._tableName, this._referenceTableName, this._sql);
  };
}

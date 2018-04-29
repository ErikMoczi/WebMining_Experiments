def drop_tables() -> str:
    return (
        'DROP TABLE IF EXISTS unique_user;\n'
        'DROP TABLE IF EXISTS web_mining;\n'
    )


def create_tables() -> str:
    return (
        'CREATE TABLE IF NOT EXISTS web_mining (\n'
        '  id                 INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n'
        '  user_id            INTEGER,\n'
        '  session_id_rlength INTEGER,\n'
        '  session_id_sttq    INTEGER,\n'
        '  ip                 VARCHAR(15),\n'
        '  cookie             VARCHAR(255),\n'
        '  dtime              VARCHAR(28),\n'
        '  unixtime           INTEGER                           NOT NULL,\n'
        '  length             INTEGER,\n'
        '  request_method     VARCHAR(5),\n'
        '  url                TEXT,\n'
        '  http_version       VARCHAR(10),\n'
        '  status_code        INTEGER,\n'
        '  referrer           TEXT,\n'
        '  agent              TEXT                              NOT NULL\n'
        ');\n'
        'CREATE INDEX web_mining_ip_agent_unixtime_index\n'
        '  ON web_mining (ip, agent, unixtime);\n'
        '\n'
        'CREATE INDEX web_mining_ip_agent_index\n'
        '  ON web_mining (ip, agent);\n'
        '\n'
        'CREATE TABLE IF NOT EXISTS unique_user (\n'
        '  user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n'
        '  ip      VARCHAR(15)                       NOT NULL,\n'
        '  agent   TEXT                              NOT NULL,\n'
        '  FOREIGN KEY (ip, agent) REFERENCES web_mining (ip, agent)\n'
        '    ON DELETE CASCADE\n'
        '    ON UPDATE CASCADE\n'
        ');\n'
        '\n'
        'CREATE INDEX unique_user_ip_agent_index\n'
        '  ON unique_user (ip, agent);\n'
    )


def web_mining_fill_user_id() -> str:
    return (
        'INSERT INTO unique_user (ip, agent)\n'
        '  SELECT\n'
        '    ip,\n'
        '    agent\n'
        '  FROM web_mining\n'
        '  GROUP BY ip, agent;\n'
        '  \n'
        'UPDATE web_mining\n'
        'SET user_id = (\n'
        '  SELECT uu.user_id\n'
        '  FROM unique_user uu\n'
        '  WHERE uu.ip = web_mining.ip AND uu.agent = web_mining.agent\n'
        ');\n'
    )


def web_mining_fill_length(stt_seconds: int) -> str:
    return (
               'UPDATE web_mining\n'
               'SET length = (\n'
               '  SELECT MIN(wm_next.unixtime) - web_mining.unixtime\n'
               '  FROM web_mining wm_next\n'
               '  WHERE wm_next.agent = web_mining.agent\n'
               '        AND wm_next.ip = web_mining.ip\n'
               '        AND (\n'
               '          (\n'
               '            wm_next.id > web_mining.id\n'
               '            AND wm_next.unixtime >= web_mining.unixtime\n'
               '          )\n'
               '          OR\n'
               '          (\n'
               '            wm_next.id <> web_mining.id\n'
               '            AND wm_next.unixtime > web_mining.unixtime\n'
               '          )\n'
               '        )\n'
               ');\n'
               '\n'
               'UPDATE web_mining\n'
               'SET length = NULL\n'
               'WHERE length > %i;\n'
           ) % (stt_seconds,)


def get_average_event_intensity() -> str:
    return (
        'SELECT\n'
        '  1/AVG(length)\n'
        'FROM web_mining\n'
    )


def get_web_mining_rlength() -> str:
    return (
        'SELECT\n'
        '  id,\n'
        '  user_id,\n'
        '  length,\n'
        '  unixtime\n'
        'FROM web_mining\n'
        'ORDER BY user_id, unixtime\n'
    )


def update_web_mining_session_id(session_type: str, session_id: int, ids: list) -> str:
    return (
               'UPDATE web_mining\n'
               'SET %s = %i\n'
               'WHERE id IN(%s)\n'
           ) % (session_type, session_id, ','.join(map(str, ids)),)
